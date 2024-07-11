import requests
from bs4 import BeautifulSoup

def get_page_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_product_data(product):
    title = product.find('h2', class_='woocommerce-loop-product__title').text
    price = product.find('span', class_='woocommerce-Price-amount').text
    description_url = product.find('a', class_='woocommerce-LoopProduct-link')['href']
    description, stock = get_product_details(description_url)
    
    return {
        'title': title,
        'price': price,
        'description': description,
        'stock': stock
    }

def get_product_details(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Description ve stock bilgilerini çek
    description_tag = soup.find('div', class_='woocommerce-product-details__short-description')
    description = description_tag.text.strip() if description_tag else 'No description available'
    
    stock_tag = soup.find('p', class_='stock')
    stock = stock_tag.text.strip() if stock_tag else 'Stock info not available'
    
    return description, stock

def scrape_all_products(base_url, max_pages):
    all_products = []
    
    for page in range(1, max_pages + 1):
        page_url = f"{base_url}?paged={page}"
        soup = get_page_soup(page_url)
        
        products = soup.find_all('li', class_='product')
        for product in products:
            product_data = get_product_data(product)
            all_products.append(product_data)
    
    return all_products

# Kullanım
base_url = "https://scrapeme.live/shop/"
max_pages = 1  # Toplam sayfa sayısı. Bu değeri gerçek sayfa sayısına göre güncelleyin.
all_products = scrape_all_products(base_url, max_pages)

# Çıktıyı kontrol et
for product in all_products:
    print(f"Title: {product['title']}")
    print(f"Price: {product['price']}")
    print(f"Description: {product['description']}")
    print(f"Stock: {product['stock']}")
    print("-" * 40)
