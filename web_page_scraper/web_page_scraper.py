import requests
from bs4 import BeautifulSoup
import string
import os


def get_user_input():

    while True:

        pages_input = input("Input the number of pages:\n> ")

        if not pages_input.isdigit():

            print("Invalid input! Enter a positive number.")
            continue

        pages = int(pages_input)

        if pages <= 0:

            print("Number must be greater than 0.")
            continue

        break

    while True:

        article_type = input("Input the article type:\n> ").strip()

        if article_type == "":

            print("Article type cannot be empty.")
            continue

        break

    return pages, article_type


def create_page_folder(page_number):

    folder_name = f"Page_{page_number}"

    if not os.path.exists(folder_name):

        os.mkdir(folder_name)

    return folder_name


def get_page(url):

    headers = {'Accept-Language': 'en-US,en;q=0.5'}

    try:

        response = requests.get(url, headers=headers)

        return response

    except requests.exceptions.RequestException:

        return None


def clean_title(title):

    translator = str.maketrans('', '', string.punctuation)

    title = title.translate(translator)

    title = title.replace(" ", "_")

    return title


def save_article(folder, title, content):

    filename = clean_title(title) + ".txt"

    path = os.path.join(folder, filename)

    with open(path, "wb") as file:

        file.write(content.encode("utf-8"))

    return filename


def parse_articles(pages, article_type):

    base_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2022&page="

    saved_articles = []

    for page in range(1, pages + 1):

        folder = create_page_folder(page)

        url = base_url + str(page)

        response = get_page(url)

        if response is None or response.status_code != 200:

            print(f"The URL returned {response.status_code if response else 'error'}!")

            continue

        soup = BeautifulSoup(response.content, "html.parser")

        articles = soup.find_all("article")

        for article in articles:

            type_tag = article.find("span", {"data-test": "article.type"})

            if not type_tag:

                continue

            if type_tag.text.strip() != article_type:

                continue

            link_tag = article.find("a", {"data-track-action": "view article"})

            if not link_tag:

                continue

            title = link_tag.text.strip()

            link = "https://www.nature.com" + link_tag.get("href")

            article_response = get_page(link)

            if article_response is None or article_response.status_code != 200:

                continue

            article_soup = BeautifulSoup(article_response.content, "html.parser")

            body = article_soup.find("div", {"class": lambda x: x and "body" in x})

            if not body:

                continue

            text = body.get_text().strip()

            filename = save_article(folder, title, text)

            saved_articles.append(filename)

    print("Saved all articles.")


def main():

    pages, article_type = get_user_input()

    parse_articles(pages, article_type)


main()

