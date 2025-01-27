if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'kafka error: {err}')
    }
    producer = SerializingProducer(producer_config)

    # producer_manager = KafkaProducerManager(producer_config)

    try:
        simulate_journey(producer, 'Vehicle-Samkons')

    except KeyboardInterrupt:
        print('Simulation ended by user')
    except Exception as e:
        print(f'Unexpected Error occurred : {e}')