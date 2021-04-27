from MODS.DRIVERS.kafka_proc.driver import KafkaProducerConfluent

with KafkaProducerConfluent(
        use_tx=False,
        one_topic_name='__cl_smpb_showcase_kafka_queue_general_nsi_means_of_passport'
) as kp:
    for i in range(37):
        kp.put_data(
            key='test1',
            value={
                'INN': f'99777_{i}',
                'Size': 7000 + i
            }
        )
