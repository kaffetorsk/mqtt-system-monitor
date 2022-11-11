[![CodeQL](https://github.com/kaffetorsk/mqtt-system-monitor/actions/workflows/codeql.yml/badge.svg)](https://github.com/kaffetorsk/mqtt-system-monitor/actions/workflows/codeql.yml)

# mqtt-system-monitor
Small python script that reads basic hardware performance and publishes it as JSON to an MQTT broker.

## Usage
Config through environment variables, if `.env` is present it will be checked for variables.
### Required
```
MQTT_BROKER: IP address of MQTT broker
```
### Optional
```
MQTT_TOPIC: stats will be published to this topic. (default: device/server/stats)
MQTT_RECONNECT_INTERVAL: Wait this amount before retrying connection to broker (in seconds) (default: 5)
STATUS_INTERVAL: Time between published status messages (in seconds) (default: 5)
PARTITIONS: List of partitions to monitor (default: ['/'])
NVIDIA_GPU: Monitor GPU? (default: True)
DEBUG: True enables full debug (default: False)
```
### Running
```
python main.py
```
or
```
docker run -d --env-file .env kaffetorsk/mqtt-system-monitor
```

## Notes
This repo is in early development, treat it as such and feel free to submit PRs.
