import requests
import json
import re
from bs4 import BeautifulSoup

countries = [
  {
    'url': 'https://fr.viamichelin.be',
    'page': '/web/Restaurants/Restaurants-Belgique',
    'code': 'be'
  },
  {
    'url': 'https://www.viamichelin.de',
    'page': '/web/Restaurants/Restaurants-Germany',
    'code': 'de'
  },
  {
    'url': 'https://www.viamichelin.co.uk',
    'page': '/web/Restaurants/Restaurants-United_Kingdom',
    'code': 'gb'
  },
  {
    'url': 'https://www.viamichelin.ie',
    'page': '/web/Restaurants/Restaurants-Ireland',
    'code': 'ie'
  },
  {
    'url': 'https://fr.viamichelin.be',
    'page': '/web/Restaurants/Restaurants-Luxembourg',
    'code': 'lu'
  },
  {
    'url': 'https://www.viamichelin.nl',
    'page': '/web/Restaurants/Restaurants-Nederland',
    'code': 'nl'
  },
  {
    'url': 'https://www.viamichelin.pt',
    'page': '/web/Restaurantes/Restaurantes-Portugal',
    'code': 'pt'
  },
  {
    'url': 'https://de.viamichelin.ch',
    'page': '/web/Restaurants/Restaurants-Schweiz',
    'code': 'ch'
  },
  {
    'url': 'https://www.viamichelin.com',
    'page': '/web/Restaurants/Restaurants-Shanghai-_-Shanghai-China',
    'code': 'cn'
  },
  {
    'url': 'https://www.viamichelin.com',
    'page': '/web/Restaurants/Restaurants-Seoul-_-Seoul_Jikhalsi-South_Korea',
    'code': 'kr'
  }
]

def main():
  for country_info in countries:
    scrape(country_info)

def scrape(country_info):
  base_url = country_info['url']
  country = country_info['code']
  list_page_url = f'{base_url}{country_info["page"]}'
  num_stars = [1, 2, 3]
  result = []
  for num_star in num_stars:
    is_ended = False
    page_count = 1
    while not is_ended:
      url = f'{list_page_url}?stars={num_star}&page={page_count}'
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
      rs = soup.find_all('li', {'class': 'poi-item-restaurant'})
      print(f'fetched {url}\n  {len(rs)}')
      for restaurant in rs:
        info = {
          'url': f'{base_url}{restaurant.a["href"]}',
          'country': country,
          'name': restaurant.a.text,
          'num_star': num_star
        }
        result.append(info)

      if len(rs) < 24:
        is_ended = True
      page_count += 1

  visit_details(result)
  with open(f'{country}2018.json', 'w') as fp:
    json.dump(result, fp, sort_keys=True, indent=2)

def safe_website(soup):
  texts = soup.find('ul', {'class': 'datasheet-more-infos'}).text.split()
  maybe_website = list(filter(lambda x: x.startswith('http') or x.startswith('www'), texts))
  if len(maybe_website) > 0:
    return maybe_website[0]
  return ''

def visit_details(restaurants):
  for restaurant in restaurants:
    url = restaurant['url']
    name = restaurant['name']
    print(f'{name} @ {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    restaurant['cuisine'] = ','.join(soup.find('div', {'class': 'datasheet-infos-cooking-type'}).text.strip().split('|'))
    address_raw = soup.find('div', {'class': 'datasheet-infos-address'}).em.text.strip().split()
    restaurant['address'] = ' '.join(address_raw)
    restaurant['neighborhood'] = address_raw[-1]
    restaurant['price_range'] =  ' '.join(soup.find('div', {'class': 'datasheet-price'}).text.split())
    restaurant['website'] = safe_website(soup)
    m = re.search(r'"latitude":"([0-9.-]+)"', str(soup))
    restaurant['latitude'] = m.group(1)
    m = re.search(r'"longitude":"([0-9.-]+)"', str(soup))
    restaurant['longitude'] = m.group(1)





if __name__ == '__main__':
  main()
