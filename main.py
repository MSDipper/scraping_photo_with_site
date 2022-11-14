import requests
from bs4 import BeautifulSoup
import json

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

def get_image(url):
    req = requests.get(url, stream=True)
    r = open("/home/userlinux3/Django_Framework_project_GitHub/scraping__GH/image/" + url.split('/')[-1], 'wb')
    for value in req.iter_content(1024*1024):
        r.write(value)
    r.close()


for i in range(1, 129, 20):
    url = f'https://iss-work.com/page/{i}/'
    
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml') 

    # with open('index.html', 'w') as file:
    #     file.write(response.text)
    
    with open('index.html') as file:
        src = file.read()
        
soup = BeautifulSoup(src, 'lxml')
all_products_hrefs = soup.find_all(class_='bx-sz-bb text-center')

all_title_href_dict = {}
for i in all_products_hrefs:
    item_text = i.find('a').text.strip()
    item_href = i.find('a').get('href')
    all_title_href_dict[item_text] = item_href

# with open('all_title_href_dict.json', 'w') as file:
#     json.dump(all_title_href_dict, file, indent=4, ensure_ascii=False)


with open('all_title_href_dict.json') as file:
    all_title_href = json.load(file)


for product_name, product_href in all_title_href.items():
    req = requests.get(url = product_href, headers = headers)
    src = req.text
    
    # with open(f'data/{product_name}.html', 'w') as file:
    #     file.write(src)
    
    with open(f'data/{product_name}.html') as file:
        src = file.read()
        
    soup = BeautifulSoup(src, 'lxml')
    product_image = soup.find_all(class_='wp-block-image size-large')
    
    
    for i in product_image:
        image = 'https://iss-work.com/' + i.find('img').get('src')
        get_image(image)