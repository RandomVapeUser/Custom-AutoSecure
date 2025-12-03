import requests
import re

def removeServices(amrp: str, canary: str):

    uatRequest = requests.get(
        url = "https://account.live.com/consent/Manage?guat=1",
        headers = {
            "Cookie": f"AMRPSSecAuth={amrp}"
        }
    )

    # This is SLOW 
    matches = re.findall(r'data-clientid="(.*?)"', uatRequest.text, re.IGNORECASE)
    print("Done with regex")
    print(matches)
    if not matches:
        print("[+] - No SSID Services Found")
    else:
        for id in matches:
            print("Done")
            requests.post(
                url = f"https://account.live.com/consent/Edit?client_id={id}",
                headers = {
                    "Cookie": f"AMRPSSecAuth={amrp}"
                },
                data = f"canary={canary}"
            )