---
title: Your Files Outside the Vault
date: 2026-04-15
author: Robert Lewis
---

# Your Files Outside the Vault

Armored Vault is excellent at one thing: keeping the files inside it private. But every file in your vault originally came from somewhere outside it — your Photos library, the system file browser, an email attachment, a USB drive — and most files eventually leave the vault again, whether to share with someone, archive somewhere durable, or migrate to a new Mac or iPad.

The handoff between "inside the vault" and "outside the vault" is one of the most underappreciated parts of personal security. This article is about doing those handoffs right.

## What "outside the vault" actually means

When a file is inside Armored Vault, it has every protection I described in Article 1: encrypted under your passphrase-derived key, filename obscured, metadata sealed, integrity tagged per chunk. The moment that file lives anywhere else — even somewhere else on the same device — it has none of those protections. The OS's at-rest encryption is good, but it's tied to your device passcode or Mac account password, not your vault passphrase. That's a categorically different security tier.

So: every time a file leaves the vault, you are downgrading its protection. Sometimes that's necessary. Sometimes it's avoidable. The question is: are you doing it on purpose?

## Importing: the "before" side of the boundary

Files you bring into the vault come from a small number of sources:

1. **Photos library** (your camera roll, screenshots, imported shots)
2. **The system file browser** (Finder on Mac, the Files app on iPad — both reach iCloud Drive, local storage, and mounted external drives)
3. **AirDrop or the share menu** (from another device or app)
4. **External USB-C / Thunderbolt storage** (drives, SD readers)

Each of these has its own hygiene story.

### From your Photos library

The cleanest source. You took the photos and videos yourself, on a device you control. The risk is low — but not zero. If your device has *ever* synced photos from a service that aggregates from other people (shared albums, iCloud Shared Library), some of those files were not actually taken by you, and the malicious-file scenario from Article 3 applies.

**Recommendations:**

- After you import photos and videos into the vault, **delete the originals from Photos** (and then empty Recently Deleted). The vault only protects what's *inside* it. A copy in Photos is a copy outside the vault.
- If the goal is to clean up your Photos library while keeping vault copies, batch-import then batch-delete. Don't leave originals laying around for "just in case" — that defeats the point.

### From the system file browser (Finder / Files)

This is where you import documents, PDFs, downloads, and anything you've previously stashed in iCloud Drive or another cloud provider. The risk depends entirely on how those files got there.

**Recommendations:**

- Import the file, verify it opens correctly inside the vault, then delete the source. Empty the Trash afterward.
- Don't trust filenames. A file called `tax_return_2024.pdf` could contain anything. Use Quick Look (spacebar in Finder; long-press preview in Files) *before* you import it, in a context where exposure is okay, to confirm it's what it claims to be.
- If a file came down from a sync service (Drive, Dropbox, iCloud Drive), remember that sync providers keep deletion histories. Deleting locally doesn't always remove the cloud copy. Sign in to the provider's web interface and confirm the file is gone from its cloud-side trash too.

### From AirDrop or the share menu

The risk depends on the sender. AirDrop from your spouse standing next to you is fine. AirDrop from a stranger in a coffee shop is hostile until proven otherwise.

**Recommendations:**

- Default your AirDrop setting to "Contacts Only" or "Receiving Off." Switch to "Everyone for 10 Minutes" only when you're actively expecting a transfer from someone in front of you, then let it switch back automatically.
- If you receive an unexpected AirDrop, decline. You can't know what's in a file you didn't expect.

### From external USB-C / Thunderbolt storage

External drives are a powerful and underused part of both Mac and iPad workflows. They're also a vector. The provenance of the drive matters more than the drive itself.

**Recommendations:**

- Use drives you bought yourself, sealed, from a known retailer.
- A drive you've handed to someone else and gotten back is now of unknown provenance. The safe assumption is that any file that wasn't on it when you handed it out, or any file modified while it was out of your control, could be hostile.
- If you're importing from a drive that's traveled, scan it with a file-scanning tool on a computer before bringing files into the vault.

