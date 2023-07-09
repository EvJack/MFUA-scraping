import csv
import requests
from bs4 import BeautifulSoup
import os

def get_data_rent(url):
    req_rent = requests.get(url)
    return req_rent.text

def get_phones_and_names_rent(src):
    soup = BeautifulSoup(src, 'html.parser')
    phone_elements = soup.find_all('span', class_='protectedNumber')

    data_rent = []

    for element in phone_elements:
        phone_rent = element.get('title', 'none')
        name_rent = ''
        prev_sibling = element.find_previous_sibling()

        while prev_sibling is not None:
            if prev_sibling.name == 'span' and prev_sibling.find('img') and prev_sibling.find('img')['src'] == '/img/icons/person.gif':
                name_rent = prev_sibling.next_sibling.strip()
                break
            prev_sibling = prev_sibling.previous_sibling

        data_rent.append({'phone': phone_rent, 'name': name_rent})

    return data_rent

def get_category_id_rent(src):
    soup = BeautifulSoup(src, 'html.parser')
    category_elements = soup.find_all('span', class_='category')
    categories_rent = [element.text.strip() for element in category_elements]
    return categories_rent

def get_titles_rent(src):
    soup = BeautifulSoup(src, 'html.parser')
    title_elements = soup.find_all('a', class_='title')
    titles_rent = [element.text.strip() for element in title_elements]
    return titles_rent

def get_descriptions_rent(src):
    soup = BeautifulSoup(src, 'html.parser')
    description_elements = soup.find_all('p', class_='zam')
    descriptions_rent = [element.text.strip() for element in description_elements]
    return descriptions_rent

def get_image_urls_rent(src):
    soup = BeautifulSoup(src, 'html.parser')
    thumbs_elements = soup.find_all('div', class_='thumbs')
    image_urls_rent = []

    for element in thumbs_elements:
        image_elements = element.find_all('img')
        for img in image_elements:
            if 'src' in img.attrs:
                image_url = img['src']
                if "_thumbnail" in image_url:
                    image_url = image_url.replace("_thumbnail", "")
                image_urls_rent.append(image_url)

    return image_urls_rent

def save_to_csv(data, categories, titles, descriptions, image_urls):
    with open("result/data_rent.csv", "a", encoding="utf-8", newline="") as file:
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
    if os.path.exists("result/data_rent.csv"):
        os.remove("result/data_rent.csv")

    for i in range(1, 101):
        url = f'http://jerdesh.ru/birge_sdayu_komnatu_kojko_mesto/{i}'
        src_rent = get_data_rent(url)
        data_rent = get_phones_and_names_rent(src_rent)
        categories_rent = get_category_id_rent(src_rent)
        titles_rent = get_titles_rent(src_rent)
        descriptions_rent = get_descriptions_rent(src_rent)
        image_urls_rent = get_image_urls_rent(src_rent)

        print(f"Page {i}:")

        print("Name and phone:")
        for item in data_rent:
            print(item['name'], item['phone'])

        print("Categories:")
        for category in categories_rent:
            print(category)

        print("Titles:")
        for title in titles_rent:
            print(title)

        print("Descriptions:")
        for description in descriptions_rent:
            print(description)

        print("Image URLs:")
        for url in image_urls_rent:
            print(url)

        print()
        save_to_csv(data_rent, categories_rent, titles_rent, descriptions_rent, image_urls_rent)

if __name__ == '__rent__':
    main()
