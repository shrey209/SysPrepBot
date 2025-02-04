import os
from dotenv import load_dotenv
from openai import AzureOpenAI

Core_memory={}

pastPrompts={}

endpoint=os.getenv("ENDPOINT")
api_key=os.getenv("AZURE_OPENAI_KEY")
deployment=os.getenv("DEPLOYMENT")

client = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint=endpoint,
    api_key=api_key
)


chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an a system design expert your job is to summarize the system design papers each ,time you will get a page and you have to summarize it for the user,you have to shortend it upto 2/3 "
            }
        ]

    },
     {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": page.extract_text()
            }
        ]
        
    }
] 
    
# Include speech result if speech is enabled  
messages = chat_prompt 

completion = client.chat.completions.create(  
    model=deployment,  
    messages=messages,
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,
    stop=None,  
    stream=False  
)  
  
response=completion
print(response.choices[0].message)  
print("ended")