import discord
import json
from discord import ui, TextInput  
from views.button_one import ButtonViewOne
import os

class MyModalThree(ui.Modal, title="Verification"):
    box_one = ui.TextInput(label="Title", placeholder="Your Custom Title", required=True)
    box_two = ui.TextInput(label="Verify Message", style=discord.TextStyle.paragraph, placeholder="Your Custom Message", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        if not os.path.exists("data.json"):
            interaction.response.send_message("You need to set the webhook first with /webhook <url>")
            return
        
        # Switched into 2 diferent commands and removed unnecessary custom hex colour 
        title = self.box_one.value
        description = self.box_two.value

        colour = discord.Colour.green
        embed = discord.Embed(
            title=title,
            description=description,
            colour=colour
        )

        await interaction.channel.send(embed=embed, view=ButtonViewOne())