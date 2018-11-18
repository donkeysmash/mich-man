import re
import requests
import json
from bs4 import BeautifulSoup

def main():
  by_country('fr')
  by_country('it')
  by_country('es')

def by_country(country):
  detail_urls = construct_restaurant_urls(country)
  all_restaurants = []
  for detail_url in detail_urls:
    all_restaurants.append(scape_restaurant_detail_page(detail_url, country))
  with open(f'{country}2018.json', 'w') as fp:
    json.dump(all_restaurants, fp, sort_keys=True, indent=2)


def scape_restaurant_detail_page(url, country):
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  name = soup.find('h1').text.strip()
  print(name)
  num_stars_str = soup.find('ul', {'class': 'michelin-poi-distinctions-list'}).find('div', {'class': 'content-wrapper'}).text
  num_star = int(re.search('[1-3]', num_stars_str).group(0))
  neighborhood = soup.find('span', {'class': 'locality'}).text.strip()
  price_range_str = soup.find('div', {'class': 'poi_intro-display-prices'}).text.strip()
  price_range = re.search('[0-9]+.*', price_range_str).group(0)
  cuisine = soup.find('div', {'class': 'node_poi-cooking-types'}).text.strip()
  address_pieces = soup.find('div', {'class': 'field--name-field-address'}).find_all(text=True)
  address_pieces = filter(lambda x: x != ' ', address_pieces)
  address = ', '.join(address_pieces)
  website = safe_website(soup)
  coor = re.search(r'maps\.google\.com/\?q=([0-9.,-]+)', str(soup)).group(1).split(',')

  restaurant = {
    'country': country,
    'name': name,
    'num_star': num_star,
    'neighborhood': neighborhood,
    'price_range': price_range,
    'cuisine': cuisine,
    'address': address,
    'url': url,
    'website': website,
    'latitude': coor[0],
    'longitude': coor[1]
  }

  return restaurant

def safe_website(soup):
  try:
    return soup.find('div', {'class': 'website'}).find('a')['href']
  except Exception:
    return ''



def construct_restaurant_urls(country):
  num_stars = [1, 2, 3]
  results = []
  for num_star in num_stars:
    is_ended = False
    page_count = 1
    while not is_ended:
      url = gen_list_url(country, num_star, page_count)
      print(url)
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
      cards = soup.find('ul', {'class': 'poi-search-result'}).find_all('li', recursive=False)
      for card in cards:
        results.append(f'{base_url(country)}{card.a["href"]}')
      print(len(cards))
      if len(cards) < 18:
        is_ended = True
      page_count += 1

  return results

def base_url(country):
  if country == 'fr':
    return f'https://restaurant.michelin.fr'

  if country == 'it':
    return f'https://guida.michelin.it'

  if country == 'es':
    return f'https://guia.michelin.es'

def gen_list_url(country, num_stars, page_count):
  if country == 'fr':
    plural = 's' if num_stars > 1 else ''
    return f'{base_url(country)}/restaurants/france/restaurants-{num_stars}-etoile{plural}-michelin/page-{page_count}'

  if country == 'it':
    plural = 'e' if num_stars > 1 else 'a'
    return f'{base_url(country)}/ristoranti/italia/ristoranti-{num_stars}-stell{plural}-michelin/pagina-{page_count}'

  if country == 'es':
    plural = 's' if num_stars > 1 else ''
    return f'{base_url(country)}/restaurantes/espana/restaurantes-{num_stars}-estrella{plural}/pagina-{page_count}'


if __name__ == '__main__':
  main()
