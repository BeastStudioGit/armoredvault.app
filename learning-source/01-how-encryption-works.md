---
title: How Armored Vault Encrypts Your Files
date: 2026-04-06
author: Robert Lewis
---

# How Armored Vault Encrypts Your Files

I built Armored Vault because I wanted a place — on a Mac or iPad — where private files were actually private. Not "private if the device's lock screen holds," not "private until somebody plugs the device into a forensic tool," but private in the only sense that matters: unreadable to anyone who doesn't know my passphrase. This article walks through how that actually works under the hood. No marketing words, no hand-waving. If you're going to trust an app with your files, you deserve to understand what it's doing with them.

## The one sentence version

**Your 10-word Diceware passphrase is the root of trust.** Without it, every file body, every filename, and every byte of metadata in the vault is mathematically inaccessible. The system Keychain holds nothing that could substitute for it. If somebody seizes your unlocked device and pulls the entire app sandbox into a forensic tool, what they get is a directory full of `<random-uuid>.enc` files and a 104-byte key blob that's useless without your passphrase.

Now let me show you why that's true.

## The threat model

I designed Armored Vault to keep your files unreadable in three uncomfortable scenarios:

1. **Forensic seizure of an unlocked-but-locked device.** Somebody knows your device passcode or account password, throws the device into a forensic tool, and reads the entire app sandbox.
2. **Full filesystem access by an adversary.** Whether through a jailbroken iPad, malware with full disk access on a Mac, or a cloned disk image, every file in Armored Vault's container is exposed to inspection.
3. **Backup theft or cloud snapshot exposure.** Your data leaks through some channel that bypasses OS-level at-rest protection.

In all three cases, an attacker without your Diceware passphrase should see opaque ciphertext and not even be able to recover original filenames. That's the bar.

## The two architectural pillars

### Pillar 1: Passphrase-derived Key Encrypting Key (KEK)

Every vault has a randomly generated **Master File Encryption Key (MFEK)** — a 256-bit AES key that encrypts every file you import. The MFEK never lives unwrapped on disk, never lives in the Keychain, and never leaves memory while the vault is locked.

Instead, the MFEK is **wrapped** by a key derived from your Diceware passphrase. Here's the chain:

- Your passphrase (10 Diceware words ≈ 130 bits of entropy) goes through **PBKDF2-HMAC-SHA512** with a 32-byte random salt and 600,000 iterations. That derives a 256-bit Key Encrypting Key (KEK).
- The KEK **AES-GCM-encrypts** the MFEK. The result — 60 bytes of wrapped key plus the salt and iteration count — gets written to a 104-byte `vault.kek` file in the app's Documents directory.
- When you unlock, your passphrase is run through PBKDF2 against the stored salt. If the resulting KEK successfully GCM-decrypts the wrapped MFEK, the passphrase was correct.

Notice what's *not* in that chain: there is no hashed-password comparison anywhere. **AES-GCM's authentication tag is the passphrase check.** Wrong passphrase → wrong KEK → AES-GCM authentication fails → unlock denied. There's no "compare hashes" step that could be bypassed by patching the binary, because the cryptography itself is the gatekeeper.

The iteration count and salt are stored per-vault, so I can raise the difficulty parameter in future versions without breaking your existing vault.

The decoy vault (more on that elsewhere) uses the exact same scheme with its own independent `decoy.kek`, salt, MFEK, and passphrase. The two are cryptographically unrelated. There is no flag on disk that distinguishes "real vault" from "decoy vault."

### Pillar 2: UUID filenames + AVMD encrypted metadata header

Every file you import is renamed on disk to a random UUID with a `.enc` extension. The original filename, file kind, date added, and original byte size live only inside an **AVMD metadata header** prepended to the encrypted body:

- The AVMD header is 12 bytes of plaintext (the magic string `AVMD`, a version number, and a payload length) followed by a JSON blob of the metadata, **AES-GCM-encrypted under the same MFEK** that protects the file body.
- Without the MFEK — which requires your passphrase — neither the filename nor any metadata can be recovered.

A directory listing of an Armored Vault container looks like this:

```
4f8e7d10-...e6.enc
9a2b1c44-...07.enc
c1d8f3a9-...22.enc
```

No filenames. No extensions that hint at file types. No creation dates that match when you imported them. The forensic examiner cannot tell a video from a photo from a PDF from a tax return.

