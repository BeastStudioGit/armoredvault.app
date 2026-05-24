---
title: Choosing a Strong Passphrase (And Why "Password123" Won't Cut It)
date: 2026-04-09
author: Robert Lewis
---

# Choosing a Strong Passphrase (And Why "Password123" Won't Cut It)

Here's the uncomfortable truth about Armored Vault: the encryption is mathematically excellent, but I cannot save you from a bad passphrase. If you pick `"password"` or `"letmein2026"`, the entire architecture I described in the previous article collapses. Not because the encryption is weak — it isn't — but because somebody who can guess your passphrase doesn't need to break the encryption. They just unlock the vault the way you do.

This article is about how to pick a passphrase that no one — not your nosy roommate, not a forensic technician, not a botnet farm with a million GPUs — can guess in any reasonable amount of time.

## What we're actually defending against

When somebody tries to break into your vault, they do one of two things:

1. **Guess your passphrase from a list of common patterns.** "password," "qwerty," your birthday, your dog's name, the team you root for. Modern attackers use lists of *billions* of leaked passwords from previous breaches. If your passphrase is on one of those lists — or follows a common pattern — they don't need to "crack" anything.
2. **Brute force every possible combination.** Try every 8-character string, then every 9-character string, and so on, hoping to stumble onto yours.

Armored Vault's architecture makes brute force *slow*. PBKDF2 with 600,000 iterations means each guess takes a fraction of a second on Apple hardware, and even on dedicated cracking rigs (which are roughly 1,000× faster) you're still looking at a millisecond per guess. So the math problem becomes: how many guesses does the attacker need before they're likely to land on yours?

That number is determined entirely by your passphrase's **entropy** — a measure of how unpredictable it is.

## Entropy in plain English

Entropy is measured in bits. Each bit doubles the number of possible values. If your password has 1 bit of entropy, an attacker needs 2 guesses on average. 10 bits = 1,024 guesses. 50 bits = a quadrillion guesses.

Here's what real passwords look like in entropy terms:

- `"password"` — under 5 bits. Brute-forced instantly. Not because it's short, but because it's on every guessing list ever made.
- `"P@ssw0rd1!"` — about 15 bits *if you account for the predictable substitutions* (every cracker knows `@` for `a`). Looks "complex," cracks in seconds.
- `"Tr0ub4dor&3"` (the famous XKCD example) — about 28 bits. Still cracks in hours on modest hardware.
- A truly random 8-character password (mixed case, digits, symbols) — about 52 bits. Strong against casual attackers, vulnerable to a serious adversary with time.
- A 10-word Diceware passphrase like `"correct horse battery staple plumber zebra envelope mountain coffee daughter"` — about **130 bits**. The heat death of the universe arrives before this gets cracked.

That last one is what Armored Vault is built around.

## What is Diceware, and why does it work so well?

Diceware is a method of generating passphrases by rolling physical dice (or, in our case, using a cryptographically secure random number generator) to pick words from a numbered list. Each word in a standard Diceware list contributes about 12.9 bits of entropy. Ten words gives you ~130 bits.

Two things make Diceware special:

1. **The randomness is real.** A computer rolling cryptographic dice doesn't have any pattern an attacker can predict. There's no birthday in there, no pet's name, no leetspeak.
2. **The words are memorable.** Your brain is much better at remembering "dolphin marble candle thunder pillow" than at remembering `Xj7#qPm2!nL@`. And — critically — a long random passphrase is *exponentially* stronger than a short complex one. Length beats complexity every time.

Armored Vault includes a built-in Diceware passphrase generator. Use it on the passphrase setup screen and you'll get a 10-word random phrase. **Use it.** Or roll your own with five physical dice and a Diceware word list (the EFF publishes one for free at `eff.org`).

## Strong common-sense recommendations

Here's how to actually pick a passphrase that protects you:

### Do these things

- **Use the in-app generator.** It produces passphrases at the strength tier the architecture is designed for. There's no faster way to get this right.
- **If you make your own, use at least 8 random words.** From a real word list, picked by real randomness (dice or a secure RNG), not by you "thinking of random words." Humans are terrible at randomness.
- **Write it down on paper and put it somewhere safe.** A safe-deposit box, a fireproof home safe, a sealed envelope with your will. This is the *opposite* of bad practice — paper that an attacker would need physical access to your home to steal is far more secure than a passphrase you've memorized so badly you reuse it across services.
- **If you're going to memorize it, use it daily for the first two weeks.** Type it out. Build muscle memory. The first few days are the highest-risk window for forgetting.
- **Pick a passphrase you'll actually type.** If it's so long you start hating it, you'll be tempted to weaken it later. Ten Diceware words is the sweet spot — strong, and tolerable to type.

### Don't do these things

- **Don't reuse a passphrase you use anywhere else.** Not your email, not your bank, not Netflix. If any one of those services gets breached (and they do, constantly), your password ends up on a list. Vault passphrases must be unique to the vault.
- **Don't pick something meaningful.** Your wedding date, your kid's middle name, your favorite quote. If anyone who knows you could guess it within 100 tries, it's not strong enough.
- **Don't use leetspeak as your "complexity."** `M0nday!` is no harder to crack than `monday`. Crackers know all those substitutions.
- **Don't store it in a password manager.** Wait — really? Yes, really, for *this specific app*. The whole point of Armored Vault is that no other software gatekeeps your files. If your password manager gets breached, you don't want your vault passphrase in there with everything else. Memorize it, write it on paper, do both. Don't put it in 1Password.
- **Don't share it with anyone "just in case."** Not your spouse, not your sibling, not your lawyer. If you want a contingency plan for your death, leave the written passphrase with your will, in a sealed envelope, with instructions. Don't tell anyone the contents while you're alive.

## What Armored Vault does to nudge you in the right direction

Armored Vault enforces:

- **Strength gating.** The Save button doesn't enable until your passphrase scores at least "Strong" (≥80 bits) on the in-app strength meter. The meter is dictionary-aware and diceware-aware: it down-rates common words and patterns, and it doesn't credit fake entropy from separators or casing on a Diceware-shaped phrase. You can't game it by typing `"passwordpasswordpassword"`. In practice, "Strong" means roughly a 7-word Diceware passphrase or equivalent randomness.

This means you can't accidentally choose something terrible. But you *can* still choose something mediocre — a barely-Strong passphrase is much weaker than a 10-word Diceware phrase. **Don't aim for the floor. Aim for the ceiling.** The cost of a great passphrase versus a barely-acceptable one is about 30 extra seconds of typing, once. The benefit is decades of security.

## "But what about Face ID or Touch ID? Doesn't using my biometrics weaken everything?"

Reasonable question. The short answer is **no, biometric unlock does not weaken your vault** — and here's exactly why, in the same architectural terms as the previous article.

When you enable biometric unlock in Armored Vault (Face ID on iPad, Touch ID on Mac), the app does *not* store your passphrase anywhere. It also does not derive a second, weaker key. What it does is take the **MFEK** (the master file encryption key, already in memory because you just unlocked the vault with your passphrase) and write a copy of it into a special Keychain entry that's gated by your device's **Secure Enclave** — the dedicated security co-processor present on every supported Mac (Apple Silicon or T2-equipped Intel) and iPad. The entry is created with two access flags that matter:

- **`kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`** — the entry never leaves the device, never appears in any backup, and is destroyed if you remove the device passcode or account password entirely.
- **`.biometryCurrentSet`** — the entry is bound to the *exact* biometric enrollment that exists right now. If you re-enroll Face ID, add or remove a fingerprint, or change the device passcode/account password, the OS automatically destroys the entry. There is no way for someone to enroll a new face or finger and unlock your vault.

When you use biometric unlock later, the Secure Enclave performs the biometric match in dedicated hardware (the device's CPU never sees the face or fingerprint data) and only releases the MFEK if the match succeeds. The MFEK then goes straight back into memory, exactly as if you'd typed your passphrase. Decryption happens normally from there.

**Why this is still safe:**

- The MFEK in the biometric Keychain entry is protected by the same hardware that protects Apple Pay, your iCloud Keychain, and your device unlock. The Secure Enclave is a separate co-processor with its own encrypted memory; even Apple cannot extract its contents.
- Any biometric or OS-level security change — re-enrollment, a passcode/password change, certain OS updates — invalidates the entry. The next unlock requires your passphrase. The entry is then re-created (if you choose) with the new biometric template.
- On iPad, after every reboot, Face ID is **locked out** until your passphrase has been entered once. A freshly stolen, freshly rebooted iPad cannot be unlocked with a face alone, ever. On Mac, Touch ID persists across restarts by design, but the OS-level invalidation triggers above still apply.
- Disabling biometric unlock in Armored Vault deletes the biometric Keychain entry immediately. The MFEK copy is gone; only your passphrase can recover the vault.

**What biometric unlock does *not* do:**

- It does not bypass your passphrase. Your passphrase is still the only thing that can recover the vault from a reset, an OS update, or a re-enrollment.
- It does not weaken the encryption. The same AES-256-GCM is used; biometrics only change how the MFEK gets back into memory.
- It does not leak biometric data to Armored Vault. The app never sees your face or fingerprint — the OS hands the app a yes/no answer from the Secure Enclave, and that's it.

**The honest tradeoff to be aware of:** if someone with physical control over you can compel a biometric match — by holding your iPad up to your face, or placing your finger on Touch ID — they can unlock the vault while biometrics are in a valid session. That's true of every biometric-protected app. The mitigations are:

- **(iPad) Press the side button five times** to immediately disable Face ID until the passphrase is entered. This is an iOS-wide feature; learn it.
- **(Mac) Tap the red Lock button** at the top of every library to immediately lock the vault. Re-unlock requires your passphrase or Touch ID — but it's no longer in an already-authenticated session.
- **Use the Decoy Vault** if duress is part of your threat model — see Article 3.
- **Disable biometric unlock inside Armored Vault** if your threat model includes "someone might force a biometric match." The vault then requires your passphrase every time, period.

For everyone else, biometric unlock is a convenience layer built on the strongest hardware Apple offers. The math doesn't get weaker. The passphrase remains the root of trust. Use it with confidence — and know exactly when to turn it off.

## The "what if I forget?" question

I'll be direct: **if you forget your passphrase, your vault is gone.** Forever. There is no recovery email, no security questions, no Apple ID reset, no support ticket I can answer that will get your files back. The cryptography I described in the previous article makes recovery mathematically impossible — that's the whole point. If I had a backdoor, the Department of Justice could compel me to use it. I don't.

This means **the responsibility for remembering or storing your passphrase is yours.** Take it seriously. Write it on paper. Put the paper somewhere physical and safe. The strength of an architecture that no government can break is also its hardest constraint: it cannot tell you apart from anyone else who doesn't know the passphrase.

## The bottom line

Generate it with the built-in tool. Write it on paper. Put the paper somewhere safe. Type the passphrase every day for two weeks until you know it cold. Don't reuse it. Don't share it. Don't store it in your password manager.

Do those things and your vault is protected by math that no current or near-future attacker can defeat. Skip them and the strongest encryption in the world doesn't help you.

— Robert
