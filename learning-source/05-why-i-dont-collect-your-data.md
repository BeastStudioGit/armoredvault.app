---
title: Why I Don't Collect Your Data
date: 2026-04-18
author: Robert Lewis
---

# Why I Don't Collect Your Data

Most apps you install on your Mac or iPad collect data about you. They send analytics, crash reports, usage telemetry, and occasionally things you'd be uncomfortable knowing they collect. They do it because data is valuable — to advertisers, to product teams, to investors, occasionally to law enforcement subpoenas. The whole modern app ecosystem assumes a default of "of course we'll collect data; what kind of company would we be if we didn't?"

Armored Vault is built on the opposite default: **collect nothing.** No analytics. No telemetry. No crash reporting service. No advertising IDs. No hidden network calls. No "anonymous usage statistics that totally couldn't be re-identified, I promise." Nothing.

This article is about why that decision is non-negotiable for an app like this, what it means in practice, and what you can verify yourself.

## The simplest reason: data I don't have can't be subpoenaed

I am one developer. I am not Apple, I am not Google, I am not 1Password. If I collected your data — even "anonymous" data, even just analytics about which buttons you tap — and a court order arrived demanding I turn it over, I would be legally obligated to comply. The size of my legal team is zero. The cost of fighting a subpoena is far more than I make from app sales. The realistic outcome: I'd hand the data over.

The only way to make that scenario impossible is to never collect the data in the first place. **You cannot subpoena data that doesn't exist.** Every byte of telemetry I never received is a byte that no court can demand from me.

This isn't a hypothetical. Vault and security apps get subpoenaed. They get pressured by governments. They get acquired by larger companies whose privacy policies suddenly change. The only durable defense is to architect the app so that the operator (me) genuinely can't help an attacker, even if asked.

## The technical version: what's actually happening

Let me show you what Armored Vault does and doesn't do at the network level.

**The app makes zero network calls during normal operation.** No "phone home." No update checks (the App Store handles updates). No analytics endpoints. No crash reporters. The app's `Info.plist` and entitlements do not enable arbitrary network access. There are no SDKs from Firebase, Mixpanel, Amplitude, Google Analytics, Segment, Sentry, or any other vendor. There is no advertising SDK. There is no "growth tooling."

**Crash reporting happens through Xcode Organizer.** Apple aggregates anonymized crash reports from devices that have opted into sharing diagnostics with developers. Those reports go through Apple's anonymization pipeline before I see anything, and only users who explicitly opted in (via Settings → Privacy → Analytics on iPad, or System Settings → Privacy & Security → Analytics & Improvements on Mac) participate. I don't run any other reporting layer.

**The app does not access the network for any purpose during vault operations.** It doesn't fetch icons. It doesn't validate licenses. It doesn't check for updates. The crypto operations are all local, the file storage is all local, the metadata is all local. The few network paths that exist are tied to actions you explicitly take — for example, using the share menu to send an exported file to a cloud-storage app. That app's network call happens; Armored Vault itself isn't connecting to anything.

**You can verify this yourself.** If you don't trust me, install a network monitoring tool (Little Snitch or LuLu on Mac; Charles Proxy or a comparable network monitor on a computer routing your iPad's traffic). Open Armored Vault. Use it normally for an hour. Watch what calls are made. The answer should be zero — except where you explicitly invoked a feature that hands files off to another app.

## The privacy policy in plain English

There's a formal privacy policy at `armoredvault.app/privacy.html`. The plain-English version is shorter:

- I do not collect your data.
- I cannot see what files you put in your vault.
- I do not know who you are.
- I do not have an account system.
- I do not require you to register, sign in, or create a profile.
- I do not track your usage of the app.
- I do not send anything about your usage to any server.
- I do not have a database of users because I do not have users in any sense beyond "people who downloaded a binary from the App Store."

If a government agency, a private investigator, a journalist, a hacker, or anyone else asks me what's in your vault, the truthful answer is: **I have no idea, and I have no way to find out.**

## Why I made these choices

A few reasons, in descending order of importance.

### 1. The product can't credibly be what it claims to be otherwise

If I told you "Armored Vault encrypts your files with a passphrase only you know" and then quietly collected analytics that included your file counts, file sizes, file types, vault open frequency, and feature usage patterns, the sentence would be technically true but morally a lie. The whole *point* of a privacy vault is that I'm not in the loop. The first time I add a telemetry SDK, I'm in the loop. The architecture doesn't exist.

### 2. I genuinely don't want the responsibility

Holding user data is a liability. Even "anonymous" telemetry can be re-identified given enough cross-references. Even encrypted analytics can leak through metadata. Holding nothing is the only state in which I can sleep at night, knowing that no breach of my infrastructure could harm you. There's nothing to breach. There's no infrastructure that holds your data.

## What about debugging?

A reasonable question: how do I fix bugs if I'm not collecting telemetry?

The answer is the same as how software was debugged for decades before telemetry became universal: users tell me when things break, and I fix them. There's a Support URL on the App Store listing that points to the support page. If you have a bug, write it up there. If it's a crash, the Xcode Organizer shows me the anonymized crash reports from users who opted in via Settings. That's a smaller dataset than telemetry would give me, but it's been enough for every bug I've fixed so far.

The other reality is that Armored Vault is intentionally a small, focused app. Fewer features mean fewer bugs. A vault that does one thing well is easier to keep correct than a vault that does ten things mediocrely. The simplicity of the product makes the no-telemetry choice tractable.

## What about future features?

I'll be transparent about anything that ever changes here:

- **If a future feature requires the network**, it will be a feature you explicitly invoke. It will not become a background process. It will not "phone home." If a feature ever required a server I run, I'd document it explicitly and you could choose not to use it.
- **If I ever consider adding telemetry**, I won't do it quietly. I'll write a Learning Center article about exactly what would be collected and why, and you'll get to decide before any data leaves your device. The default would be off.
- **If anyone ever offers to acquire Armored Vault**, the no-data-collection commitment is something I'd refuse to compromise on. If that's a deal-breaker, I won't sell.

## The bottom line

You should be able to trust the apps you let near your private files. Not because you "trust the developer" — that's a weak guarantee that depends on the developer's mood, finances, and integrity over time. You should be able to trust the apps because the apps are *architected* in a way that doesn't require you to trust anyone.

Armored Vault tries to be that kind of app. Your data lives on your device, encrypted under your passphrase. I don't see it. I don't collect it. I don't track you. There is no server. There is no database. There is no analytics dashboard somewhere with your usage patterns on it. There is the binary you downloaded from the App Store, and there is your device, and there is your passphrase, and there is nothing else.

That's the deal. I'm going to keep it.

— Robert
