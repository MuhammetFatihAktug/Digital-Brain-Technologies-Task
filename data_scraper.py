import time
import json
from confluent_kafka import Producer
import requests
from bs4 import BeautifulSoup

# Kafka üretici ayarları
kafka_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker adresi
}

# Kafka'ya veri gönderme
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

producer = Producer(kafka_config)

def send_to_kafka(topic, data):
    producer.produce(topic, key='product', value=json.dumps(data), callback=delivery_report)
    producer.flush()

# Ürünleri çekme ve Kafka'ya gönderme
def get_page_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_product_data(product):
    name = product.find('h2', class_='woocommerce-loop-product__title').text
    price = product.find('span', class_='woocommerce-Price-amount').text
    description_url = product.find('a', class_='woocommerce-LoopProduct-link')['href']
    description, stock = get_product_details(description_url)
    
    return {
        'name': name,
        'price': price,
        'description': description,
        'stock': stock
    }

def get_product_details(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    description_tag = soup.find('div', class_='woocommerce-product-details__short-description')
    description = description_tag.text.strip() if description_tag else 'No description available'
    
    stock_tag = soup.find('p', class_='stock')
    stock = stock_tag.text.strip() if stock_tag else 'Stock info not available'
    
    return description, stock

def scrape_and_send(base_url, max_pages, topic):
    with open('products_data.json', 'w') as file:
        for page in range(1, max_pages + 1):
            page_url = f"{base_url}?paged={page}"
            soup = get_page_soup(page_url)
            
            products = soup.find_all('li', class_='product')
            for product in products:
                product_data = get_product_data(product)
                send_to_kafka(topic, product_data)
                
                # Veriyi dosyaya yaz
                json.dump(product_data, file)
                file.write('\n')
                
                time.sleep(1)  # 1 saniyede bir veri gönder
                print(f"Sent to Kafka: {product_data}")

# Kullanım
base_url = "https://scrapeme.live/shop/"
max_pages = 1  # Toplam sayfa sayısı
topic = "product_topic_1"  # Kafka topic adı

scrape_and_send(base_url, max_pages, topic)
