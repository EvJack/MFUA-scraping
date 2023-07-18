import csv
import requests
from bs4 import BeautifulSoup
import os

def get_data_job(url):
    req_job = requests.get(url)
    return req_job.text

def get_phones_and_names_job(src):
    soup = BeautifulSoup(src, 'html.parser')
    phone_elements = soup.find_all('span', class_='protectedNumber')

    data_job = []

    for element in phone_elements:
        phone_job = element.get('title', 'none')
        name_job = ''
        prev_sibling = element.find_previous_sibling()

        while prev_sibling is not None:
            if prev_sibling.name == 'span' and prev_sibling.find('img') and prev_sibling.find('img')['src'] == '/img/icons/person.gif':
                name_job = prev_sibling.next_sibling.strip()
                break
            prev_sibling = prev_sibling.previous_sibling

        data_job.append({'phone': phone_job, 'name': name_job})

    return data_job

def get_category_id_job(src):
    soup = BeautifulSoup(src, 'html.parser')
    category_elements = soup.find_all('span', class_='category')
    categories_job = [element.text.strip() for element in category_elements]
    return categories_job

def get_titles_job(src):
    soup = BeautifulSoup(src, 'html.parser')
    title_elements = soup.find_all('a', class_='title')
    titles_job = [element.text.strip() for element in title_elements]
    return titles_job

def get_descriptions_job(src):
    soup = BeautifulSoup(src, 'html.parser')
    description_elements = soup.find_all('p', class_='zam')
    descriptions_job = [element.text.strip() for element in description_elements]
    return descriptions_job

def get_image_urls_job(src):
    soup = BeautifulSoup(src, 'html.parser')
    thumbs_elements = soup.find_all('div', class_='thumbs')
    image_urls_job = []

    for element in thumbs_elements:
        image_elements = element.find_all('img')
        for img in image_elements:
            if 'src' in img.attrs:
                image_url = img['src']
                if "_thumbnail" in image_url:
                    image_url = image_url.replace("_thumbnail", "")
                image_urls_job.append(image_url)

    return image_urls_job

def save_to_csv(data, categories, titles, descriptions, image_urls):
    with open("result/data_job.csv", "a", encoding="utf-8", newline="") as file:
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
    if os.path.exists("result/data_job.csv"):
        os.remove("result/data_job.csv")

    for i in range(1, 6):
        url = f'http://jerdesh.ru/birge_rabota/{i}'
        src_job = get_data_job(url)
        data_job = get_phones_and_names_job(src_job)
        categories_job = get_category_id_job(src_job)
        titles_job = get_titles_job(src_job)
        descriptions_job = get_descriptions_job(src_job)
        image_urls_job = get_image_urls_job(src_job)

        print(f"Page {i}:")

        print("Name and phone:")
        for item in data_job:
            print(item['name'], item['phone'])

        print("Categories:")
        for category in categories_job:
            print(category)

        print("Titles:")
        for title in titles_job:
            print(title)

        print("Descriptions:")
        for description in descriptions_job:
            print(description)

        print("Image URLs:")
        for url in image_urls_job:
            print(url)

        print()
        save_to_csv(data_job, categories_job, titles_job, descriptions_job, image_urls_job)

if __name__ == '__job__':
    main()