This invariant extends *beyond* the vault directory. Temporary files created during imports and document previews are also staged under random UUIDs in the system temp directory, never under your filename. The app's logging is sanitized — Armored Vault's log calls never emit user-chosen names, so even a captured device log won't leak what you imported.

## File body encryption (the IPAC chunked format)

Once your MFEK is decrypted into memory, file bodies are encrypted in a streaming, chunked format I call **IPAC**:

- **Cipher:** AES-256-GCM, via Apple's CryptoKit. Hardware-accelerated on every supported Mac and iPad.
- **Chunk size:** 4 MB. Each chunk is sealed independently with its own random 96-bit GCM nonce and 128-bit authentication tag.
- **IPAC body header:** 24 bytes — magic `IPAC`, version, chunk size, total chunks, plaintext file size.

Why chunked instead of whole-file encryption?

- **Streaming with bounded memory.** Multi-gigabyte videos work without holding the entire decrypted file in RAM. Each chunk is processed inside an `autoreleasepool` so transient buffers don't accumulate.
- **Random-access video playback.** When you scrub through a 1 GB encrypted video, Armored Vault decrypts only the chunks that overlap the requested byte range, with a 32-chunk (128 MB) cache and a 20-chunk speculative prefetch on a separate worker pool. Seek latency on a 1 GB encrypted file is indistinguishable from a small file.
- **Per-chunk integrity.** A single corrupt chunk fails authentication without contaminating the rest. If somebody tampered with byte 800 million of your video, you'd know — and the rest of the video would still be recoverable.

## The cryptographic primitives, end to end

| Purpose                          | Primitive                                | Library             |
| -------------------------------- | ---------------------------------------- | ------------------- |
| Passphrase → KEK                 | PBKDF2-HMAC-SHA512, 600K iter, 32B salt  | CommonCrypto        |
| KEK wraps MFEK                   | AES-256-GCM                              | CryptoKit           |
| File body (per 4 MB chunk)       | AES-256-GCM                              | CryptoKit           |
| AVMD metadata header             | AES-256-GCM (under MFEK)                 | CryptoKit           |
| Random salts, MFEK, nonces       | `SecRandomCopyBytes` (kernel CSPRNG)     | Security framework  |
| At-rest protection               | iOS `FileProtectionType.complete` / macOS App Sandbox + FileVault | Foundation |
| Backup exclusion                 | `URLResourceValues.isExcludedFromBackup` | Foundation          |

Armored Vault uses **only Apple system crypto** — CryptoKit, CommonCrypto, and the Security framework. No third-party crypto libraries. No custom modes. No rolled key schedules. This is also why the app qualifies for the U.S. Export Administration Regulations §740.17(a) exemption — the same reason no ERN/CCATS filing is required for App Store submission.

## What this provably protects

Even with full filesystem access — jailbreak, malware with full disk access, a forensic image, a backup leak — an attacker without your passphrase cannot:

- Decrypt any file body. The MFEK is wrapped under the passphrase-derived KEK, and AES-GCM provides both confidentiality and integrity.
- Recover any filename, file type, or date. That data lives inside the AVMD header, encrypted under the same MFEK.
- Distinguish a video from a photo from a document by inspection. They're all `<uuid>.enc` files with the same shape.
- Brute-force your passphrase practically. 600K PBKDF2-HMAC-SHA512 iterations gate every guess to a fraction of a second on modern Apple hardware. A 10-word Diceware passphrase has roughly 130 bits of entropy. Even at one billion guesses per second on dedicated hardware, the search space is computationally infeasible.
- Substitute, tamper with, or partially corrupt a file undetectably. Every chunk's GCM tag will fail authentication on any modification.
- Tell the real vault from the decoy by examining the disk. Both vaults have identical structure, independent keys, and no flag indicating which is "real."

## The bottom line

The strength of every guarantee above flows from one thing: your passphrase. If you pick something a computer can guess in a million tries, none of this saves you. If you pick a 10-word Diceware passphrase (or use the in-app generator), the math says cracking it would take roughly 25 quintillion years at one trillion guesses per second — vastly longer than the current age of the universe. For practical purposes, "uncrackable in any human lifetime" is the right way to think about it.

That's why the next article in this Learning Center is about choosing your passphrase. Read that one too. It's the single most important decision you make as an Armored Vault user.

— Robert
