import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage

# Load environment variables from .env file
load_dotenv()
lite_llm_endpoint = os.getenv("lite_llm_endpoint")
api_key = os.getenv("api_key")

def invoke(system_prompt, user_prompt):
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
                    UserMessage(content=user_prompt)
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
    return response.choices[0].message.content
