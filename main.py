import csv
import requests
from lxml import etree

def get_data(url):
    req = requests.get(url)
    with open("projects.html", "w", encoding="utf-8") as file:
        file.write(req.text)

    with open("projects.html", encoding="utf8") as file:
        src = file.read()
    return src

def get_phones(src):
    tree = etree.HTML(src)
    phone_elements = tree.xpath('//span[@class="protectedNumber"]')
    phones = [element.get('title', 'none') for element in phone_elements]
    return tuple(phones)

def get_category_id(src):
    tree = etree.HTML(src)
    category_elements = tree.xpath('//span[@class="category"]')
    categories = [element.text.strip() for element in category_elements]
    return tuple(categories)

def get_titles(src):
    tree = etree.HTML(src)
    title_elements = tree.xpath('//a[@class="title"]')
    titles = [element.text.strip() for element in title_elements]
    return tuple(titles)

def get_descriptions(src):
    tree = etree.HTML(src)
    description_elements = tree.xpath('//p[@class="zam"]')
    descriptions = [element.text.strip() for element in description_elements]
    return tuple(descriptions)

def save_to_csv(phones, categories, titles, descriptions):
    data = zip(phones, categories, titles, descriptions)

    with open("data.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Phone", "Category", "Title", "Description"])
        writer.writerows(data)

def main():
    for i in range(1, 101):
        url = f'http://jerdesh.ru/search/iPage,{i}'
        src = get_data(url)
        phones = get_phones(src)
        categories = get_category_id(src)
        titles = get_titles(src)
        descriptions = get_descriptions(src)

        print(f"Page {i}:")

        print("Phones:")
        for phone in phones:
            print(phone)

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

        save_to_csv(phones, categories, titles, descriptions)

if __name__ == '__main__':
    main()
