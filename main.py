import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_data(url):
    req = requests.get(url)
    with open("projects.html", "w", encoding="utf-8") as file:
        file.write(req.text)

    with open("projects.html", encoding="utf8") as file:
        src = file.read()
    return src

def get_phones_and_names(src):
    soup = BeautifulSoup(src, 'html.parser')
    phone_elements = soup.find_all('span', class_='protectedNumber')

    phones = []
    names = []

    for element in phone_elements:
        phone = element.get('title', 'none')
        name = ''
        prev_sibling = element.find_previous_sibling()

        while prev_sibling is not None:
            if prev_sibling.name == 'span' and prev_sibling.find('img') and prev_sibling.find('img')['src'] == '/img/icons/person.gif':
                name = prev_sibling.next_sibling.strip()
                break
            prev_sibling = prev_sibling.previous_sibling

        phones.append(phone)
        names.append(name)

    return names, phones

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

def save_to_csv(names, phones, categories, titles, descriptions):
    data = zip(names, phones, categories, titles, descriptions)
    
    now = datetime.now()
    timestamp = now.strftime("%d_%m_%Y_%H_%M_%S")
    filename = f"data_{timestamp}.csv"
    
    try:
        with open("data.csv", "x"):
            pass
        file_exists = False
    except FileExistsError:
        file_exists = True
    
    if file_exists:
        with open(filename, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["name", "phone", "category", "title", "description"])
            writer.writerows(data)
    else:
        with open("data.csv", "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["name", "phone", "category", "title", "description"])
            writer.writerows(data)

def main():
    for i in range(1, 101):
        url = f'http://jerdesh.ru/search/iPage,{i}'
        src = get_data(url)
        names, phones = get_phones_and_names(src)
        categories = get_category_id(src)
        titles = get_titles(src)
        descriptions = get_descriptions(src)

        print(f"Page {i}:")
        print("Phones:")
        for phone in phones:
            print(phone)

        print("Names:")
        for name in names:
            print(name)

        print("Categories:")
        for category in categories:
            print(category)

        print("Titles:")
        for title in titles:
            print(title)

        print("Descriptions:")
        for description in descriptions:
            print(description)
        print()

        save_to_csv(names, phones, categories, titles, descriptions)

if __name__ == '__main__':
    main()
