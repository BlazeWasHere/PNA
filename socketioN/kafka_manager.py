import logging
import pickle

try:
    import kafka
except ImportError:
    kafka = None

from .pubsub_manager import PubSubManager

logger = logging.getLogger('socketioN')


class KafkaManager(PubSubManager):  # pragma: no cover
    """Kafka based client manager.

    This class implements a Kafka backend for event sharing across multiple
    processes.

    To use a Kafka backend, initialize the :class:`Server` instance as
    follows::

        url = 'kafka://hostname:port'
        server = socketioN.Server(client_manager=socketioN.KafkaManager(url))

    :param url: The connection URL for the Kafka server. For a default Kafka
                store running on the same host, use ``kafka://``.
    :param channel: The channel name (topic) on which the server sends and
                    receives notifications. Must be the same in all the
                    servers.
    :param write_only: If set ot ``True``, only initialize to emit events. The
                       default of ``False`` initializes the class for emitting
                       and receiving.
    """
    name = 'kafka'

    def __init__(self, url='kafka://localhost:9092', channel='socketioN',
                 write_only=False):
        if kafka is None:
            raise RuntimeError('kafka-python package is not installed '
                               '(Run "pip install kafka-python" in your '
                               'virtualenv).')

        super(KafkaManager, self).__init__(channel=channel,
                                           write_only=write_only)

        self.kafka_url = url[8:] if url != 'kafka://' else 'localhost:9092'
        self.producer = kafka.KafkaProducer(bootstrap_servers=self.kafka_url)
        self.consumer = kafka.KafkaConsumer(self.channel,
                                            bootstrap_servers=self.kafka_url)

    def _publish(self, data):
        self.producer.send(self.channel, value=pickle.dumps(data))
        self.producer.flush()

    def _kafka_listen(self):
        for message in self.consumer:
            yield message

    def _listen(self):
        for message in self._kafka_listen():
            if message.topic == self.channel:
                yield pickle.loads(message.value)
