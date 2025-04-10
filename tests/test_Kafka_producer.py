# # import pytest
# # from unittest.mock import MagicMock,patch, ANY
# # from confluent_kafka import Message
# # from src.simulation.kafka_producer import KafkaProducerManager
# #
# #
# # @pytest.fixture
# # def mock_kafka_producer():
# #     """
# #     Fixture to mock Kafka producer and return the KafkaProducerManager instance.
# #     """
# #     producer_config = {"bootstrap.servers": "localhost:9093"}
# #
# #     mock_producer = MagicMock()
# #
# #     kafka_producer_manager = KafkaProducerManager(producer_config)
# #
# #     kafka_producer_manager.producer = mock_producer
# #
# #     return kafka_producer_manager, mock_producer
# #
# # @pytest.fixture
# # def kafka_producer_manager():
# #     producer_config = {'bootstrap.servers': 'localhost:9092'}
# #     return KafkaProducerManager(producer_config)
# #
# # def test_produce_data(kafka_producer_manager):
# #     mock_on_delivery = MagicMock()
# #
# #     data = {
# #         "id": "12345",
# #         "device_id": "67890",
# #         "timestamp": "2025-03-23T12:34:56",
# #         "location": "52.4862,-1.8904",
# #         "speed": 60.0,
# #         "direction": "North-East",
# #         "make": "Toyota",
# #         "model": "Prius",
# #         "fuelType": "Hybrid"
# #     }
# #
# #     with patch.object(kafka_producer_manager.producer, 'produce') as mock_produce:
# #         kafka_producer_manager.produce_data('test-topic', data)
# #
# #         mock_produce.assert_called_once_with(
# #             'test-topic',
# #             key='12345',
# #             value=b'{"id": "12345", "device_id": "67890", "timestamp": "2025-03-23T12:34:56", "location": "52.4862,-1.8904", "speed": 60.0, "direction": "North-East", "make": "Toyota", "model": "Prius", "fuelType": "Hybrid"}',
# #             on_delivery=ANY
# #         )
# #
# #
# #         mock_on_delivery.assert_called_once()
# #
# #         args, kwargs = mock_on_delivery.call_args
# #         assert len(args) == 2
# #         assert isinstance(args[1], Message)
# #
# # # def test_delivery_report():
# # #     """
# # #     Test the delivery_report method of KafkaProducerManager.
# # #     """
# # #     mock_msg = MagicMock(spec=Message)
# # #     mock_msg.topic.return_value = "test-topic"
# # #     mock_msg.partition.return_value = 0
# #
# # #     KafkaProducerManager.delivery_report(None, mock_msg)
# # #
# # #     mock_msg.topic.assert_called_once()
# #
# # #     KafkaProducerManager.delivery_report("Error", mock_msg)
# #
# # #     mock_msg.topic.assert_called_once()
# #
#
#
# import pytest
# from unittest.mock import MagicMock, patch, ANY
# from confluent_kafka import Message
# from src.simulation.kafka_producer import KafkaProducerManager
#
#
# @pytest.fixture
# def mock_kafka_producer():
#     """
#     Fixture to mock Kafka producer and return the KafkaProducerManager instance.
#     """
#     producer_config = {"bootstrap.servers": "localhost:9093"}
#
#     mock_producer = MagicMock()
#
#     kafka_producer_manager = KafkaProducerManager(producer_config)
#
#     kafka_producer_manager.producer = mock_producer
#
#     return kafka_producer_manager, mock_producer
#
#
# @pytest.fixture
# def kafka_producer_manager():
#     producer_config = {'bootstrap.servers': 'localhost:9092'}
#     return KafkaProducerManager(producer_config)
#
#
# def test_produce_data(kafka_producer_manager, mock_kafka_producer):
#     mock_on_delivery = MagicMock()
#
#     data = {
#         "id": "12345",
#         "device_id": "67890",
#         "timestamp": "2025-03-23T12:34:56",
#         "location": "52.4862,-1.8904",
#         "speed": 60.0,
#         "direction": "North-East",
#         "make": "Toyota",
#         "model": "Prius",
#         "fuelType": "Hybrid"
#     }
#
#     with patch.object(kafka_producer_manager.producer, 'produce') as mock_produce, \
#             patch.object(kafka_producer_manager.producer, 'flush') as mock_flush:
#         # Call the function under test
#         kafka_producer_manager.produce_data('test-topic', data)
#
#         # Check if produce was called with correct arguments
#         mock_produce.assert_called_once_with(
#             'test-topic',
#             key='12345',
#             value=b'{"id": "12345", "device_id": "67890", "timestamp": "2025-03-23T12:34:56", "location": "52.4862,-1.8904", "speed": 60.0, "direction": "North-East", "make": "Toyota", "model": "Prius", "fuelType": "Hybrid"}',
#             on_delivery=ANY  # Ensure on_delivery is passed as argument
#         )
#
#         # Check if flush was called
#         mock_flush.assert_called_once()
#
#         # Handle on_delivery callback
#         args, kwargs = mock_produce.call_args
#         on_delivery = kwargs.get('on_delivery')
#
#         # Test that the on_delivery callback is invoked when produce is called
#         if on_delivery:
#             on_delivery(None, MagicMock())
#             mock_on_delivery.assert_called_once()