# STA9760 Project 3  Visualizing and Analysis on Kibana

![scrnshot](https://raw.githubusercontent.com/laurachan2020/STA9760_Kibana/master/dashboard.PNG)

## How to Run

Start:

export APP_KEY={MY_TOKEN}

docker-compose up -d

cd C:\project3\bigdata3

git pull

docker-compose down

docker images

docker rmi bigdata3_pyth -f

docker-compose up -d

docker-compose run pyth python tickets.py --page_size=12000 --num_pages=400

The above command will load violation parking data into Elasticsearch.

Shutting off:

docker-compose down



