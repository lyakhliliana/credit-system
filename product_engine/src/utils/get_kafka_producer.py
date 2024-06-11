import asyncio
import os

from aiokafka import AIOKafkaProducer

event_loop = asyncio.get_event_loop()
kafka = os.getenv('KAFKA_INSTANCE')
produce_topic = os.getenv('TOPIC_NAME_AGREEMENTS')


class AgreementProducer(object):
    def __init__(self):
        self.__producer = AIOKafkaProducer(loop=event_loop, bootstrap_servers=kafka)
        self.__produce_topic = produce_topic

    async def start(self) -> None:
        await self.__producer.start()

    async def stop(self) -> None:
        await self.__producer.stop()

    async def send(self, value: bytes) -> None:
        await self.start()
        try:
            await self.__producer.send(
                topic=self.__produce_topic,
                value=value,
            )
        finally:
            await self.stop()


def get_producer() -> AgreementProducer:
    return AgreementProducer()

