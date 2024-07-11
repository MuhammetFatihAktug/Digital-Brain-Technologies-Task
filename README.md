# Digital-Brain-Technologies-Task

Digital Brain Technologies ML Engineer Task

## Task 1: Kafka Kurulumu ve Mesaj Gönderme

### Adım 1: Docker ile Kafka ve Zookeeper Kurulumu

Öncelikle, Kafka ve Zookeeper'ı Docker kullanarak kurmamız gerekiyor. Bunun için aşağıdaki `docker-compose.yml` dosyasını kullanın:

```yaml
version: '2'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.3.0
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  broker:
    image: confluentinc/cp-kafka:7.3.0
    container_name: broker
    ports:
      - "9092:9092"
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1 
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT, PLAINTEXT_INTERNAL:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092,PLAINTEXT_INTERNAL://broker:29092
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
```

Docker servislerini başlatmak için aşağıdaki komutu kullanın:

```sh
docker-compose up -d
```

### Adım 2: Kafka Konusu (Topic) Oluşturma

Kafka CLI komutlarını kullanarak bir konu oluşturun. Öncelikle, broker konteynerine bağlanın:

```sh
docker exec -it broker /bin/sh
```

Ardından, aşağıdaki komutu kullanarak bir Kafka konusu oluşturun:

```sh
kafka-topics --create --topic my-topic --bootstrap-server broker:9092 --partitions 1 --replication-factor 1
```

### Adım 3: Kafka Konusuna Mesaj Gönderme

Oluşturduğunuz konuya mesaj göndermek için aşağıdaki komutu kullanın:

```sh
kafka-console-producer --broker-list broker:9092 --topic my-topic
```

Komut çalıştırıldıktan sonra, konsolda mesajlarınızı yazabilirsiniz. Örneğin:

```sh
> Merhaba sayin izleyici
> Umarim dogru olmustur
```

### Adım 4: Kafka Konusundan Mesaj Dinleme

```sh
kafka-console-consumer --bootstrap-server broker:9092 --topic my-topic --from-beginning --partition 0
```

### Ornek Resim

![Program Ciktisi](task_1_png.PNG)
