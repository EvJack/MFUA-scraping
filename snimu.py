import csv
import requests
from bs4 import BeautifulSoup
import os

def get_data_snimu(url):
    req_snimu = requests.get(url)
    return req_snimu.text

def get_phones_and_names_snimu(src):
    soup = BeautifulSoup(src, 'html.parser')
    phone_elements = soup.find_all('span', class_='protectedNumber')

    data_snimu = []

    for element in phone_elements:
        phone_snimu = element.get('title', 'none')
        name_snimu = ''
        prev_sibling = element.find_previous_sibling()

        while prev_sibling is not None:
            if prev_sibling.name == 'span' and prev_sibling.find('img') and prev_sibling.find('img')['src'] == '/img/icons/person.gif':
                name_snimu = prev_sibling.next_sibling.strip()
                break
            prev_sibling = prev_sibling.previous_sibling

        data_snimu.append({'phone': phone_snimu, 'name': name_snimu})

    return data_snimu

def get_category_id_snimu(src):
    soup = BeautifulSoup(src, 'html.parser')
    category_elements = soup.find_all('span', class_='category')
    categories_snimu = [element.text.strip() for element in category_elements]
    return categories_snimu

def get_titles_snimu(src):
    soup = BeautifulSoup(src, 'html.parser')
    title_elements = soup.find_all('a', class_='title')
    titles_snimu = [element.text.strip() for element in title_elements]
    return titles_snimu

def get_descriptions_snimu(src):
    soup = BeautifulSoup(src, 'html.parser')
    description_elements = soup.find_all('p', class_='zam')
    descriptions_snimu = [element.text.strip() for element in description_elements]
    return descriptions_snimu

def get_image_urls_snimu(src):
    soup = BeautifulSoup(src, 'html.parser')
    thumbs_elements = soup.find_all('div', class_='thumbs')
    image_urls_snimu = []

    for element in thumbs_elements:
        image_elements = element.find_all('img')
        for img in image_elements:
            if 'src' in img.attrs:
                image_url = img['src']
                if "_thumbnail" in image_url:
                    image_url = image_url.replace("_thumbnail", "")
                image_urls_snimu.append(image_url)

    return image_urls_snimu

def save_to_csv(data, categories, titles, descriptions, image_urls):
    with open("result/data_snimu.csv", "a", encoding="utf-8", newline="") as file:
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
    if os.path.exists("result/data_snimu.csv"):
        os.remove("result/data_snimu.csv")

    for i in range(1, 5):
        url = f'http://jerdesh.ru/birge_snimu_komnatu_kojko_mesto/{i}'
        src_snimu = get_data_snimu(url)
        data_snimu = get_phones_and_names_snimu(src_snimu)
        categories_snimu = get_category_id_snimu(src_snimu)
        titles_snimu = get_titles_snimu(src_snimu)
        descriptions_snimu = get_descriptions_snimu(src_snimu)
        image_urls_snimu = get_image_urls_snimu(src_snimu)

        print(f"Page {i}:")

        print("Name and phone:")
        for item in data_snimu:
            print(item['name'], item['phone'])

        print("Categories:")
        for category in categories_snimu:
            print(category)

        print("Titles:")
        for title in titles_snimu:
            print(title)

        print("Descriptions:")
        for description in descriptions_snimu:
            print(description)

        print("Image URLs:")
        for url in image_urls_snimu:
            print(url)

        print()
        save_to_csv(data_snimu, categories_snimu, titles_snimu, descriptions_snimu, image_urls_snimu)

if __name__ == '__snimu__':
    main()
