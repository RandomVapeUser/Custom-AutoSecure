import requests
import json

def removeProof(amrp: str, apicanary: str, amsc: str, proofID: str):

    remove = requests.post(
        "https://account.live.com/API/Proofs/DeleteProof",
        headers={
            "Cookie": f"AMRPSSecAuth={amrp}; amsc={amsc}",
            "canary": apicanary,
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "proofId": proofID,
            "uiflvr": 1001,
            "uaid": "da90e97a55cf431385e2dd217c6ba873",
            "scid": 100109,
            "hpgid": 201030
        })
    )

    print(remove.text)
    print(remove.headers)

    # {"apiCanary":"u5ITSK+\/7zw2eAi8QTGulwAcpeVl98ZW22h5PDCdEgoG0aURjhcX4W8VmvZIFs+mjvz\/PS6GIMXNCUXTNS\/8EgAgSR8e3R0cR1RVe9zQbvI7IhMWB4Re36Mhpex4cQPa3DyJ4ohTSNGu\/KgKJ97hxWsfZ3ntF7bI\/KbT0QlABosx2g4eeFGagmXDwjeEFfqyHggf96nyL\/6u\/oONVTSkbMfm0JQQ92DNVY8ZbbPTr244Ip4KFpwbtlVPqO6AeCO3:2:3c","telemetryContext":"617XT3ra3JVn1EMS766h2OgqQNdUOpKRadCk4hwpvnEsq6StivhAoEiPKSSDDdA1h\/JJM21KSmDM3SOxdKq3aJp\/rTxW4mOPzKAW\/ZOg4TgkRsVz5C25VFLU720DdXkLTaqxTiu6qO5ZPosLXWjJnQ==:2:3"}    
    
    if remove.status_code == 200:
        print("[+] - Removed Proof")
    else:
        print("[-] - Failed to remove Proof")