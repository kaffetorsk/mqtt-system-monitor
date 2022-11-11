from decouple import config
import asyncio
import logging
import psutil
from nvitop import Device
import json
import asyncio_mqtt as aiomqtt

# Read config from ENV
MQTT_BROKER = config('MQTT_BROKER', default=None)
MQTT_TOPIC = config('MQTT_TOPIC', default='device/server/stats')
MQTT_RECONNECT_INTERVAL = config('MQTT_RECONNECT_INTERVAL', default=5)
STATUS_INTERVAL = config('STATUS_INTERVAL', default=5, cast=int)
PARTITIONS = config('PARTITIONS', default=['/'])
NVIDIA_GPU = config('NVIDIA_GPU', default=True, cast=bool)
DEBUG = config('DEBUG', default=False, cast=bool)

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

GPU = Device(index=0) if NVIDIA_GPU else None


def get_disk_usage():
    return {d: psutil.disk_usage(d).percent for d in PARTITIONS}


def get_gpu_usage():
    return {
        "gpu_utilization": GPU.gpu_utilization(),
        "enc_utilization": GPU.encoder_utilization(),
        "dec_utilization": GPU.decoder_utilization(),
        "memory_usage": GPU.memory_percent()
        }


async def listen_stats():
    while True:
        status = {
            "cpu_utilization": psutil.cpu_percent(),
            "mem_usage": psutil.virtual_memory().percent,
            "disk_usage": get_disk_usage()
            }
        if GPU:
            status['gpu'] = get_gpu_usage()
        yield status
        await asyncio.sleep(STATUS_INTERVAL)


async def mqtt_client():
    while True:
        try:
            async with aiomqtt.Client(MQTT_BROKER) as client:
                logging.info(f"MQTT client connected to {MQTT_BROKER}")
                async for status in listen_stats():
                    await client.publish(
                        MQTT_TOPIC,
                        payload=json.dumps(status)
                        )
        except aiomqtt.MqttError as error:
            logging.info(f'MQTT "{error}". reconnecting.')
            await asyncio.sleep(MQTT_RECONNECT_INTERVAL)


async def main():
    await asyncio.gather(mqtt_client())


while True:
    try:
        asyncio.run(main())
    except RuntimeError:
        logging.info("Closed.")
        break
