### Env Setup
    pip install -r requirements.txt
    sudo docker-compose up
Download the dataset: https://disk.yandex.ru/d/yBki2haZCe7t8Q
### Start data flow
    python producer.py --dataset_path "path to the dataset"

In another tab

    python visualizer.py

Open streamlit frontend with browser

#### I wanted to implement winner with deep learning but it appeared to be too complicated so I just left the position and telemetry visualization