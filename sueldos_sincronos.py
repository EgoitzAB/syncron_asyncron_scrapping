#!/usr/bin/python3
import requests
import time
from bs4 import BeautifulSoup

""" Bot who scrape syncronusly all the salaries of the majors of Spain. The code
is old and can be improved, but the main objetive is to compare the differente
scrapping methods an times."""

main_url = 'https://sueldode.org/'
links_partidos = []
new_url = []
referencias = []
partidos_url = []
referidos = []

def llamar_url(url):
    """ Function to get the url and return a soup objects """
    html = requests.get(url).text
    soup = BeautifulSoup(html, features ='lxml')
    return soup

def get_party_links():
    """ Function to get the links of the political parties appending to list """
    soup = llamar_url(main_url)
    link_parties = soup.find_all('a', class_="no-lightbox")
    for i in link_parties:
        link = i.get('href')
        links_partidos.append(link)

def make_urls():
    """ Refine the links of the urls and append to list """
    for i in links_partidos:
        acotar_link = i.strip()
        añadir_url = (f"{main_url}{acotar_link[1:]}")
        new_url.append(añadir_url)

def get_politburo():
    """ Get the links to each politic of spain, but I don't remember really in
    what position. """
    for url in new_url:
        sopa = llamar_url(url)
        nombre_personas = sopa.find_all('li')
        for nombre in nombre_personas:
            try:
                referencia = nombre.find('a', href=True)
                referencias.append(referencia['href'])
            except:
                continue

def main(url):
    """ Get the anual salary of each politic """
    urls = requests.get(url).text
    soup = BeautifulSoup(urls, 'lxml')
    nombre_vasallo = soup.find('article', {'id':True}).h1.string
    puesto_vasallo = soup.find('div', {'class' : 'entry-content'}).h2.text
    salario_vasallo = soup.find('strong').find_parent().text
    anual_vasallo = soup.find('strong').find_parent().find_next_sibling().text
    referidos.append(f"El vasallo cobra:\n {salario_vasallo} actuando como {puesto_vasallo}")
    referidos.append(f"Anualmente\n {anual_vasallo}.")


if __name__=='__main__':
    """ Print each formated politician syncronus and printing the
    spent time to compare """
    s = time.perf_counter()
    get_party_links()
    make_urls()
    get_politburo()
    for ref in referencias:
        main(ref)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
#710 secondes more or less
