# Simple Kafka Streaming Application with Python and Faust

## Setup
### Prerequisites
- Linux, e.g. Ubuntu in WSL2
- Python 3.7+
- docker, docker-compose

### Source Code
Clone this repo to your favorite directory and change to there:
```
git clone ...
cd kafka-streams-simple-python-app
```

Install the required packages:
```
pip install -r requirements
```

### Kafka Broker
A minimal Kafka cluster, consisting of Zookeeper and a standalone Kafka Broker, can be created with the docker compose 
file in `docker-compose.yaml`. 

Execute the setup with `docker-compose up -d`.

## Run the Application
This project ships with a kafka producer, consumer and a streams app.

Deployment steps are the following:
* start the faust worker: `faust -A purchase_stream worker -l info`
* start the kafka consumer (to check message production): `python3 consumer.py kafka_client_config.ini`
* start the kafka producer (will create 10 new messages): `python3 producer.py kafka_client_config.ini`

## Review Streaming Results
Now you can have a look at the output of the Kafka Stream (which is a table) and review the counted results.

Connect to your Kafka Container:
```
$ docker ps
CONTAINER ID   IMAGE                                 COMMAND                  CREATED          STATUS          PORTS                                            NAMES
3daa5375bd2d   confluentinc/cp-kafka:7.0.0           "/etc/confluent/dock…"   29 seconds ago   Up 28 seconds   0.0.0.0:9092->9092/tcp, :::9092->9092/tcp        broker
[...]
$ docker exec -it 3d bash
```

List the topic content of the count_users table:
```
$ /bin/kafka-console-consumer --bootstrap-server localhost:9092 --property print.key=True --topic purchases-count_users-changelog --from-beginning
"jbernard"      1
"jbernard"      2
"htanaka"       1
"jsmith"        1
"jsmith"        2
"eabara"        1
"awalther"      1
"awalther"      2
"eabara"        2
"awalther"      3
Processed a total of 10 messages
```

List the topic content of the count_products table:
```
$ /bin/kafka-console-consumer --bootstrap-server localhost:9092 --property print.key=True --topic purchases-count_purchases-changelog --from-beginning
"batteries"     1
"book"  1
"gift card"     1
"alarm clock"   1
"alarm clock"   2
"alarm clock"   3
"t-shirts"      1
"alarm clock"   4
"alarm clock"   5
"alarm clock"   6
Processed a total of 10 messages
```