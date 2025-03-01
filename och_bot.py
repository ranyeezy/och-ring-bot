import requests
import discord
from bs4 import BeautifulSoup
import urllib.parse
import json


class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content == 'fpring':
            floor_price = await self.get_onchain_heroes_ring_floor_price()
            embed = discord.Embed(
                title="OCH Genesis Ring",
                description=f"",
                color=discord.Color.blue()  # You can choose any color
            )
            embed.add_field(name="Floor Price", value=f'{floor_price/10**18:.2f} ETH', inline=False)
            embed.set_image(url="https://raw.seadn.io/files/9637918b237c511371d10ba1243d19a5.gif")
            embed.set_footer(text="Made by poosox -- RNs Copyright Ⓒ 2025 ")
            await message.channel.send(embed=embed)
        elif message.content == "fptoken":
            floor_price = await self.get_onchain_heroes_token_price()
            embed = discord.Embed(
                title="OCH Genesis Token Price",
                description=f"",
                color=discord.Color.blue()  # You can choose any color
            )
            embed.add_field(name="Token Price", value=f'{floor_price} USD', inline=False)
            embed.set_image(url="https://docs.onchainheroes.xyz/~gitbook/image?url=https%3A%2F%2F1697034096-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FJpx9ur3CmOkW7hy40mdH%252Fuploads%252FzbrD7jM5R47Qsc0TkqdK%252Fcoin-export%2520%282%29.gif%3Falt%3Dmedia%26token%3D527ed4e6-ca39-481a-a1c1-758cd88e88a9&width=768&dpr=4&quality=100&sign=b90031a0&sv=2")
            embed.set_footer(text="Made by poosox -- RNs Copyright Ⓒ 2025 ")
            await message.channel.send(embed=embed)
        elif  message.content == "fphero":
            floor_price = await self.get_hero_floor()
            embed = discord.Embed(
                title="OCH Genesis Token Price",
                description=f"",
                color=discord.Color.blue()  # You can choose any color
            )
            embed.add_field(name="Token Price", value=f'{floor_price} ETH ', inline=False)
            embed.set_image(url="https://img.reservoir.tools/images/v2/abstract/hc%2BnPcLmWxs%2FDW99DlBQ42k40ZoyYV5jCIms5qHjwvuCBlT9hjArlF9SVfnB1z2uVgIfYdFxQI46t7gMxjihHgClMKcGroM4pwE6C3Sc0%2B%2B1gpBDgBrIPO6qtFUZ1sVHZiJcBva1z9qIU5V1iKsz%2BaH0c4VGE%2BXRMxmJmTa9Shit1QPlvZuvw4s%2F%2Bgs0d6vf.gif")
            embed.set_footer(text="Made by poosox -- RNs Copyright Ⓒ 2025 ")
            await message.channel.send(embed=embed)
        elif message.content == "fpall":
            floor_price_hero = await self.get_hero_floor()
            floor_price_ring = await self.get_onchain_heroes_ring_floor_price()
            floor_price_token = await self.get_onchain_heroes_token_price()
            embed = discord.Embed(
                title="On Chain Hero Prices",
                description=f"[Magic Eden](https://magiceden.us/collections/abstract/0x7c47ea32fd27d1a74fc6e9f31ce8162e6ce070eb)",
                color=discord.Color.blue()  # You can choose any color
            )
            embed.add_field(name="Hero Price", value=f'{floor_price_hero} ETH ', inline=True)
            embed.add_field(name="Ring Price", value=f'{floor_price_ring/10**18:.2f} ETH ', inline=True)
            embed.add_field(name="Token Price", value=f'{floor_price_token} USD ', inline=True)
            embed.set_image(url="https://img.reservoir.tools/images/v2/abstract/hc%2BnPcLmWxs%2FDW99DlBQ42k40ZoyYV5jCIms5qHjwvuCBlT9hjArlF9SVfnB1z2uVgIfYdFxQI46t7gMxjihHgClMKcGroM4pwE6C3Sc0%2B%2B1gpBDgBrIPO6qtFUZ1sVHZiJcBva1z9qIU5V1iKsz%2BaH0c4VGE%2BXRMxmJmTa9Shit1QPlvZuvw4s%2F%2Bgs0d6vf.gif")
            embed.set_footer(text="Made by poosox -- Copyright Ⓒ 2025 RNs  ")
            messagee = await message.reply(embed=embed)
            await messagee.add_reaction("🗑️")
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == "🗑️" and reaction.message.id == messagee.id

            # Wait for the user to react to the message
            reaction, user = await self.wait_for('reaction_add', check=check)

            # Delete the message after the user reacts
            await messagee.delete()
            print(f"Message deleted by {user.name}")


    async def get_onchain_heroes_ring_floor_price(self):
        api_key = 'key'  # Replace with your SimpleHash API key
        contract_address = '0x8e02d1e68Dff0dCEBf1CDE4eE5f60f1D5A499B1e'
        

        url = f'https://api.simplehash.com/api/v0/nfts/ethereum/{contract_address}?limit=1'
        headers = {'X-API-KEY': api_key,
                'Accept': 'application/json'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            #print(data)  # Print the entire response to check the data structurec
            floor_price = data['nfts'][0]['collection']['floor_prices'][0]['value']
            if floor_price is not None:
                return floor_price
            else:
                return 'Floor price not available'
        else:
            return f'Error: {response.status_code}'
        
    async def get_onchain_heroes_token_price(self):
        api_key = 'keymx'  # Replace with your SimpleHash API key
        
        

        url = f'https://api.simplehash.com/api/v0/fungibles/assets?fungible_ids=abstract.0x33EE11cE309854a45B65368C078616ABcb5c6e3d&include_prices=1'
        headers = {'X-API-KEY': api_key,
                'Accept': 'application/json'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            #print(data)  # Print the entire response to check the data structurec
            floor_price = data['prices'][0]['value_usd_string']
            if floor_price is not None:
                return floor_price
            else:
                return 'Floor price not available'
        else:
            return f'Error: {response.status_code}'
        
    async def get_hero_floor(self):
                # URL of the NFT collection on Magic Eden
        url = "https://magiceden.us/collections/abstract/0x7c47ea32fd27d1a74fc6e9f31ce8162e6ce070eb"

        # Headers to mimic a real browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # Send request to the page
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the meta tag containing the og:image property
            meta_tag = soup.find("meta", property="og:image")

            if meta_tag:
                content = meta_tag["content"]
                # Extract the data query parameter
                parsed_url = urllib.parse.urlparse(content)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                data_encoded = query_params.get("data", [""])[0]

                if data_encoded:
                    # Decode the base64 encoded JSON
                    import base64
                    data_decoded = base64.b64decode(data_encoded).decode("utf-8")
                    data_json = json.loads(data_decoded)

                    # Find the floor price
                    floor_price_data = next(
                        (item for item in data_json["bigStats"] if item["trait_type"] == "FLOOR PRICE"),
                        None,
                    )

                    if floor_price_data:
                        floor_price = floor_price_data["value"]
                        return floor_price
                    else:
                        return "Floor price data not found."
                else:
                    print("Data parameter not found in URL.")
            else:
                print("Meta tag with og:image property not found.")
        else:
            print("Failed to fetch the webpage. Status code:", response.status_code)
                
# Example usage

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run('DISCORD TOKEN') #put discord bot token
