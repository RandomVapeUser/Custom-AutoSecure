# AutoSecure

**Contact:** `salomao31_termedv3 / https://discord.gg/HEUTEjsprE`

---

## Overview

AutoSecure is a **Discord bot for ethical cybersecurity training**. It simulates account verification scams to teach users how attackers trick people into sharing information. It’s **for educational use only** — never use it on real users or accounts.

It was made with the purpose of giving everyone acess to an autosecure without the need of having to pay for one or having to use dhooked free ones, it is fully open-source so you can check the code yourself. It will have most features that paid autosecures have.

I will be updating this regularly.

---

### Securing (In Progress)

- Request Based
- Sends Email OTP/Authenticator Numbers to any email bypassing 2FA
- Provides Skyblock/Hypixel Info
- Automaticly secures accounts
- Checks Minecraft (Owns MC, Capes)
  
## Updates

* [ ] Family Check
* [ ] Locked Check
* [ ] Change main alias
* [ ] Remove Zyger Explot 
* [ ] Get Account Info
* [X] Change Security Email
* [X] Change Password
* [X] Improve embed designs
* [X] Add Minecraft account checking
* [X] Switching to request based securing (Removing playwright)
* [X] Switch to channel-based logging (instead of webhooks)
* [x] Improved modal_one 

---

## Disclaimer

**This tool is for learning, testing, and awareness training only.** If you encounter any issue dm me / make a [issue](https://github.com/RandomVapeUser/Custom-AutoSecure/issues). The author is not responsible for misuse. 

---

## How to Set Up

1. **Install Python 3.11:**
   [Download Here](https://www.python.org/downloads/release/python-3110/)

2. **Create a Bot:**
   Get a Discord bot token and enable all intents [here](https://discord.com/developers/applications).

3. **Get API Keys:**

   * [MailSlurp](https://www.mailslurp.com/) for Aliases replacement.* 
   * [Hypixel](https://developer.hypixel.net/) for Hypixel stats. (Optional)

4. **Configure the Bot:**
   Edit `config.json` and add:

   ```python
   bot_token = "YOUR_DISCORD_BOT_TOKEN"
   mailslurp_key = "YOUR_MAILSLURP_KEY"
   hypixel_key = "YOUR_HYPIXEL_KEY"
   owners = [YOUR_DISCORD_ID]
   ```

5. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Bot:**

   ```bash
   python bot.py
   ```

7. **Set Logs Channel:**
   Use `/set` to select where logs go.

   ⚠️ Do NOT modify the channel ID in the config if you don't know what you are doing.
   If you remove the ID after setting it up and the bot stops working it is you fault hence why I did not add any checking if it is there.

8. **Set your Verification Embed:**
   Use `send_embed` to send the verification embed in the same channel you are in.
   
---


## License

Use responsibly under an open, educational license (MIT recommended).
