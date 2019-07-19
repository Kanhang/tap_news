#!/bin/bash
service redis_6379 start
service mongod start

pip install -r requirements.txt

cd news_topic_modeling_service/server
nohup python server.py &

cd ../../news_pipeline
nohup python news_monitor.py &
nohup python news_fetcher.py &
nohup python news_deduper.py &

echo "=================================================="
read -p "PRESS [ANY KEY] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
