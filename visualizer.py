import argparse
import json
from time import sleep

import matplotlib.pyplot as plt
import streamlit as st 
from confluent_kafka import Consumer
import pandas as pd



if __name__ == "__main__":
    st.set_page_config(
        page_title="Race telemetry",
        layout="wide",
    )

    pilot_position = st.empty()
    data_table = st.empty()
    pilot_index = st.selectbox(label="driver id", options=range(20), index=None)

    parser = argparse.ArgumentParser()
    parser.add_argument("--server", type=str, default="localhost:9008")
    parser.add_argument("--topic", type=str, default="f1_telemetry")

    args = parser.parse_args()

    config = {'bootstrap.servers': args.server, 'group.id': 'my_consumers'}
    consumer = Consumer(config)
    consumer.subscribe([args.topic])

    print("Started consuming")

    message= consumer.poll(2000)
    sample = json.loads(message.value())
    
    data_dict = {}
    for key in sample:
        data_dict[key] = [""] * 20


    while True:
        message= consumer.poll(2000)
        if message is None:
            print('The message is empty')
            continue

        sample = json.loads(message.value())
        print(sample) 


        for key in sample.keys():
            data_dict[key][int(sample["pilot_index"])] = sample[key]

        data_table.table(pd.DataFrame(data_dict))

        if int(sample["pilot_index"]) != pilot_index:
            continue

        fig, ax = plt.subplots()
        plt.xlim([-1000., 1000.])
        plt.ylim([-1000., 1000.])
        ax.scatter([float(sample["worldPositionX"])], [float(sample["worldPositionZ"])])
        
        pilot_position.pyplot(fig, clear_figure=True)