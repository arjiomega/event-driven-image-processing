import json
from urllib.parse import unquote

import pika
from celery import Celery

from core.config import get_settings

settings = get_settings()

TASK_NAME = "worker.tasks.image_processing.process_image"
celery_client = Celery(broker=settings.celery_broker_url)


def on_message(channel, method, properties, body):
    event = json.loads(body)

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        storage_key = unquote(record["s3"]["object"]["key"])
        event_name = record["eventName"]

        print(f"Received event: {event_name} for {bucket}/{storage_key}")

        celery_client.send_task(
            TASK_NAME,
            kwargs={"storage_key": storage_key, "bucket": bucket},
        )

    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.amqp_host,
        ),
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=settings.amqp_exchange,
        exchange_type=settings.amqp_exchange_type,
        durable=True,
    )
    result = channel.queue_declare(
        queue=settings.amqp_queue,
        durable=True,
    )
    queue_name = result.method.queue
    channel.queue_bind(exchange=settings.amqp_exchange, queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message)
    print("Waiting for MinIO events...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
