import argparse
import os.path as op
import csv
import time
import json

from confluent_kafka import Producer


def produce(args):
    config = {'bootstrap.servers': args.server}

    producer = Producer(config)

    f = open(args.dataset_path, "r")
    data = csv.DictReader(f)

    print("Started producing")

    for sample in data:
        time.sleep(0.1)

        print(sample)
        producer.produce(args.topic, key='1', value=json.dumps(sample))
        producer.flush()

    
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", type=str, default="localhost:9008")
    parser.add_argument("--topic", type=str, default="f1_telemetry")
    parser.add_argument("--dataset_path", type=str)

    args = parser.parse_args()

    assert op.exists(args.dataset_path)

    produce(args)