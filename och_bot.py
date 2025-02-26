import requests
import discord


class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content == 'ringfp':
            floor_price = await self.get_onchain_heroes_floor_price()
            embed = discord.Embed(
                title="OCH Genesis Ring",
                description=f"JIMMY IS BROKE LOL",
                color=discord.Color.blue()  # You can choose any color
            )
            embed.add_field(name="Floor Price", value=f'{floor_price/10**18:.2f} ETH', inline=False)
            embed.set_image(url="https://raw.seadn.io/files/9637918b237c511371d10ba1243d19a5.gif")
            await message.channel.send(embed=embed)
        

    async def get_onchain_heroes_floor_price(self):
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

# Example usage


intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run('bot token')#replace with the token of your bot
