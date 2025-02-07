import json

import requests
from google.cloud import vision
from google.oauth2 import service_account
from config import CREDENTIALS_FILE, LANGFLOW_API_URL, APPLICATION_TOKEN

# Initialize Google Cloud Vision client
try:
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    vision_client = vision.ImageAnnotatorClient(credentials=credentials)
except Exception as e:
    raise Exception(f"Error initializing Google Cloud Vision client: {e}")

# Function to call Langflow API
def langflow_api_request(prompt):
    try:
        url = f"{LANGFLOW_API_URL}/lf/171b7c20-8dee-4729-922d-81546c6617cb/api/v1/run/ff3639bf-2e6b-43bd-ae35-0a58d34035c0?stream=false"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {APPLICATION_TOKEN}'
        }
        data = {
            "input_value": prompt,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": {
                "ChatInput-S1SYL": {},
                "ParseData-Ni5tY": {},
                "Prompt-yc56u": {},
                "SplitText-VtuDa": {},
                "OpenAIModel-jCJyT": {},
                "ChatOutput-NJYG0": {},
                "AstraDB-KAVqu": {},
                "OpenAIEmbeddings-ATX0Q": {},
                "AstraDB-BDoeE": {},
                "OpenAIEmbeddings-q5ztU": {},
                "File-KGxcR": {}
            }
        }

        # Make the API request
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # Extract the desired nested text response
            response_data = response.json()
            text = response_data["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
            return text
        else:
            return f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Langflow API Error: {e}"
