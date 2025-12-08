import requests
import re

def removeServices(amrp: str, amsc: str, canary: str):
    # Create a session to maintain cookies across requests
    session = requests.Session()
    
    uatRequest = session.get(
        url="https://account.live.com/consent/Manage?guat=1",
        headers={
            "Cookie": f"AMRPSSecAuth={amrp}"
        }
    )

    print(f"Canary: {canary}")
    print(f"AMRP: {amrp}")
    print(f"AMSC: {amsc}")

    matches = re.findall(r'data-clientId="([^"]+)"', uatRequest.text, re.IGNORECASE)
    
    if not matches:
        print("[+] - No SSID Services Found")
        return
    
    for client_id in matches:
        response = session.post(
            url=f"https://account.live.com/consent/Edit?client_id={client_id}",
            headers={
                "Cookie": f"AMRPSSecAuth={amrp}; amsc={amsc}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://account.live.com"
            },
            data = f"canary={canary}",
            allow_redirects = False
        )
        
        # Check if the redirect was successful
        # 302 -> 200 usually means success
        # Check the final URL or response content
        print(f"ID: {client_id} | Status: {response.status_code} | Final URL: {response.url}")
