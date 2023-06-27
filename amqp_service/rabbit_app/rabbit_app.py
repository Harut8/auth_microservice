import asyncio
import uuid

from aio_pika import Message
from aio_pika.abc import AbstractConnection, ExchangeType, AbstractIncomingMessage
from service.parser import ParseEnv
import aio_pika


class RabbitMQ:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RabbitMQ, cls).__new__(cls)
        return cls.instance

    @classmethod
    async def connect(cls, vhost):
        __dsn = cls(vhost).dsn
        cls.conn: AbstractConnection = await aio_pika.connect(__dsn)
        print("Connected to RabbitMQ")

    def __init__(self, vhost):
        self.dsn = "amqp://"+ParseEnv.USER_MQ+":"+ParseEnv.PASSWD_MQ+"@localhost/"+vhost

    @classmethod
    async def publish(cls, exchange, message, routing_key):
        channel = await cls.conn.channel()

        _exchange = await channel.declare_exchange(
            exchange, ExchangeType.DIRECT,
        )

        message = Message(
            message.encode('utf-8'),
            message_id=str(uuid.uuid4())
        )

        # Sending the message
        await _exchange.publish(message, routing_key=routing_key)
        print("PUBLISHED")

    @classmethod
    async def consume(cls, exchange, queue):
        channel = await cls.conn.channel()
        queue = await channel.declare_queue(queue)
        await queue.bind(exchange)
        async with queue.iterator() as iterator:
            print(queue)
            async for message in iterator:
                print(message)

