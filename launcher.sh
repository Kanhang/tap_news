#!/bin/bash
fuser -k 3001/tcp
fuser -k 4040/tcp
fuser -k 5050/tcp

service redis_6379 start
service mongod start

pip install -r requirements.txt

cd ./web_server/client
npm install
# npm run build
GENERATE_SOURCEMAP=false npm run-script build
cd ../server
npm install
nohup nodemon ./bin/www --port=3001 &
cd ../../backend_server
nohup python service.py &
cd ../news_recommendation_service
nohup python recommendation_service.py &
nohup python click_log_processor.py &

echo "=================================================="
read -p "PRESS [ANY KEY] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
fuser -k 3001/tcp
service redis_6379 stop
service mongod stop

# Please delete below comment.
# First, cd week8. Then input command: chmod +x launcher.sh
#After that, input command to run web app tap-news: sudo ./launcher.sh
