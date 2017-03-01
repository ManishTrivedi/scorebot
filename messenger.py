from flask import Flask, request
import os
import json
import sys
import requests
#from wit_client import parse_text
from wit import Wit
 
app = Flask(__name__)

#This is the access token we get when we create the bot
PAGE_ACCESS_TOKEN = "EAAR9DLZC03VoBADAV7pIUYkYp3yuZB1T53S6ZB7p6UNEmGwg3vN6vJyhPovs5JEi4NAysrVsAVpXc5ZCyWp3cOyydFUc5INmyLXrV1ZBkNvcKKyPbdenl587454dxDG93FEyEWNNhtMquPxUiCEkv7IXu5lZCBlaGaeKRIvpH8nwZDZD"
#Verification token which we mention when giving the url 
VERIFY_TOKEN='secret' 
ID=''

############ WIT LOGIC ####################

def send(request, response):
    recepient_id = request['session_id']
    send_message(ID, str(response['text']))

def getScore(request):
    print('In score')
    context = request['context']
    entities = request['entities']

    if not entities.get('intent', None):
        context['missingIntent'] = True
    elif entities.get('teamname', None):
        context['result'] = '2-1'
    else:
        context['missingTeam'] = True   
    #print(context)
    return context

def getFixture(request):
    print('In fixture')
    context = request['context']
    entities = request['entities']

    context['game'] = 'Arsenal'
    #print(context)
    return context    


actions = {
    'send' : send,
    'getScore' : getScore,
    'getFixture' : getFixture
}   

client = Wit(access_token='REPASDYTEYYSAPQ5477TGMP7VZ2KHDRX', actions=actions)

#############################################################

@app.route('/man/', methods=['GET'])
def test():
    return "Hello Manish", 200

#method that handles verification from facebook
@app.route('/', methods=['GET'])
def handle_verification():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
  
#Respond back to facebook messenger
def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
 
#Receive messages from fb messenger 
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    #log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    global ID
                    ID=sender_id
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    context0={}
                    context1 = client.run_actions('session1', text, context0)
                    print("{0} is context after run actions".format(context1))
                    #send_message(sender_id, wit_response)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200
 
def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=True)