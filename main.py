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
                
                if count == 0:
                    print("Started")
                else:
                    try:
                        # Ensure the 'uri' field is present and valid
                        api_url = data.get('uri')
                        if not api_url:
                            print("Error: 'uri' field is missing or None. Skipping this iteration.")
                            continue  # Skip to the next message if 'uri' is missing

                        response2 = requests.get(api_url)
                        data2 = json.loads(response2.text)

                        name = data2.get('name', 'Unknown Name')
                        symbol = data2.get('symbol', 'Unknown Symbol')
                        description = data2.get('description', 'No description available')

                        # Ensure valid URLs or set to default if None
                        image = data2.get('image') if data2.get('image') else "https://defaultimage.url"
                        twitter = data2.get('twitter') if data2.get('twitter') else "No Twitter available"
                        telegram = data2.get('telegram') if data2.get('telegram') else "No Telegram available"
                        website = data2.get('website') if data2.get('website') else "No Website available"

                        mint = data.get('mint', 'Unknown Mint')
                        mcap = data.get('marketCapSol', 0)
                        mcap2 = math.ceil(mcap)
                        link = f"https://pump.fun/{mint}"

                        current_time = datetime.now()
                        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

                        # Error handling for the CoinGecko API request
                        try:
                            response3 = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd')
                            data = response3.json()
                            solana_price = data['solana']['usd']
                            mcap_usd = mcap2 * solana_price
                            mcap_usd2 = math.ceil(mcap_usd)
                        except (KeyError, requests.exceptions.RequestException) as e:
                            print(f"Error fetching Solana price: {e}. Skipping this iteration.")
                            solana_price = 0
                            mcap_usd2 = 0

                        message_content = (
                            f"**Mint:** {mint}\n"
                            f"**Symbol:** {symbol}\n"
                            f"**Marketcap:** {mcap_usd2}$\n"
                            f"**Description:** {description}\n"
                            f"**Twitter:** {twitter}\n"
                            f"**Telegram:** {telegram}\n"
                            f"**Website:** {website}\n\n"
                            f"Click [**__HERE__**]({link}) to open on pump.fun"
                        )

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
                    except Exception as e:
                        print(f"An error occurred while processing data: {e}")
                
                print("-------------------")
                count = 2

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e  # Rethrow the exception to restart the connection

async def main():
    while True:
        try:
            await subscribe()
        except Exception as e:
            print(f"Connection failed, retrying in 5 seconds. Error: {e}")
            time.sleep(5)  # Wait 5 seconds before retrying

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Fatal error, restarting program: {e}")
            time.sleep(5)  # Wait 5 seconds before restarting the main loop
