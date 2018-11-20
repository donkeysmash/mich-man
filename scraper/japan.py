import re
import requests
import json
from bs4 import BeautifulSoup

country = 'jp'

def main():
  base_urls = get_all_base_urls()
  urls = get_all_urls(base_urls)
  restaurants = []
  for url in urls:
    restaurants = restaurants + visit_list(url)
  print(f'collected and now visiting {len(restaurants)} restaurants')
  for restaurant in restaurants:
    scrape(restaurant)
  with open(f'{country}2018.json', 'w') as fp:
    json.dump(restaurants, fp, sort_keys=True, indent=2)



def scrape(restaurant):
  url = restaurant['url']
  res = requests.get(concat_url(url, 'map/'))
  soup = BeautifulSoup(res.text, 'html.parser')
  info_cont = soup.find('div', {'id': 'rInfo'})
  price_cont = info_cont.find('dl', {'class': 'price'})
  price_range = '' if price_cont is None else price_cont.dd.text.strip()
  address_cont = info_cont.find('dl', {'class': 'address'})
  address = '' if address_cont is None else address_cont.dd.text.strip()
  website_cont = info_cont.find('dl', {'class': 'url'})
  website = '' if website_cont is None else website_cont.a['href']
  restaurant['price_range'] = price_range
  restaurant['address'] = address
  restaurant['website'] = website
  coords = re.search(r'maps\.google\.com/maps\?q=([0-9.-]+)%2C([0-9.-]+)', str(soup))
  if len(coords.groups()) == 2:
    restaurant['latitude'] = coords[0]
    restaurant['longitude'] = coords[1]


def visit_list(base_url):
  root_url = re.search(r'(https://[^/]+)/.*', base_url).group(1)
  num_stars = [1, 2, 3]
  result = []
  for num_star in num_stars:
    page_count = 1
    is_ended = False
    while not is_ended:
      url = f'{base_url}all_area/all_small_area/all_food/{num_star}star/p{page_count}/'
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
      restaurants_list = soup.find('ul', {'id': 'restaurantList'})
      region = soup.h3.text
      if restaurants_list is None:
        break
      else:
        restaurants_list = restaurants_list.find_all('li', recursive=False)
        print(f'{url}\n   {len(restaurants_list)}')
      for restaurant_info in restaurants_list:
        cuisine_and_neighborhood = [x for x in restaurant_info.dd.text.split('\n') if len(x.strip()) > 0]
        restaurant = {
          'name': restaurant_info.a.text,
          'num_star': num_star,
          'url': concat_url(root_url, restaurant_info.a['href']),
          'neighborhood': cuisine_and_neighborhood[1].strip(),
          'cuisine': cuisine_and_neighborhood[0].strip(),
          'country': country,
          'region': region
        }
        result.append(restaurant)
      page_strings = soup.find('div', {'id': 'resultPager'}).var.text.split()
      last_page = int(page_strings[0].split('-')[1])
      total_page = int(page_strings[-1])
      if (last_page == total_page):
        is_ended = True
      page_count += 1
  return result


def concat_url(a, b):
  a = a[:-1] if a.endswith('/') else a
  b = b[1:] if b.startswith('/') else b
  return f'{a}/{b}'


def get_all_urls(urls):
  result = []
  for url in urls:
    response = requests.get(f'{url}/restaurant')
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find('div', {'id': 'selectArea'}).find_all('a')
    hrefs = set(map(lambda x : concat_url(url, x['href']), links))
    result = result + list(hrefs)
  return result


def get_all_base_urls():
  url = 'https://guide.michelin.co.jp/'
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  links = soup.find('div', {'class': 'map-box'}).find_all('a')
  hrefs = set(map(lambda x : x['href'], links))
  cleaned_urls = []
  for href in hrefs:
    match = re.search(r'(https?://[A-z0-9.-]+)/.*$', href)
    cleaned_urls.append(str(match.group(1)))
  print(f'extracted: {len(hrefs)}')
  return cleaned_urls

if __name__ == '__main__':
  main()
