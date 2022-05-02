import bs4
import requests
from nltk.corpus import wordnet
import random

def banner():
    print("""
    ██╗    ██╗██╗██╗  ██╗██╗██████╗  ██████╗ ████████╗
    ██║    ██║██║██║ ██╔╝██║██╔══██╗██╔═══██╗╚══██╔══╝
    ██║ █╗ ██║██║█████╔╝ ██║██████╔╝██║   ██║   ██║
    ██║███╗██║██║██╔═██╗ ██║██╔══██╗██║   ██║   ██║
    ╚███╔███╔╝██║██║  ██╗██║██████╔╝╚██████╔╝   ██║
     ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝    ╚═╝

    A bot for the Wikipedia link game.
    Author: Noxtal
    """)

def printpath(word, similarity, url):
    print(f"└> {word} with {similarity:.3f} ({url})")

def main():
    banner()
    s = input("Starting point: ")
    e = input("Ending point: ")

    origin = f'https://en.wikipedia.org/wiki/{s}'
    destin = f'https://en.wikipedia.org/wiki/{e}'

    print("\nPATH")

    response = requests.get(origin)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    printpath(soup.title.text[:-12], 1, origin)

    url = origin

    response = requests.get(destin)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    objective = wordnet.synsets(soup.title.text[:-12])[0]

    i = 0
    tried = []
    while True:
        if url == destin:
            break

        response = requests.get(url)

        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        links = soup.select('a')

        best_similarity = 0
        best_word = ""
        for link in links:
            href = link.get("href")
            word = link.get_text()

            if href:
                href = href.lower()

                if 'https://en.wikipedia.org' + href != url and href.startswith("/wiki/") and "wiki" in href \
                        and "disambiguation" not in href and ":" not in href and "#" not in href:

                    sw = wordnet.synsets(word)
                    if sw:
                        choice = sw[0]
                        j = 1
                        valid = True
                        while choice in tried:
                            if j >= len(sw):
                                valid = False
                                break
                            choice = sw[j]
                            j+=1

                        if valid:
                            tried.append(choice)
                            similarity = choice.wup_similarity(objective)
                            if similarity > best_similarity:
                                best_similarity = similarity
                                url = 'https://en.wikipedia.org' + href
                                best_word = word

        i += 1
        printpath(best_word, best_similarity, url)

    print(f"\n DONE IN {i} iterations.")

if __name__ == '__main__':
    main()
