import requests
import base64
import json

def get_capes(uuid: str) -> str:

    response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
    response.raise_for_status()
    capedata = response.json()
    try:
        if "properties" in capedata:

            b64value = capedata["properties"][0]["value"]
            decoded_bytes = base64.b64decode(b64value).decode("UTF-8")
            decodedcapedata = json.loads(decoded_bytes)

            if decodedcapedata["textures"]["CAPE"]:
                print(f"Capes Found!")
                return decodedcapedata["textures"]['CAPE']["url"]
            else:
                print("No Capes Found")
        else:
            print("No 'properties' key found in the response.")
    except:
        return ""