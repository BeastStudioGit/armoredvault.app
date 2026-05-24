---
title: What Armored Vault Doesn't Protect Against (And What You Can Do About It)
date: 2026-04-12
author: Robert Lewis
---

# What Armored Vault Doesn't Protect Against (And What You Can Do About It)

I'm going to do something that most security apps don't do: tell you exactly what Armored Vault *can't* protect you from. And then — more importantly — I'm going to give you specific, common-sense things you can do to defeat each of those limits yourself.

Security is never one product. It's a stack of choices. Armored Vault is a strong layer in that stack, but the layers above and below it (your Mac or iPad, your habits, the files you import) belong to you. This article is about owning those layers like an adult.

## Limit 1: Malware running inside an unlocked vault session

Once you unlock the vault, your files are decrypted in memory so the app can show them to you. If something malicious is running inside the Armored Vault process during that window, it can in principle read what's decrypted. The "/" kill switch and the iPad's face-down auto-lock exist to keep that window short, but they don't make it zero.

Here's the thing: on Apple platforms, the realistic version of this risk isn't "Armored Vault gets malware injected into it." OS-level sandboxing prevents one app from reaching into another. The realistic version is **"the file you imported was a malicious file designed to exploit the viewer that opens it."** A booby-trapped MP4 that targets a flaw in the video decoder. A PDF with a JavaScript payload aimed at PDFKit. A JPEG crafted to exploit ImageIO. These attacks are real — Apple has patched several of them in recent years (BLASTPASS, FORCEDENTRY).

### What you can do

- **Vet the source of every file before you import it.** This is the single most powerful thing you can do. If a file came from someone you trust, sent through a channel you trust (iMessage from a known contact, AirDrop from a person standing next to you, a USB stick you bought yourself and have controlled the whole time), the risk is very low. If it came from an email attachment you weren't expecting, a file-sharing site, a stranger's AirDrop in a coffee shop, or a USB drive somebody handed you — **don't import it without thinking very hard.**
- **Keep your operating system updated.** Every iOS and macOS point release patches dozens of security holes, including the kind of parser exploits that target media files. The day Apple ships an update, install it. There is no good reason to delay.
- **Don't import files you don't recognize.** If you're cleaning out your camera roll and you see a photo from August 2022 that you don't remember taking, the safe move is to delete it, not to vault it.
- **Be especially skeptical of email attachments.** Email is the single most common malware delivery vector on the planet. If somebody emails you a "tax document" you weren't expecting, treat it as hostile until you can verify with the sender by phone or in person.
- **AirDrop hygiene matters.** Set AirDrop to "Contacts Only" or "Off" by default. Only switch it to "Everyone for 10 Minutes" when you're actively expecting a transfer from someone in front of you. The default of accepting AirDrops from strangers is how attackers in airports and conference halls deliver malicious files.
- **USB drives have provenance.** A USB drive from a vendor table at a trade show is not the same as one you bought sealed at Best Buy. If you don't know where a drive has been, scan it on a computer with antivirus before plugging it into your device's import flow. (Yes, even iPad imports can carry malicious files; the malice is in the file, not the drive.)

The shortest version: **be picky about what you bring inside.** A vault is only as private as the files you put in it. If you import a malicious file and then unlock the vault, you've handed the attacker the keys yourself.

## Limit 2: Weak passphrase choice

I covered this in detail in the previous article, but it bears repeating in this list. Armored Vault's encryption is excellent, but if you pick a passphrase a computer can guess in a million tries, none of it saves you.

### What you can do

- **Use the in-app Diceware generator.** The default is 10 words (~129 bits) — that's the security tier the architecture is designed for. You can drop to 7 words (~91 bits) if you need a more memorable passphrase, but 7 is the minimum the generator will offer.
- **Aim for the ceiling, not the floor.** The Strong gate (≥80 bits) is the *floor*. Don't stop there. A 10-word Diceware passphrase is millions of times stronger than a barely-Strong custom passphrase.
- **Write it on paper. Store it physically.** Do not put it in a password manager.

The previous article goes deep on this. Read it.

## Limit 3: Shoulder-surfing and coerced disclosure

If somebody is standing behind you watching you type your passphrase, no encryption helps. If somebody has physical control over you and is demanding that you unlock the vault, the encryption isn't the bottleneck — *you are*.

### What you can do

