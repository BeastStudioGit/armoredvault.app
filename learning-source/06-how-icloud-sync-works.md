---
title: How iCloud Sync Works
date: 2026-06-18
author: Robert Lewis
---

# How iCloud Sync Works

For most of its life, Armored Vault was a single-device app on purpose. One vault, one device, nothing leaving it. That's the safest design there is — but it's also inconvenient the moment you own more than one Apple device and want your vault on both.

iCloud Sync is how Armored Vault crosses that gap *without* giving up the thing that makes it a vault. The short version: your devices can share one vault through your own iCloud, but iCloud — and I — never see your files, your file names, or your key. Here's exactly how that works, and the deliberate, slightly old-fashioned design choices that keep it safe.

## The one rule everything else follows: iCloud only holds ciphertext

Before anything leaves your device, it's already encrypted. The file blobs Armored Vault uploads are the very same AES-256-GCM ciphertext that lives in your vault — encrypted on-device, under your key, before iCloud ever sees them. The index that records which blob is which file — names, sizes, types — is itself encrypted under your vault key and uploaded as one more opaque blob.

So what actually sits in iCloud is a pile of encrypted blobs and an encrypted index. Apple can't read it. I can't read it. There is no point at which a readable copy of your files exists anywhere but on a device you've personally unlocked.

And it is *your* iCloud — your private iCloud database, tied to your Apple Account. There is no Armored Vault server in the middle. I don't run infrastructure that touches your data, because there is no infrastructure (see **Why I Don't Collect Your Data**). Sync is your devices talking to your own iCloud, with me nowhere in the loop.

## Why a vault can't sync like Notes or Photos

Apple's own apps sync by merging: two devices both make changes, and the system stitches them together. That's fine for notes and photos, where a merge conflict means a duplicated line, not a catastrophe.

For an encrypted vault, naive two-way merging is dangerous. If two devices each believe they hold the truth and quietly disagree, you can end up with conflicts you can't see — and the failure mode isn't a harmless duplicate, it's *silently losing a change you thought you'd made.* For files you're trusting a vault to keep, that is unacceptable.

So Armored Vault doesn't merge. It uses a deliberately conservative model: **one device is in charge at a time.**

## Source and Mirror

At any moment, exactly one of your devices is the **Source** — the one in charge of edits. Every other device is a **Mirror**: a read-only copy that pulls the Source's vault down from iCloud and shows it to you.

A Mirror is read-only on purpose. You can browse everything, open anything, play your media — but you can't edit it out from under the Source. That is the whole trick: because only one device can ever write, your devices can't drift out of step or fight over which version is real. The right phrase for what a Mirror does is *pull from*, not *sync to* — it pulls down the Source's truth; it never pushes a competing version up.

## Taking over: changing which device leads

When you do want to edit on a Mirror, you **take over.** That device becomes the Source, and your others quietly become Mirrors of it from then on. Nothing is deleted and nothing is lost — the only thing that changes is which device leads. To hand the lead back, you take over on the other device.

There is one safety rule here worth understanding, because it protects you from a mistake you'd never see coming: **taking over requires an internet connection.**

A take-over has to be coordinated through iCloud, so the device that *was* the Source learns it has been handed off. If a device can't reach iCloud, Armored Vault won't let it take over — it tells you to connect first. That feels like a small inconvenience, but it is preventing a real one: if two devices both believed they were in charge (because they couldn't reach iCloud to sort it out), an edit you made on one would silently vanish the next time they reconnected. Rather than risk that, a Mirror that's offline simply stays read-only and asks you to get online.

The flip side is the good news for travel: **the device that already *is* the Source can edit offline all it wants.** Its changes queue up and upload the moment it is back on a connection. So if you're boarding a flight, make the device you're bringing the Source *before* you lose signal, and you can work the whole way — it syncs when you land.

## How a second device can read the vault at all

For another device to make sense of the ciphertext it pulls, it needs your vault's key. Armored Vault never copies that key into iCloud in usable form. Instead, the key is stored **wrapped** — encrypted under a key derived from your passphrase — and a joining device only unwraps it after *you* enter that same passphrase on it.

So even the key material that passes through iCloud is itself encrypted, and worthless without the passphrase only you know. iCloud sees a wrapped blob; your device turns it back into a usable key locally, in memory, after you authenticate. The unwrapped key never leaves a device and never lands in the cloud.

## Your decoy stays out of it

If you use Armored Vault's decoy vault, it is deliberately excluded from sync. Your decoy never touches iCloud — so nothing about syncing can hint that a second, real vault exists. Sync only ever concerns your real vault, and only while you are unlocked into it.

## What iCloud can and can't see — honestly

I try to be straight about limits everywhere else, so here too. What iCloud *can* observe is metadata: that some number of encrypted blobs exist, roughly how large they are, and when they were uploaded or changed. That is the unavoidable cost of using cloud storage at all.

What iCloud *cannot* see is the part that matters: your file names, your file contents, what any file actually is, your passphrase, or your usable key. And what *I* can see is nothing — there is no server I run, no dashboard, no copy of anything. The blobs are strictly between your devices and your iCloud.

## It's optional, and reversible

Sync is off until you turn it on. If you never set it up, Armored Vault is exactly the single-device vault it has always been, and not one byte goes to iCloud. If you turn it on and later change your mind, you can disable it and clear the cloud copy. Nothing about the feature is forced, sticky, or on by default.

## The bottom line

iCloud Sync lets one vault live on all your devices, through your own iCloud, while keeping every promise the single-device version made. Only ciphertext ever leaves your device. Only one device edits at a time, so nothing is lost to a merge. Your key passes through the cloud only in wrapped form, useless without your passphrase. Apple can't read it, and I can't either.

It's sync built like a vault — cautious on purpose.

— Robert
