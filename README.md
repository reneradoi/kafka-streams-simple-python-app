# Simple Kafka Streaming Application with Python and Faust

## Setup
### Prerequisites
- Linux, e.g. Ubuntu in WSL2
- Python 3.7+
- docker, docker-compose

### Source Code
Clone this repo to your favorite directory and change to there:
```
git clone [repo url]
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
This project ships with a kafka producer, consumer and a streams app. Producer and consumer are based on the step-by-step
guide "Getting Started with Apache Kafka and Python" (https://developer.confluent.io/get-started/python).

Deployment steps are the following:
* start the faust worker: `faust -A purchase_stream worker -l info`
* start the kafka producer (will create a new message every two seconds): 
```
$ python3 producer.py kafka_client_config.ini
produced message with user: eabara, product: t-shirts
produced message with user: awalther, product: gift card
produced message with user: sgarcia, product: alarm clock
produced message with user: eabara, product: book
produced message with user: sgarcia, product: t-shirts
produced message with user: jbernard, product: batteries
```

In order to review your streaming results, connect to the Kafka Container and have a look at corresponding topic.
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
[...]
```

### Use Case 1: Aggregate
`faust -A purchase_stream worker -l info`

Result: Counts the amount of purchases each user makes:
```
$ /bin/kafka-console-consumer --bootstrap-server localhost:9092 --property print.key=True --topic purchases-count_users-changelog
"awalther"      2102
"jbernard"      2041
"awalther"      2103
"htanaka"       2070
"awalther"      2104
"jbernard"      2042
"awalther"      2105
"jbernard"      2043
"awalther"      2106
"htanaka"       2071
[...]
```

### Use Case 2: Filter Data
`faust -A filtered_stream worker -l info`

Result: Only purchases for books or batteries will be shown.
```
$ /bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic filtered_purchases
{"user": "eabara", "product": "batteries", "__faust": {"ns": "filtered_stream.Purchase"}}
{"user": "eabara", "product": "batteries", "__faust": {"ns": "filtered_stream.Purchase"}}
{"user": "jsmith", "product": "batteries", "__faust": {"ns": "filtered_stream.Purchase"}}
[...]
```

### Use Case 3: Join Information
`faust -A joint_stream worker -l info`

Result: The topic will show all purchases with the total amount for this product since start of producing messages
```
$ /bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic joint_purchases
"user: eabara, product: batteries, amount: 16504"
"user: jbernard, product: t-shirts, amount: 16506"
"user: htanaka, product: batteries, amount: 16505"
"user: jsmith, product: batteries, amount: 16506"
"user: jsmith, product: alarm clock, amount: 16621"
"user: sgarcia, product: alarm clock, amount: 16622"
"user: htanaka, product: gift card, amount: 16398"
[...]
```