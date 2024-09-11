import asyncio
import websockets
import json
import requests
from datetime import datetime
import math

# Webhook URL
webhook_url = 'YOUR WEBHOOK URL'
count = 0

async def subscribe():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        try:
            # Subscribing to new token events
            payload = {
                "method": "subscribeNewToken",
            }
            await websocket.send(json.dumps(payload))

            # Listening for messages
            async for message in websocket:
                data = json.loads(message)
                global count
                global count2
                
                if count == 0:
                    print("Started")
                else:
                    api_url = data.get('uri')
                    response2 = requests.get(api_url)
                    data2 = json.loads(response2.text)

                    name = data2.get('name')
                    symbol = data2.get('symbol')
                    description = data2.get('description')
                    image = data2.get('image')
                    twitter = data2.get('twitter')
                    telegram = data2.get('telegram')
                    website = data2.get('website')

                    mint = data.get('mint')
                    mcap = data.get('marketCapSol')
                    mcap2 = math.ceil(mcap)
                    link = f"https://pump.fun/{mint}"

                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

                    response3 = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd')
                    data = response3.json()
                    solana_price = data['solana']['usd']
                    mcap_usd = mcap2 * solana_price
                    mcap_usd2 = math.ceil(mcap_usd)

                    message_content = f"**Mint:** {mint}\n**Symbol:** {symbol}\n**Marketcap:** {mcap_usd2}$\n**Description:** {description}\n **Twitter:** {twitter}\n **Telegram:** {telegram}\n **Website:** {website}\n \n Clich [**__HERE__**]({link}) to open on pump.fun\nMade by TheSolyboy"

                    embed = {
                        "title": f"{name} created on pump.fun",
                        "description": message_content,
                        "color": 0x932adb,  
                        "thumbnail": {
                            "url": image
                        },
                        "footer": {
                            "text": formatted_time,
                        }
                    }

                
                    payload = {
                        'embeds': [embed],
                        'username': 'Coin Scanner',
                        'avatar_url': 'https://cdn.discordapp.com/attachments/1257057484083040286/1257073132380885084/image.png?ex=66e20016&is=66e0ae96&hm=57e2e22e76f2e3db1c0140fc644e09df991c2d22aff7337c99965f127026e202&'
                    }

                    response = requests.post(webhook_url, json=payload)

                    if response.status_code == 204:
                        print(name)
                        print("Sent message successfully")
                        print(formatted_time)
                    else:
                        print(f'Failed to send message. Status code: {response.status_code}')
                        print('Response:', response.text)
                print("-------------------")
                count = 2

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(subscribe())
