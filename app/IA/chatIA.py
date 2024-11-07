import boto3
import json

def get_bedrock_response(question):
    session = boto3.Session(
    aws_access_key_id='AKIAXIGQUWDADME3ADOI',
    aws_secret_access_key='Z8dVP1Ryau6EwBUEP0ALC77M31UPgv8IfzXNIngB',
    region_name='us-east-1'  # example: 'us-west-1'
)

    bedrock = session.client(service_name='bedrock-runtime')

    body = json.dumps({
        "prompt": f"\n\nHuman: {question}\n\nAssistant:",
        "max_tokens_to_sample": 300,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())
    return response_body.get('completion')
