import os
import csv
import requests
from bs4 import BeautifulSoup
import discord 
from mojang import MojangAPI

client = discord.Client()

#Statut

@client.event
async def on_ready():
    print("Le bot est prêt.")
    await client.change_presence(activity=discord.Game(name="-help"))

#Messages

@client.event
async def on_message(message):
		if message.content.startswith('-profil'):
			pseudo = message.content[8:]
			uuid = MojangAPI.get_uuid(pseudo)
			name = MojangAPI.get_name_history(uuid)
			for data in name:
				name_history = f"{data['name']} depuis {data['changed_to_at']}"
			mojang = requests.get("https://api.mojang.com/user/profiles/{}/names" .format(uuid))
			page = mojang.content
			soup = BeautifulSoup(page, features="lxml")
			body = soup.find("body")
			fois = f"{body.string}".count("changedToAt")
			embed = discord.Embed(title="", description="", color=0x3464eb)
			embed.set_author(name=f"Profil de {pseudo}", icon_url="https://cdn.discordapp.com/attachments/566639457286094860/841555331631808532/Minecraft-logos-removebg-preview.png", url = f"http://fr.namemc.com/profile/{pseudo}")
			embed.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}")
			embed.add_field(name ="**UUID**", value =f"`{uuid}`", inline =False)
			embed.add_field(name ="**Skin**", value =f"[Télécharger le Skin de {pseudo}](https://mc-heads.net/download/{uuid})", inline =False)
			embed.add_field(name = "Nombre de fois où le pseudo a été changé :", value =f"`{fois}`" )
			await message.channel.send(embed = embed)

		if message.content.startswith('-help'):
			await message.channel.send("**Les commandes du bot sont :**\n\n`-profil [pseudo]` pour afficher le profil Minecraft d'un joueur.\n`-hypixel` pour afficher les infos sur le serveur hypixel.")

		if message.content.startswith("-hypixel"):
			hypixel_online = requests.get("https://minecraft-api.com/api/ping/status/mc.hypixel.net/25565")
			content = hypixel_online.content
			soup2 = BeautifulSoup(content, features="lxml")
			page = soup2.find("body")
			hypixel_players = requests.get("https://minecraft-api.com/api/ping/online/mc.hypixel.net/25565")
			content2 = hypixel_players.content
			soup3 = BeautifulSoup(content2, features="lxml")
			page2 = soup3.find("body")
			hypixel_ver = requests.get("https://minecraft-api.com/api/ping/version/mc.hypixel.net/25565")
			content3 = hypixel_ver.content
			soup4 = BeautifulSoup(content3, features="lxml")
			page3 = soup4.find("body")
			ver =f"{page3.string}"[12:]
			
			if page.string == "En ligne":
				status =f"`{page.string}` :green_circle:"

			else:
				status =f"`{page.string}` :red_circle:"
			
			embed = discord.Embed(title="", description="", color=0xfc033d)
			embed.set_author(name=f"Infos Hypixel", icon_url="https://downloadwap.com/thumbs2/wallpapers/p2ls/2019/misc/50/9f09606513560842.jpg")
			embed.set_thumbnail(url="https://downloadwap.com/thumbs2/wallpapers/p2ls/2019/misc/50/9f09606513560842.jpg")
			embed.add_field(name ="Statut", value =f"{status}", inline =False)
			embed.add_field(name ="Nombre de joueurs", value =f"`{page2.string} / 200000`", inline =False)
			embed.add_field(name ="Version du serveur", value =f"`{ver}`" )
			await message.channel.send(embed = embed)

		if message.content.startswith("-paladium"):
			hypixel_online = requests.get("https://eu.mc-api.net/v3/server/status-http/proxy.paladium-pvp.fr")
			content = hypixel_online.content
			soup2 = BeautifulSoup(content, features="lxml")
			page = soup2.find("body")
			hypixel_players = requests.get("https://api.serveurs-minecraft.com/api.php?Joueurs_En_Ligne_Ping&ip=proxy.paladium-pvp.fr&port=25565")
			content2 = hypixel_players.content
			soup3 = BeautifulSoup(content2, features="lxml")
			page2 = soup3.find("body")
			hypixel_ver = requests.get("http://api.serveurs-minecraft.com/api.php?Version_Ping&ip=proxy.paladium-pvp.fr&port=25565")
			content3 = hypixel_ver.content
			soup4 = BeautifulSoup(content3, features="lxml")
			page3 = soup4.find("body")
			ver =f"{page3.string}"
			
			if page.string.startswith("true"):
				status ="`En ligne` :green_circle:"

			else:
				status ="`Hors Ligne` :red_circle:"
			
			embed = discord.Embed(title="", description="", color=0xfc033d)
			embed.set_author(name=f"Infos Palafdium", icon_url="https://pbs.twimg.com/profile_images/1249367268162764800/nT0fW4I-.jpg")
			embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1249367268162764800/nT0fW4I-.jpg")
			embed.add_field(name ="Statut", value =f"{status}", inline =False)
			embed.add_field(name ="Nombre de joueurs", value =f"`{page2.string}`", inline =False)
			embed.add_field(name ="Version du serveur", value =f"`{ver}`" )
			await message.channel.send(embed = embed)



client.run("TOKEN")
