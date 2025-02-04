import os
from dotenv import load_dotenv
from openai import AzureOpenAI

from pdf_manager import read_page
from collections import deque

fixed_size_queue = deque(maxlen=5)


load_dotenv()

endpoint = os.getenv("ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
deployment = os.getenv("DEPLOYMENT")

client = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint=endpoint,
    api_key=api_key
)

def interaction(chatid):
    
    data=read_page(chatid=chatid)
    
    sumarize_text=""
    for item in fixed_size_queue:
        sumarize_text+=item
          
    messages = [
        {
            "role": "system",
            "content": "You are a system design expert. Your job is to summarize system design papers. Each time you receive a page, summarize it up to 2/4 of the original content.you must explain in as much easier language and use some emojis if required"
        },
        {
            "role":"user",
            "content":data
        },
        {
            "role":"user",
            "content":"previous page summary to provide the context of what have been discussed->"
        }
    ]
    
    # Send initial request to the LLM
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
    )
    response_message = completion.choices[0].message.content
    fixed_size_queue.append(response_message)

    return response_message

   
 
