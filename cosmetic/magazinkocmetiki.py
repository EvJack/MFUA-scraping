import csv
import requests
from bs4 import BeautifulSoup
import os
import re

def get_data(url):
    req = requests.get(url)
    return req.text

def get_product(src):
    soup = BeautifulSoup(src, 'lxml')
    href_list = [a_tag.get('href') for a_tag in soup.select('h4 a') if a_tag.get('href')]
    return href_list

def get_product_data(href):
    src = get_data(href)
    soup = BeautifulSoup(src, 'lxml')

    not_found_elem = soup.find('div', class_='col-sm-9')
    if not_found_elem and 'The product you requested does not exist.' in not_found_elem.text:
        return None

    articles_elem = soup.select('ul.list-unstyled')
    articles = articles_elem[2].get_text(strip=True) if len(articles_elem) >= 3 else ''

    article_li_elem = soup.find('li', string=re.compile('Артикул:.*'))
    article_text = article_li_elem.text.strip() if article_li_elem else ''
    article = article_text.split('Артикул:')[1].strip() if article_text else ''

    categorys_elem = soup.select('a[rel="nofollow"]')
    categorys = categorys_elem[0].text.strip() if len(categorys_elem) >= 1 else ''
    subcategorys = categorys_elem[1].text.strip() if len(categorys_elem) >= 2 else ''
    subsubcategorys = categorys_elem[2].text.strip() if len(categorys_elem) >= 3 else ''

    names_elem = soup.find('div', class_='col-sm-5')
    names = names_elem.find('b').text.strip() if names_elem and names_elem.find('b') else ''

    image_tag = soup.find('img', title=True, alt=True)
    image_urls = image_tag['src'] if image_tag and 'src' in image_tag.attrs else ''
    if "/cache/" in image_urls:
        image_urls = image_urls.replace("/cache", "")
    if "-380x380" in image_urls:
        image_urls = image_urls.replace("-380x380", "")

    description_div = soup.find('div', id='tab-description')
    descriptions = description_div.get_text(strip=True) if description_div else ''

    start_index = descriptions.find('РФ')
    descriptions = descriptions[start_index + 2:] if start_index != -1 else descriptions

    if descriptions.startswith('.'):
        descriptions = descriptions[1:]

    prices_elem_with_discount = soup.find('h3')
    prices = prices_elem_with_discount.text.strip() if prices_elem_with_discount else ''

    return article, categorys, subcategorys, subsubcategorys, names, image_urls, descriptions, prices

def save_to_csv(data_list, href_list):
    with open("result/result.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        if file.tell() == 0:
            # Include "Ссылка откуда спарсировано" (Source URL) in the header
            writer.writerow(["Артикул", "Категория", "Подкатегория", "подподкатегория", "Название товара", "Image URL", "Описание", "Цена", "Ссылка откуда спарсировано"])

        # Zip the data_list and href_list together to iterate through both lists simultaneously
        for data, href in zip(data_list, href_list):
            # Append the URL (href) from href_list to the data row
            data_row = data + (href,)
            writer.writerow(data_row)

def main():
    if not os.path.exists("result"):
        os.mkdir("result")

    if os.path.exists("result/result.csv"):
        os.remove("result/result.csv")

    data_list = []
    href_list = []

    for i in range(1, 2):
        url = f'https://magazinkocmetiki.com/index.php?route=product/search&limit=4730&page={i}'
        src = get_data(url)
        hrefs = get_product(src)

        print(f"Page {i}:")
        print("Product hrefs:")
        for href in hrefs:
            if re.search(r'/\d+', href):
                href_list.append(href)
                print(href)
                data = get_product_data(href)
                if data is not None:
                    data_list.append(data)

    save_to_csv(data_list, href_list)

if __name__ == '__main__':
    main()
