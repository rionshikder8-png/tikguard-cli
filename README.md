# TikGuard CLI

A local, privacy-first TikTok safety helper for **Android Termux**. Pure Python standard library, no API keys, no server.

> Repository: https://github.com/rionshikder8-png/tikguard-cli

## What it does
1. **Username Scanner**: checks username *syntax* and builds a profile URL. It does **not** verify an account exists.
2. **Report Assistant**: prepares a *local* case for a genuine violation and opens official TikTok help. It never submits anything for you.
3. **Account Recovery Assistant**: official recovery checklist and links. Never asks for passwords, codes, cookies or tokens.
4. **Security Center**: password, 2-step verification, trusted devices, phishing tips.
5. **Local Case Manager**: SQLite storage, list/view/JSON export/delete.
6. **Settings & Diagnostics**: versions, optional dependencies, offline detection.

## Install (Termux)
1. Install Termux from F-Droid or the official GitHub releases.
2. Update and install tools:
   ```sh
   pkg update && pkg upgrade
   pkg install python git termux-tools
   ```
3. Clone and enter the repository:
   ```sh
   git clone https://github.com/rionshikder8-png/tikguard-cli.git
   cd tikguard-cli
   ```
4. (Optional, recommended) read `install.sh`, then run it. It only creates a `tikguard` command:
   ```sh
   sh install.sh
   ```
5. Start:
   ```sh
   tikguard            # after install.sh
   # or
   ./tikguard.sh       # or: python main.py
   ```
Diagnostics: `python main.py diagnostics`

## Update
```sh
cd tikguard-cli
git pull
```
Your cases live in `~/.tikguard` (outside the repo), so updates never touch them.

## Uninstall
```sh
sh uninstall.sh     # removes only the launcher command; keeps your data
```
Then delete the cloned folder. To also delete data (irreversible): `rm -r ~/.tikguard`.

## Data & privacy
- Cases are stored in `~/.tikguard/cases.db` (override with `TIKGUARD_HOME`). Exports go to `~/.tikguard/exports/`.
- No hidden network requests. The network is only used when you choose to open a link, or run diagnostics (a single connection test).
- Never store passwords, codes or tokens in notes.
- Databases and exports are in `.gitignore`.

## Limitations
- Syntax validation only; no account lookup, no private data, no scraping.
- Official TikTok URLs may change; verify them at https://support.tiktok.com/.
- Tested on Linux with Python 3.11. Not yet tested on a physical Android device.

## Development
```sh
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m flake8 .
```

---

# TikGuard CLI (বাংলা)

Android Termux-এর জন্য একটি লোকাল, প্রাইভেসি-বান্ধব TikTok নিরাপত্তা সহায়ক। কোনো API key বা সার্ভার লাগে না।

## কী কী করে
1. **ইউজারনেম স্ক্যানার**: ইউজারনেমের গঠন যাচাই করে ও প্রোফাইল লিংক বানায়। অ্যাকাউন্ট আছে কিনা তা **যাচাই করে না**।
2. **রিপোর্ট অ্যাসিস্ট্যান্ট**: সত্যিকারের নীতিভঙ্গের জন্য লোকাল কেস তৈরি করে। TikTok-এ **নিজে রিপোর্ট পাঠায় না**; আপনাকে অফিসিয়াল পেজে নিজে জমা দিতে হবে।
3. **অ্যাকাউন্ট রিকভারি**: অফিসিয়াল চেকলিস্ট ও লিংক। পাসওয়ার্ড/কোড/কুকি/টোকেন কখনো চায় না।
4. **সিকিউরিটি সেন্টার**: পাসওয়ার্ড, টু-স্টেপ ভেরিফিকেশন, ডিভাইস রিভিউ, ফিশিং থেকে সুরক্ষা।
5. **লোকাল কেস ম্যানেজার**: SQLite-এ সংরক্ষণ, দেখা, JSON এক্সপোর্ট, মুছে ফেলা।
6. **সেটিংস ও ডায়াগনস্টিকস**।

## ইনস্টল (Termux)
```sh
pkg update && pkg upgrade
pkg install python git termux-tools
git clone https://github.com/rionshikder8-png/tikguard-cli.git
cd tikguard-cli
sh install.sh
tikguard
```
`install.sh` চালানোর আগে ফাইলটি পড়ে নিন। এটি শুধু একটি `tikguard` কমান্ড তৈরি করে। কমান্ড ছাড়াও চালানো যায়: `python main.py`

## আপডেট
```sh
cd tikguard-cli
git pull
```
আপনার কেসগুলো `~/.tikguard`-এ থাকে, তাই আপডেটে মুছে যায় না।

## আনইনস্টল
`sh uninstall.sh` চালান (ডাটা থাকবে), তারপর ক্লোন করা ফোল্ডার মুছুন। ডাটাও মুছতে চাইলে: `rm -r ~/.tikguard` (ফেরত পাওয়া যাবে না)।

## সীমাবদ্ধতা
শুধু গঠন যাচাই করে; কোনো প্রাইভেট তথ্য দেখে না। এখনো আসল Android ডিভাইসে পরীক্ষা করা হয়নি।
