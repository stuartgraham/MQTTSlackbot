import paho.mqtt.client as paho
import time
import os
import json
import datetime
import logging
import slack
import random

# .ENV FILE FOR TESTING
# if os.path.exists('.env'):
#     from dotenv import load_dotenv
#     load_dotenv()

# GLOBALS
MQTT_BROKER = os.environ.get('MQTT_BROKER','')
MQTT_PORT = int(os.environ.get('MQTT_PATH', 1883))
MQTT_SUB_TOPIC = os.environ.get('MQTT_SUB_TOPIC','')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN','')


def post_to_slack(url, confidence, category):
    if confidence > 0.8:
        client = slack.WebClient(token=SLACK_TOKEN)
        url = fix_url_url(url)
        comment = "Confidence : {}%, Category : {}".format(str(confidence*100), category)
        post_message = build_message_block(url, comment)
        logging.debug(comment)
        response = client.chat_postMessage(channel="#cctv", blocks=post_message)
        logging.info(response)


# SUB MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    logging.debug("Listening to  : {}".format(MQTT_SUB_TOPIC)) 
    client.subscribe(MQTT_SUB_TOPIC)

def on_message(client, userdata, msg):
    logging.info("Received : {} convert to json".format(str(msg.payload))) 
    message = msg.payload.decode('utf-8')
    logging.debug("message : {}".format(str(message))) 
    message = json.loads(message)
    category = message['category']
    logging.debug("json_category : {}".format(str(category))) 
    confidence = message['confidence']
    logging.debug("json_confidence : {}".format(str(confidence)))
    url = message['url']
    logging.debug("json_url : {}".format(str(url)))
    post_to_slack(url, confidence, category)


def build_message_block(url, comment):
    message = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": comment
                    }
                    },
                    {
					"type": "image",
					"title": {
						"type": "plain_text",
						"text": "CCTV Analysis"
					},
					"image_url": url,
					"alt_text": "CCTV IMAGE"
				}
            ]
    return message

def fix_url_url(url):
    url = url.replace('dl=0', 'raw=1')
    return url

def main():
    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info("STARTING MQTT Slackbot")
    client = paho.Client("mqtt-slack-bot-" + str(random.randint(100, 999)))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

# Main Exectution
main()
