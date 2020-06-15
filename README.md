# MQTT Slackbot
Takes MQTT messages with url's and posts to Slack e.g. OneDrive/Google Drive/Dropbox links

### Environment variables
Pass the following environment vairables to execution environment
| Settings | Description | Inputs |
| :----: | --- | --- |
| `MQTT_BROKER` | MQTT Broker address | `mqtt.test.local` |
| `MQTT_PORT` | MQTT Broker port | `1883` |
| `MQTT_SUB_TOPIC` | MQTT Topic to subscribe to | `test/messages` ||
| `SLACK_TOKEN` | Slack API Token | `SoMeSeCrEt988766553` |

### Requirements
```sh
pip install -p requirements.txt
```

### Execution 
```sh
python3 .\main.py
```

### Docker Compose
```sh 
mqttslackbot:
    image: stuartgraham/mqttslackbot
    container_name: mqttslackbot
    environment:
        - MQTT_BROKER=mqtt.test.local
        - MQTT_PORT=1883
        - MQTT_SUB_TOPIC=test/messages
        - SLACK_TOKEN=SoMeSeCrEt988766553
    volumes:
        - input-storage:/app/input:ro
    restart: always
```