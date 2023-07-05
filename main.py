import csv
import requests
from bs4 import BeautifulSoup
import os

def get_data(url):
    req = requests.get(url)
    return req.text

def get_phones_and_names(src):
    soup = BeautifulSoup(src, 'html.parser')
    phone_elements = soup.find_all('span', class_='protectedNumber')

    data = []

    for element in phone_elements:
        phone = element.get('title', 'none')
        name = ''
        prev_sibling = element.find_previous_sibling()

        while prev_sibling is not None:
            if prev_sibling.name == 'span' and prev_sibling.find('img') and prev_sibling.find('img')['src'] == '/img/icons/person.gif':
                name = prev_sibling.next_sibling.strip()
                break
            prev_sibling = prev_sibling.previous_sibling

        data.append({'phone': phone, 'name': name})

    return data

def get_category_id(src):
    soup = BeautifulSoup(src, 'html.parser')
    category_elements = soup.find_all('span', class_='category')
    categories = [element.text.strip() for element in category_elements]
    return categories

def get_titles(src):
    soup = BeautifulSoup(src, 'html.parser')
    title_elements = soup.find_all('a', class_='title')
    titles = [element.text.strip() for element in title_elements]
    return titles

def get_descriptions(src):
    soup = BeautifulSoup(src, 'html.parser')
    description_elements = soup.find_all('p', class_='zam')
    descriptions = [element.text.strip() for element in description_elements]
    return descriptions

def get_image_urls(src):
    soup = BeautifulSoup(src, 'html.parser')
    thumbs_elements = soup.find_all('div', class_='thumbs')
    image_urls = []

    for element in thumbs_elements:
        image_elements = element.find_all('img')
        for img in image_elements:
            if 'src' in img.attrs:
                image_url = img['src']
                image_urls.append(image_url)

    return image_urls

def save_to_csv(data, categories, titles, descriptions, image_urls):
    with open("data.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Name", "Phone", "Category", "Title", "Description", "Image URL", "ID"])

        for i in range(len(data)):
            if i < len(image_urls):
                row = [data[i]['name'], data[i]['phone'], categories[i], titles[i], descriptions[i], image_urls[i], 992]
            else:
                row = [data[i]['name'], data[i]['phone'], categories[i], titles[i], descriptions[i], 'None', 992]
            writer.writerow(row)
def main():
    if os.path.exists("data.csv"):
        os.remove("data.csv")

    for i in range(1, 101):
        url = f'http://jerdesh.ru/search/iPage,{i}'
        src = get_data(url)
        data = get_phones_and_names(src)
        categories = get_category_id(src)
        titles = get_titles(src)
        descriptions = get_descriptions(src)
        image_urls = get_image_urls(src)

        print(f"Page {i}:")

        print("Name and phone:")
        for item in data:
            print(item['name'], item['phone'])

        print("Categories:")
        for category in categories:
            print(category)

        print("Titles:")
        for title in titles:
            print(title)

        print("Descriptions:")
        for description in descriptions:
            print(description)

        print("Image URLs:")
        for url in image_urls:
            print(url)

        print()
        save_to_csv(data, categories, titles, descriptions, image_urls)

if __name__ == '__main__':
    main()
