import csv
import requests
from bs4 import BeautifulSoup
import os

def get_data_sell(url):
    req_sell = requests.get(url)
    return req_sell.text

def get_phones_and_names_sell(src):
    soup = BeautifulSoup(src, 'html.parser')
    phone_elements = soup.find_all('span', class_='protectedNumber')

    data_sell = []

    for element in phone_elements:
        phone_sell = element.get('title', 'none')
        name_sell = ''
        prev_sibling = element.find_previous_sibling()

        while prev_sibling is not None:
            if prev_sibling.name == 'span' and prev_sibling.find('img') and prev_sibling.find('img')['src'] == '/img/icons/person.gif':
                name_sell = prev_sibling.next_sibling.strip()
                break
            prev_sibling = prev_sibling.previous_sibling

        data_sell.append({'phone': phone_sell, 'name': name_sell})

    return data_sell

def get_category_id_sell(src):
    soup = BeautifulSoup(src, 'html.parser')
    category_elements = soup.find_all('span', class_='category')
    categories_sell = [element.text.strip() for element in category_elements]
    return categories_sell

def get_titles_sell(src):
    soup = BeautifulSoup(src, 'html.parser')
    title_elements = soup.find_all('a', class_='title')
    titles_sell = [element.text.strip() for element in title_elements]
    return titles_sell

def get_descriptions_sell(src):
    soup = BeautifulSoup(src, 'html.parser')
    description_elements = soup.find_all('p', class_='zam')
    descriptions_sell = [element.text.strip() for element in description_elements]
    return descriptions_sell

def get_image_urls_sell(src):
    soup = BeautifulSoup(src, 'html.parser')
    thumbs_elements = soup.find_all('div', class_='thumbs')
    image_urls_sell = []

    for element in thumbs_elements:
        image_elements = element.find_all('img')
        for img in image_elements:
            if 'src' in img.attrs:
                image_url = img['src']
                if "_thumbnail" in image_url:
                    image_url = image_url.replace("_thumbnail", "")
                image_urls_sell.append(image_url)

    return image_urls_sell

def save_to_csv(data, categories, titles, descriptions, image_urls):
    with open("result/data_sell.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Name", "Phone", "Category", "Title", "Description", "Image URL", "City_ID"])

        for i in range(len(data)):
            if i < len(image_urls):
                row = [data[i]['name'], data[i]['phone'], categories[i], titles[i], descriptions[i], image_urls[i], 992]
            else:
                row = [data[i]['name'], data[i]['phone'], categories[i], titles[i], descriptions[i], 'None', 992]
            writer.writerow(row)

def main():
    if os.path.exists("result/data_sell.csv"):
        os.remove("result/data_sell.csv")

    for i in range(1, 42):
        url = f'http://jerdesh.ru/birge_prodayu-kuplyu/{i}'
        src_sell = get_data_sell(url)
        data_sell = get_phones_and_names_sell(src_sell)
        categories_sell = get_category_id_sell(src_sell)
        titles_sell = get_titles_sell(src_sell)
        descriptions_sell = get_descriptions_sell(src_sell)
        image_urls_sell = get_image_urls_sell(src_sell)

        print(f"Page {i}:")

        print("Name and phone:")
        for item in data_sell:
            print(item['name'], item['phone'])

        print("Categories:")
        for category in categories_sell:
            print(category)

        print("Titles:")
        for title in titles_sell:
            print(title)

        print("Descriptions:")
        for description in descriptions_sell:
            print(description)

        print("Image URLs:")
        for url in image_urls_sell:
            print(url)

        print()
        save_to_csv(data_sell, categories_sell, titles_sell, descriptions_sell, image_urls_sell)

if __name__ == '__sell__':
    main()
