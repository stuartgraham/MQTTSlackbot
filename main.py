import paho.mqtt.client as paho
import time
import os
import json
import datetime
import logging
import slack

# .ENV FILE FOR TESTING
#if os.path.exists('.env'):
#    from dotenv import load_dotenv
#    load_dotenv()

# GLOBALS
MQTT_BROKER = os.environ.get('MQTT_BROKER','')
MQTT_PORT = int(os.environ.get('MQTT_PATH', 1883))
MQTT_PUB_TOPIC = os.environ.get('MQTT_PUB_TOPIC','')
MQTT_SUB_TOPIC = os.environ.get('MQTT_SUB_TOPIC','')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN','')
INPUT_PATH = os.environ.get('INPUT_PATH','input')

BASE_DIR = os.getcwd()
INPUT_PATH = os.path.join(BASE_DIR, INPUT_PATH)

def post_to_slack(image, confidence, category):
    if confidence > 0.8:
        image = os.path.join(INPUT_PATH, image)
        client = slack.WebClient(token=SLACK_TOKEN)
        comment = "Confidence {}, Category {}".format(confidence, category)
        response = client.files_upload(
            file=image,
            initial_comment=comment,
            channels='#cctv'
        )
        assert response['ok']
        slack_file = response['file']
        logging.info(slack_file)

# SUB MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
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
    image = message['image']
    logging.debug("json_image : {}".format(str(image)))
    post_to_slack(image, confidence, category)

def main():
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info("STARTING MQTT Slackbot")
    client = paho.Client("mqtt-slackbot")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

# Main Exectution
main()
