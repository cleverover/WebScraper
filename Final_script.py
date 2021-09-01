import requests
from bs4 import BeautifulSoup as bs
import re
import os

# that's the last and the most complicated part of project, so I decided to post only it

# get parameters from user
number_of_page = int(input())
type_of_article = input()

start_link = 'https://www.nature.com/nature/articles'
links_for_pages = [start_link]

start_r = requests.get(start_link)

# get links for the articles
if start_r.status_code == 200:
    current_soup = bs(start_r.content, 'html.parser')
    current_number = 1

    while current_number < number_of_page:
        current_number += 1

        page = current_soup.find('li', {'data-page': str(current_number)})
        link = 'https://www.nature.com' + page.find('a').get('href')
        links_for_pages.append(link)

        current_r = requests.get(link)
        current_soup = bs(current_r.content, 'html.parser')

# parse articles content and save it in new directory
# all articles from page number N will be saved in the "Page N" directory
for number, first_link in enumerate(links_for_pages):
    dir_name = 'Page_' + str(number + 1)
    os.mkdir(dir_name)

    response = requests.get(first_link)
    soup = bs(response.content, features="html.parser")
    articles = soup.find_all('article')
    for article in articles:
        title = article.find('a', attrs={'class': 'text-gray'}).text.strip()
        punctuation = r"―—–!\"#$%&'()*+,-./:;<=>?@[\]_^`{|}~"
        title = "".join(["_" if t == " " else t if t not in punctuation else "" for t in title])
        link = 'https://www.nature.com' + article.find('a', attrs={'class': 'text-gray'}).get('href')
        type = article.find('span', attrs={'data-test': 'article.type'}).text
        if type == type_of_article:
            response2 = requests.get(f"{link}")
            soup2 = bs(response2.content, features="html.parser")
            regex = re.compile('.*body.*')
            body = soup2.find('div', attrs={'class': regex})

            current_dir = os.getcwd()
            path_to_file = current_dir + '\\' + dir_name + '\\' + title + '.txt'
            with open(path_to_file, "wb") as file:
                file.write(str.encode(body.text).strip())
