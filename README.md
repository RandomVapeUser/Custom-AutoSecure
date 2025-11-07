# AutoSecure

**Contact:** `salomao31_termedv3`

---

## Overview

AutoSecure is a **Discord bot for ethical cybersecurity training**. It simulates account verification scams to teach users how attackers trick people into sharing information. It’s **for educational use only** — never use it on real users or accounts.

---

## Updates

* [ ] Switch to channel-based logging (instead of webhooks)
* [ ] Improve embed designs
* [ ] Fix missing `LastCookie` issue
* [ ] Add Minecraft account checking
* [x] Added `SECURE_ANY` (can secure any Microsoft account)
* [x] Improved Modal1 UI

---

## Disclaimer

**This tool is for learning, testing, and awareness training only.** Using it without consent or on real systems is illegal. The author is not responsible for misuse.

---

## How to Set Up

1. **Install Python 3.11:**
   [Download Here](https://www.python.org/downloads/release/python-3110/)

2. **Create a Bot:**
   Get a Discord bot token and enable all intents.

3. **Get API Keys (optional):**

   * [MailSlurp](https://www.mailslurp.com/) for AutoSecure features.
   * [Hypixel](https://developer.hypixel.net/) for Minecraft stats.

4. **Configure the Bot:**
   Edit `config.py` and add:

   ```python
   DISCORD_TOKEN = "YOUR_TOKEN"
   MAILSLURP_API_KEY = "YOUR_MAILSLURP_KEY"
   HYPIXEL_API_KEY = "YOUR_HYPIXEL_KEY"
   ADMINS = [YOUR_DISCORD_ID]
   ```

5. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Bot:**

   ```bash
   python bot.py
   ```

7. **Sync Commands:**
   In Discord, type:

   ```
   !sync global
   ```

8. **Set Logs Channel:**
   Use `/webhook` or channel setup command to select where logs go.

---

## Tips

* Always test in a **private server** with consent.
* Never collect real account info.
* Use disposable test accounts.

---

## Common Issues

* **Config not saving:** open config file in `"w"` mode when writing.
* **Missing cookie errors:** ensure async waits are used instead of sleep.

---

## License

Use responsibly under an open, educational license (MIT recommended).
