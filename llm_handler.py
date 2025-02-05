import os
from dotenv import load_dotenv
from openai import AzureOpenAI

from pdf_manager import read_page
from collections import deque



userHistory={}


def clearPrevBookSummary(chatid):
    userHistory[chatid].clear()

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
    # Ensure user history exists
    if userHistory.get(chatid) is None:
        userHistory[chatid] = deque(maxlen=5)

    data = read_page(chatid=chatid)

    summarize_text = "".join(userHistory[chatid])

    messages = [
        {
            "role": "system",
            "content": "You are a system design expert. Your job is to summarize system design papers. Each time you receive a page, summarize it up to 2/4 of the original content. Explain in simple terms, and use emojis if required."
        },
        {
            "role": "user",
            "content": data
        },
        {
            "role": "user",
            "content": "Previous page summary for context -> " + summarize_text
        }
    ]

    # Send request to LLM
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
    userHistory[chatid].append(response_message)

    return response_message

    

def handleUserPrompt(chatid, userprompt):
    # Initialize user history if not present
    if userHistory.get(chatid) is None:
        userHistory[chatid] = deque(maxlen=5)

    # Efficient summarization accumulation
    summarize_text = "".join(userHistory[chatid])

    # Handle empty history scenario
    if not summarize_text:
        summarize_text = "(There is no interaction. Please start some paper to discuss further.)"

    messages = [
        {
            "role": "system",
            "content": "You are a system design expert. You were summarizing some system design paper, and suddenly the user asked a question or query.if the user ask for go ahead or move to next page basically a sentencte that results in this way in that case tell them to type /next. This is the summary of the paper so far: " + summarize_text
        },
        {
            "role": "user",
            "content": userprompt
        }
    ]

    # Send request to the LLM
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

    return response_message