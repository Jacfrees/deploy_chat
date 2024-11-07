import json

import requests
from requests.auth import HTTPBasicAuth

account_sid = 'ACc22482bf6b5e85130e94e1970550eea3'
auth_token = '9984f6563cd0cf370cb09c84c6576699'


def sendMessageTwilio(from_number, response):
    resp_message = {
        "To": from_number,
        "From": "whatsapp:+14155238886",
        "Body": response
    }
    requests.post('https://api.twilio.com/2010-04-01/Accounts/' + account_sid + '/Messages.json',
                  data=resp_message,
                  auth=(account_sid, auth_token))


def sendMessageTwilioWithTemplate(from_number, sid):
    resp_message = {
        "To": from_number,
        "From": "whatsapp:+14155238886",
        "ContentSid": sid,
    }

    response = requests.post(
        'https://api.twilio.com/2010-04-01/Accounts/' + account_sid + '/Messages.json',
        data=resp_message,
        auth=(account_sid, auth_token)
    )
    return response.status_code, response.json()


def update_list_projects(projects, sid_list_projects):
    items = []
    for index, project in enumerate(projects, start=1):
        item = {
            "item": project['name'],
            "description": "Código: " + project['code'],
            # "id": project['code']
            "id": str(index)
        }
        items.append(item)
    payload = {
        "friendly_name": "list_projects",
        "language": "es",
        "types": {
            "twilio/list-picker": {
                "body": "Por favor selecciona un proyecto",
                "button": "Seleccionar proyecto",
                "items": items
            }
        }
    }
    payload_json = json.dumps(payload)
    url = 'https://content.twilio.com/v1/Content'
    auth = HTTPBasicAuth('ACc22482bf6b5e85130e94e1970550eea3', '9984f6563cd0cf370cb09c84c6576699')
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, auth=auth, data=payload_json)
    response_json = response.json()
    sid = response_json.get('sid')
    print("SID:", sid)
    sid_list_projects = sid
    return sid_list_projects