## Inside the vault: the calm middle

Once a file is inside Armored Vault, it doesn't need ongoing maintenance from you. The encryption protects it. The vault doesn't talk to the network. The app doesn't collect telemetry. You can leave a file in the vault for ten years and it will be exactly as protected on year ten as on day one.

Two practices help even so:

- **Empty Trash regularly.** Deleted files go to Trash with restore support. They're still encrypted, but if you're sure they're trash, emptying Trash removes them from your device entirely.
- **Periodically open the decoy vault** if you have one set up, and add some plausible content. A decoy that hasn't been touched in two years is suspicious if anyone ever inspects it.

## Exporting: the "after" side of the boundary

This is where most people make mistakes. You spent all this effort encrypting your files, and then you export them somewhere that has none of those protections, and forget the exported copy exists.

Armored Vault gives you four export paths:

1. **Plain ZIP** — unencrypted ZIP archive. Convenience format. No password.
2. **Encrypted ZIP** — AES-256-CTR encrypted, password-protected. Compatible with most ZIP tools (7-Zip, Keka, WinZip).
3. **Full Decrypted Export** — sends the entire vault, every category, to an external drive in original file formats. One-tap bulk extraction; the drive holds plaintext during the export window.
4. **Full Armored Vault Backup** — a complete encrypted snapshot of the vault to an external drive or any Finder/Files destination. Everything stays encrypted on the destination. Pair with Restore from Backup on a new device to migrate the entire vault.

### Pick the right export format

- **For a destination you control end-to-end**: Plain ZIP is fine. Examples: an encrypted external drive that lives in your home safe; your own home computer with full-disk encryption on; another device of yours that you'll re-import to a new vault.
- **For anything that crosses the public internet or a system you don't control**: Encrypted ZIP, full stop. Email attachments, cloud uploads, drives going to a third party. Pick a strong passphrase for the ZIP. Communicate the passphrase to the recipient through a *different* channel than the one carrying the file. Phone call beats email. Text message beats email. *Any* second channel beats sending the file and password in the same message.
- **For migrating the whole vault to a new device**: use **Full Armored Vault Backup** — see the migration section below.
- **For ad-hoc external-drive archives**: Full Decrypted Export writes flat plain files to the drive. The drive holds plaintext during the export window, so use one you physically control and wipe it when you're done.

### Encrypted ZIP hides contents, not names

One detail people miss: an Encrypted ZIP encrypts the *contents* of every file, but the archive's directory listing — the file and folder names, sizes, and dates — is normally readable to anyone holding the ZIP, with or without the password. That isn't an Armored Vault choice; it's how the password-protected ZIP format works, and it's the price of the archive opening in any standard tool (7-Zip, Keka, WinZip).

So a file named `divorce-settlement-draft-3.pdf`, or a folder named `medical/oncology`, tells its story before anyone types the password.

Armored Vault gives you a way out: a **Hide file names** option on the export screen. With it on, your real files are placed inside an ordinary inner archive, and *that* is what gets encrypted — so the outer archive's readable index shows only a single, meaningless `ArmoredVault.zip`. The names now live inside the ciphertext, not in the cleartext index. The price is a small ritual for the recipient: they enter the password once, which produces `ArmoredVault.zip`, then they open that to reach the files. One password, standard tools, no extra software — just two extraction steps instead of one. The inner archive isn't itself password-protected and doesn't need to be: it only ever exists *after* someone has already supplied the correct password to unlock the outer layer, so an interceptor never sees it.

**Recommendation:**

- If the names themselves are sensitive, turn on Hide file names — and tell the recipient up front that they'll extract, enter the password, then open the `ArmoredVault.zip` inside. Skip that heads-up and they'll just be confused.
- If the names aren't sensitive, the plain Password-Protected Zip is fine and simpler on the other end.
- When even the *existence* of the file set is the secret, the strongest move is still not to export at all — keep it in the vault, or hand-carry it on a drive you physically control.

