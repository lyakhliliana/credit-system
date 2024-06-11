import asyncio
import os

from common.kafka_managers.producer import KafkaProducerSession

event_loop = asyncio.get_event_loop()
kafka = os.getenv('KAFKA_INSTANCE')
CONFIG = {'bootstrap_servers': kafka, 'loop': event_loop}

kafka_producer_agreements = KafkaProducerSession(CONFIG)
