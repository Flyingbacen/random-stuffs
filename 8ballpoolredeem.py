import asyncio
import aiohttp

"""
I just copied this over from the discord bot, and I was lazy so I kept the aiohttp and async.
"""

async def yes():
    userid = input("Enter your 8 Ball Pool User ID: ")
    async with aiohttp.ClientSession() as session:
        async def get_free_cue_sku(user_id, category_wildcard):
            url = f'https://8ballpool.com/api/items?userId={user_id}'

            try:
                async with session.get(url) as response:
                    response.raise_for_status()  # Check for HTTP errors

                    data = await response.json()
                    items = data.get('items', [])

                    for item in items:
                        if category_wildcard in item.get('category', ''):
                            return item.get('sku')

            except aiohttp.ClientError as e:
                return None

        async def redeem_free_cue(user_id, sku):
            url = 'https://8ballpool.com/api/claim'
            headers = {'content-type': 'application/json'}
            payload = {
                "user_id": str(user_id),
                "sku": sku
            }

            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    response.raise_for_status()

                    print(f"Redemption response status code: {response.status}")

                    if response.status == 200:
                        return True
                    else:
                        return response.status

            except aiohttp.ClientError as e:
                print(f"Error during redemption: {e}")

        user_id = userid
        category_wildcard = 'free_daily_cue_piece'

        # Retrieve SKU for the free piece
        free_cue_sku = await get_free_cue_sku(user_id, category_wildcard)
        if free_cue_sku:
            print(f"SKU for the free cue piece: {free_cue_sku}")

            # Redeem the free cue piece
            cue_StatusCode = await redeem_free_cue(user_id, free_cue_sku)
            if cue_StatusCode == True:
                print(f"Successfully redeemed today's cue piece\n\t\t~~||sku:{free_cue_sku}||~~")
            else:
                print(f"Error redeeming today's cue piece.\nStatus code:\n\t{cue_StatusCode}")
        else:
            print(f"Failed to retrieve SKU for the free cue piece with category wildcard: {category_wildcard}.")

asyncio.run(yes())