import asyncio
import httpx
import json

bot_token = "6801709437:AAHVDUJK8844rFOarZxUWhVlpenkOKQDS6U"  # Make sure to replace this with your actual bot token


async def listen_message_telegram(tl_user_message):
    last_update_id = None 

    async with httpx.AsyncClient() as client:
        while True:
            print("Waiting for message...")
            await asyncio.sleep(1)
            url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
            params = {'offset': last_update_id} if last_update_id else {}

            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                updates = response.json()

                if 'result' in updates and updates['result']:
                    for update in updates['result']:
                        last_update_id = update['update_id'] + 1
                        input_message = {
                            "user_message": update
                        }
                        print(f"\nGET USER MESSAGE INPUT: {json.dumps(input_message, indent=4)}")
                        tl_user_message.append(input_message)
                        print("Collected in the |request_list|")
                        await asyncio.sleep(1)  # Simulate delay in collecting messages
                else:
                    print("No new updates.")
            except httpx.HTTPStatusError as exc:
                print(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            except Exception as exc:
                print(f"An error occurred: {exc}")

# Example usage
async def main():
    tl_user_message = []
    await listen_message_telegram(tl_user_message)

# To run the async main function
if __name__ == '__main__':
    asyncio.run(main())