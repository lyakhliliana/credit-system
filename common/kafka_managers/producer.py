from aiokafka import AIOKafkaProducer

import contextlib
import json


class KafkaProducerSession:

    def __init__(self, config):
        """
        :param config: config for init AIOKafkaConsumer
        """
        self._config = config
        self._kafka_producer: AIOKafkaProducer = None

    async def init_producer(self):
        self._kafka_producer = AIOKafkaProducer(**self._config)
        await self.start()

    async def start(self) -> None:
        await self._kafka_producer.start()

    async def stop(self) -> None:
        await self._kafka_producer.stop()

    @contextlib.asynccontextmanager
    async def session(self) -> AIOKafkaProducer:
        if not self._kafka_producer:
            raise Exception('KafkaProducerSession must be initialized.')

        yield self._kafka_producer


async def send_message(producer: AIOKafkaProducer, topic: str, value=None):
    return await producer.send(topic, json.dumps(value).encode('ascii'))
