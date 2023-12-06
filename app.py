from flask import Flask, request, jsonify
from flask_cors import CORS
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-07-01-preview' # this may change in the future

# Replace these variables with your Azure Storage account details
account_name = os.getenv("STRG_ACCOUNT_NAME")
account_key = os.getenv("STRG_ACCOUNT_KEY")
container_name = 'output-content'

deployment_name='gpt35' #This will correspond to the custom name you chose for your deployment when you deployed a model. 


app = Flask(__name__)
CORS(app) 




    
@app.route('/explain', methods=['POST'])
def explain():
    try:
        data = request.get_json()
        text_content = data.get('text_content')

        # Read from prompt.txt
        with open('prompt.txt', 'r') as file:
            additional_prompt = file.read()

        prompt = f'You are a code assistant who can explain code. Here is some code: "{text_content}" can you explain what it does? {additional_prompt}'

        response = openai.ChatCompletion.create(
        engine="gpt35-turbo-latest",
        messages = [{"role":"system","content":"You are an AI assistant that helps understand what is on archived news video tapes"},
                    {"role":"user","content":prompt}],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False)

        return jsonify({'explain': response.choices[0].message.content}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