### Treat exports as time-limited

The biggest export mistake people make is forgetting that an export exists. You needed to send a PDF to your accountant, you exported it, you emailed it, the accountant got it, the job is done — and now there's a plaintext copy of that PDF sitting in Downloads or Files until your device is decommissioned.

**Recommendation:**

- After every export, set a calendar reminder for one week out: "Delete export." When the reminder fires, go delete the export. Empty the Trash / Recently Deleted. Done.
- For exports that went to cloud destinations (Drive, Dropbox, email "sent" folder), include those cleanup steps in the same reminder.

### What about sharing photos and videos?

When you want to send a photo or video to someone, the share menu is the easiest path. Use it knowing what's happening: the file is decrypted from the vault, handed to whatever app you chose to share with (Messages, Mail, Drive), and from that point lives in that app's storage. Messages keeps a copy. Mail keeps a copy. Drive keeps a copy.

**Recommendation:**

- For sensitive shares, prefer the Encrypted ZIP path: export the encrypted ZIP first, then attach it. The sender's app keeps a copy too — but the copy is the encrypted ZIP, not the plaintext file.
- For casual shares (a vacation photo to your spouse), use the share menu directly. The risk is low and the friction of Encrypted ZIP isn't worth it.

## Migrating to a new device

Eventually you'll get a new Mac or iPad. The cleanest way to bring your vault with you is the encrypted backup path — your files never exist in plaintext outside the vault during the migration:

1. On the old device: connect a USB-C drive (or pick any Finder/Files destination) and run **Full Armored Vault Backup** from Settings. The whole vault is written to the destination as encrypted ciphertext — files, names, dates, tags, favorites, the works.
2. Move the drive to the new device, or transfer the backup folder via your preferred channel. Even if somebody intercepts it in transit, the contents are still protected by your passphrase.
3. Install Armored Vault on the new device and set up a new vault using the **same passphrase** as your old one (so the backup can be decrypted on arrival).
4. Run **Restore from Backup** from Settings on the new device and point it at the backup folder. The entire vault is restored intact, including tags, favorites, and original dates.
5. Once you've verified everything restored correctly, securely erase the old device before disposing of it.
6. Optionally delete the backup destination if you don't want it lying around as a redundant copy — but unlike the old plain-files approach, the backup is encrypted, so leaving it in a desk drawer is no longer a plaintext risk.

If you need to migrate to a *different* passphrase, use **Full Decrypted Export** instead: it writes plain files to a drive, which you then ingest on the new device via Import from Folder. Wipe the drive immediately after import — plaintext on a drive in a desk drawer defeats the security model.

## What about iCloud?

A common question: "Can Armored Vault sync to iCloud?" The answer is no, and that's intentional. iCloud sync would mean handing decrypted file metadata to Apple's servers and creating cloud copies that your passphrase no longer protects.

If you're moving from another vault product that *did* use iCloud, Armored Vault can pull from iCloud Drive as a one-time migration source — but the framing matters: pull from, not sync to. The endpoint is your device. The cloud is the source you're migrating away from.

## The bottom line

Inside the vault, files are safe. Outside the vault, they're not. The boundary between the two is something *you* manage, every time you import or export.

The discipline isn't complicated:

- **Import deliberately.** Vet sources. Delete originals once they're vaulted.
- **Don't leak through copies.** Sync folders, share menus, email drafts, and AirDrop history all create copies you might forget about.
- **Export with intent.** Encrypted ZIP for anything leaving your control. Plain ZIP only for trusted destinations. Full Armored Vault Backup for migrations. Calendar reminders for cleanup.
- **Empty Trash, both in the vault and outside it.** Don't let "I might want this back" defeat your security model.

Treat the boundary like the lock on your front door — a checkpoint, not a permanent state. Files cross it deliberately, in both directions. When they're inside, the vault has them. When they're outside, you do.

— Robert
