import csv
import requests
from bs4 import BeautifulSoup
import os

def get_data_services(url):
    req_services = requests.get(url)
    return req_services.text

def get_phones_and_names_services(src):
    soup = BeautifulSoup(src, 'html.parser')
    phone_elements = soup.find_all('span', class_='protectedNumber')

    data_services = []

    for element in phone_elements:
        phone_services = element.get('title', 'none')
        name_services = ''
        prev_sibling = element.find_previous_sibling()

        while prev_sibling is not None:
            if prev_sibling.name == 'span' and prev_sibling.find('img') and prev_sibling.find('img')['src'] == '/img/icons/person.gif':
                name_services = prev_sibling.next_sibling.strip()
                break
            prev_sibling = prev_sibling.previous_sibling

        data_services.append({'phone': phone_services, 'name': name_services})

    return data_services

def get_category_id_services(src):
    soup = BeautifulSoup(src, 'html.parser')
    category_elements = soup.find_all('span', class_='category')
    categories_services = [element.text.strip() for element in category_elements]
    return categories_services

def get_titles_services(src):
    soup = BeautifulSoup(src, 'html.parser')
    title_elements = soup.find_all('a', class_='title')
    titles_services = [element.text.strip() for element in title_elements]
    return titles_services

def get_descriptions_services(src):
    soup = BeautifulSoup(src, 'html.parser')
    description_elements = soup.find_all('p', class_='zam')
    descriptions_services = [element.text.strip() for element in description_elements]
    return descriptions_services

def get_image_urls_services(src):
    soup = BeautifulSoup(src, 'html.parser')
    thumbs_elements = soup.find_all('div', class_='thumbs')
    image_urls_services = []

    for element in thumbs_elements:
        image_elements = element.find_all('img')
        for img in image_elements:
            if 'src' in img.attrs:
                image_url = img['src']
                if "_thumbnail" in image_url:
                    image_url = image_url.replace("_thumbnail", "")
                image_urls_services.append(image_url)

    return image_urls_services

def save_to_csv(data, categories, titles, descriptions, image_urls):
    with open("result/data_services.csv", "a", encoding="utf-8", newline="") as file:
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
    if os.path.exists("result/data_services.csv"):
        os.remove("result/data_services.csv")

    for i in range(1, 20):
        url = f'http://jerdesh.ru/birge_uslugi/{i}'
        src_services = get_data_services(url)
        data_services = get_phones_and_names_services(src_services)
        categories_services = get_category_id_services(src_services)
        titles_services = get_titles_services(src_services)
        descriptions_services = get_descriptions_services(src_services)
        image_urls_services = get_image_urls_services(src_services)

        print(f"Page {i}:")

        print("Name and phone:")
        for item in data_services:
            print(item['name'], item['phone'])

        print("Categories:")
        for category in categories_services:
            print(category)

        print("Titles:")
        for title in titles_services:
            print(title)

        print("Descriptions:")
        for description in descriptions_services:
            print(description)

        print("Image URLs:")
        for url in image_urls_services:
            print(url)

        print()
        save_to_csv(data_services, categories_services, titles_services, descriptions_services, image_urls_services)

if __name__ == '__services__':
    main()
