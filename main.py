import os
import discord
import requests
import random
import json
from replit import db

client = discord.Client()

def get_random_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


keywords = ["courage","dreams","fear","freedom","future","happiness","inspiration","leadership","life","love","past","success","work"]

if "zen" not in db.keys():
  db["zen"] = True

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if db["zen"]:
    if msg.startswith('$random'):
      quote = get_random_quote()
      await message.channel.send(quote)


    if msg.startswith('$quote '):
      keyword = msg.split("$quote ",1)[1]

      if keyword in keywords:
        link = "https://zenquotes.io/api/quotes/" + keyword
        response = requests.get(link)
        json_data = json.loads(response.text)
        rand = random.randint(0, len(json_data))
        quote = json_data[rand]['q'] + " -" + json_data[rand]['a']
      
        await message.channel.send(quote)

    if msg.startswith("$keywords"):
      await message.channel.send(keywords)


  if msg.startswith("$zen"):
    value = msg.split("$zen ",1)[1]

    if value.lower() == "on":
      db["zen"] = True
      await message.channel.send("Zen Bot is on.")
    elif value.lower() == "off":
      db["zen"] = False
      await message.channel.send("Zen Bot is off.")


client.run(os.getenv('ZEN_TOKEN'))