from fastapi import FastAPI
from dotenv import load_dotenv
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage
from model_instruction import question_generator
app = FastAPI()

# Load environment variables from .env file
load_dotenv()
lite_llm_endpoint = os.getenv("lite_llm_endpoint")
api_key = os.getenv("api_key")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/{prompt}")
async def get_prompt(prompt: str):
    system_prompt = question_generator(prompt)

    #setting up the Azure OpenAI client for chat completions
    client = ChatCompletionsClient(
        endpoint=f"{lite_llm_endpoint}",
        credential=AzureKeyCredential(api_key),
        api_version="2025-03-01-preview"
    )

    models = ["hack-fest-gpt-5.6-luna"]          # Must match models deployed in AI Foundry

    for model in models:
        try:
            response = client.complete(
                messages=[
                    SystemMessage(content=system_prompt),
                    UserMessage(content=prompt)
                ],
                model=model,
                headers={"Authorization": api_key, }
            )

            print(f"Response from model {model}:\n\r{response.choices[0].message.content}\n\r")
            print(f"#####################################################################\n\r")
        except Exception as e:
            print(f"Error calling model {model}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print(f"Endpoint: {lite_llm_endpoint}")
            print(f"API Key set: {'Yes' if api_key != 'nokey' else 'No - using placeholder'}")
            print(f"Model: {model}")
    return {"message": response.choices[0].message.content}