- **Type your passphrase the way you type a password at an ATM.** Cup your hand. Position your screen. Be aware of who's behind you, especially in coffee shops, airports, and hotel lobbies. The threat from a coworker glancing over your shoulder is more common than people think.
- **Use the Decoy Vault feature for the coerced-disclosure case.** Armored Vault's decoy vault is the answer to "give me the passphrase or else." It's a fully functional, indistinguishable second vault with its own passphrase. You can pre-populate it with plausible-looking but harmless content. If somebody coerces you into unlocking, you give up the decoy passphrase. There is no flag on disk that tells the attacker the real vault exists. Two cryptographically independent vaults sit in the same app sandbox.
- **Practice using the decoy.** Don't set it up and forget it. Periodically open the decoy and add to it so it has a believable history.
- **Think about who would coerce you and what they'd accept.** If you're a journalist working in hostile territory, the threat model is different than if you're a parent worried about your kid finding old photos. Match your decoy contents to the threat. Empty decoys are suspicious. Decoys full of vacation photos and tax PDFs are not.

## Limit 4: Files after they leave the vault

When you export a file out of Armored Vault — whether to Finder, the Files app, a connected drive, or as a Plain ZIP — the file is no longer protected by Armored Vault's encryption. The Plain ZIP option is *unencrypted by design* (you explicitly chose that format). The Encrypted ZIP option uses WinZip AE-2 (AES-256-CTR) with PBKDF2-HMAC-SHA1 for compatibility with other software, which is weaker than the in-vault format.

### What you can do

- **Default to Encrypted ZIP for any export that leaves your control.** If the destination is a thumb drive going to your accountant, an email attachment to a lawyer, or a backup to a cloud service, use Encrypted ZIP and pick a strong passphrase for the ZIP itself. Tell the recipient the passphrase through a different channel (a phone call, in person — not the same email).
- **Plain ZIP is for trusted destinations only.** Use it when the destination is a system you control end-to-end (your own encrypted external drive, your own home computer with full-disk encryption on). Don't use it for anything that crosses the public internet.
- **For full-vault migration, use Full Armored Vault Backup.** That writes an encrypted snapshot of the whole vault to a drive (or any Finder/Files destination). Pair with Restore from Backup on the destination device — the data never exists as plaintext outside the vault.
- **Delete exports as soon as they've served their purpose.** Exports left sitting in Downloads, Files, or a cloud folder become a quiet copy of your vault contents that has none of Armored Vault's protections. Treat exports the way you'd treat printed sensitive documents: use them, then shred.
- **Empty Trash regularly.** Files you delete from the vault go to Trash with restore support. They're still encrypted while in Trash, but if you're sure you don't want them, emptying Trash gets them off your device entirely.

## Limit 5: Backups and cloud snapshots you don't control

Armored Vault configures the vault directory with `isExcludedFromBackup`, which keeps it out of iCloud Backup and out of encrypted local backups (Finder backups of iPad; Time Machine snapshots on Mac, where the app's container is excluded by default). That's the right default. But if you ever copy your vault contents into a folder that *is* synced or backed up (iCloud Drive, Drive, Dropbox), or you take a manual snapshot, those copies are no longer governed by that exclusion setting.

### What you can do

- **Don't move vault files into iCloud Drive, Drive, or any sync folder.** Use Armored Vault's Full Armored Vault Backup or Full Decrypted Export features (which write to destinations you control) instead of dragging files into a sync directory.
- **If you back up your iPad, use encrypted local backups via Finder, not iCloud Backup.** Apple's iCloud Backup is encrypted in transit and at rest with Apple's keys; an encrypted local Finder backup uses your password and never leaves your computer. (Even though Armored Vault excludes itself from backup, this is good general hygiene for everything else.)
- **Treat any cloud-stored copy of vault contents as compromised.** If a file lives in iCloud, Drive, Dropbox, or any other cloud, assume the cloud provider could in principle access it. That doesn't mean they will — but if you wanted that level of protection, you wouldn't have put it there.

## The bigger picture

You're the security executive of your own digital life. I built Armored Vault to handle the part I can do well — strong encryption, no backdoors, no telemetry, no data collection. But the choices about what you import, where you store backups, who you trust, and what you do when somebody asks for access — those are yours.

The good news is that the recommendations in this article aren't exotic. They're the same things security professionals do for their own families. Vet your sources. Update your software. Don't reuse passwords. Use a decoy if duress is part of your threat model. Encrypt anything that leaves your control. Treat email attachments as hostile until verified.

Do those things and you've built a security stack that an enormous majority of attackers will fail at. The encryption I built is one strong layer. The other layers are the ones you control. Own them.

— Robert
