"""
This file uses the OpenAI API functions to generate a response to the user's message.
"""
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os, time
import asyncio

load_dotenv()
# Open AI API_key and assistant id
open_ai_api_key = os.getenv("OPENAI_API_KEY")
open_ai_assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

client = AsyncOpenAI(api_key=open_ai_api_key)

class Assistant:
    def __init__(self, client, openai_assistant_id):
        self.client = client
        self.assistant_id = openai_assistant_id
        self.thread_id = None
        self.run_id = None

    async def new_thread(self):
        if self.thread_id:
            my_thread = await self.client.beta.threads.retrieve(self.thread_id)  # getting thread
            print(f"Current thread: \t\t|{my_thread.id}|\n")
        else:
            empty_thread = await self.client.beta.threads.create()
            self.thread_id = empty_thread.id
            print(f"Thread created: \t\t\t|{self.thread_id}|\n")
            return self.thread_id
    
    async def new_message(self, user_message):
        thread_message = await self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=user_message
        )
        user_message = thread_message.content[0].text.value
        print(f"Adding a user message into a thread... |{self.thread_id}|")
        return user_message
    
    async def new_run(self):
        run = await self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            temperature=1
        )
        self.run_id = run.id
        print(f"\nRun Created \t\t- \t|{self.run_id}|")

    async def retrieve_run(self):
        while True:
            run = await self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, 
                run_id=self.run_id,
            )
            print(f"\nAssistant |{self.assistant_id}| processing your request.")

            if run.status == "completed":
                time_calc = run.completed_at - run.created_at
                time_taken = time.strftime("%H:%M:%S", time.gmtime(time_calc))

                print(f"\n_______________RESULTS__________________")
                print(f"Processing completed in: \t{time_taken}")
                print(f"Prompt Tokens used: \t\t{run.usage.prompt_tokens} \nCompletion Tokens used: \t{run.usage.completion_tokens} \nTotal Tokens used: \t\t{run.usage.total_tokens}\n")
                break

            if run.status == "in_progress":
                print("In progress... please wait")
            elif run.status == "canceled":
                print("Your request was canceled for some reason.")
                break
            elif run.status == "failed":
                print("Something went wrong. Please repeat the request.")
                break
            elif run.status == "expired":
                print("Your request has expired.")
                break

            await asyncio.sleep(5)

    async def list_messages(self):
        messages = await self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        last_message = messages.data[0].content[0].text.value

        print("\n<<<CHAT HISTORY>>>\n")
        # async handle_message doing this job.   
        for message in reversed(messages.data):
            print(f"{message.role}: {message.content[0].text.value:<20}")

        return last_message        