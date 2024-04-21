from aiokafka import AIOKafkaConsumer
import logging
from typing import Callable


class KafkaConsumer:

    def __init__(self, config):
        """
        :param config: config for init AIOKafkaConsumer
        """
        self._config = config
        self._topic = None
        self._kafka_consumer: AIOKafkaConsumer = None
        self._callback_function: Callable = None

    async def init_consumer(self, topic, callback_function: Callable):
        """
        :param topic: topic name for subscription
        :param callback_function: function to execute after receiving a message
        """
        self._topic = topic
        self._callback_function = callback_function
        self._kafka_consumer = AIOKafkaConsumer(self._topic, **self._config)

    async def stop(self):
        logging.info('KAFKA CONSUME STOP')
        return await self._kafka_consumer.stop()

    async def consume(self):
        logging.info('KAFKA CONSUME START')
        if not self._topic or not self._callback_function or not self._kafka_consumer:
            raise Exception('KafkaConsumer must be initialized.')

        await self._kafka_consumer.start()
        logging.info('KAFKA CONSUME STARTED')

        try:
            logging.info('KAFKA TRYING TO EXTRACT MESSAGE')
            async for msg in self._kafka_consumer:
                logging.info('MESSAGE FOR %s', msg)
                await self._callback_function(msg)
        finally:
            await self._kafka_consumer.stop()
