import asyncio
import os

from common.kafka_managers.consumer import KafkaConsumer
from common.kafka_managers.producer import KafkaProducerSession

event_loop = asyncio.get_event_loop()
kafka = os.getenv('KAFKA_INSTANCE')
CONFIG = {'bootstrap_servers': kafka, 'loop': event_loop}
CONFIG_GROUP = {'bootstrap_servers': kafka,
                'loop': event_loop,
                'group_id': 'group_from_pe',
                'auto_commit_interval_ms': 10000,
                'auto_offset_reset': "earliest"}

kafka_producer_agreements = KafkaProducerSession(CONFIG)
kafka_consumer_scoring_responses = KafkaConsumer(CONFIG_GROUP)
