#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import time
import asyncio
from aiohttp import ClientSession

""" Exercise to implement syncronus, asyncronus and pararell scrapping. I am
reusing my first bot done months ago, so the data and methods are a little bit
rudimentary and without so much knowledge of python. """

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
    soup = BeautifulSoup(url, 'lxml')
    nombre_vasallo = soup.find('article', {'id':True}).h1.string
    puesto_vasallo = soup.find('div', {'class' : 'entry-content'}).h2.text
    salario_vasallo = soup.find('strong').find_parent().text
    anual_vasallo = soup.find('strong').find_parent().find_next_sibling().text
    referidos.append(f"El vasallo cobra:\n {salario_vasallo} actuando como {puesto_vasallo}")
    referidos.append(f"Anualmente\n {anual_vasallo}.")

def fetch_async(urls):
    """ Function who coordinates the coroutines """
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_all(urls))
    loop.run_until_complete(future)

async def fetch_all(urls):
    """ Function who make task pool """
    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)

async def fetch(url, session):
    """ Function to return response object from url to fill the tasks """
    async with session.get(url) as response:
        r = await response.text()
        return main(r)

if __name__=='__main__':
    """ Print each formated politician with aiohttp and asyncio and printing the
    spent time to compare """
    s = time.perf_counter()
    get_party_links()
    make_urls()
    get_politburo()
    fetch_async(referencias)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
#30 seconds more or less
