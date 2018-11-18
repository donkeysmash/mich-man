import requests
import json
from bs4 import BeautifulSoup

root_url = 'https://guide.michelin.com'

def main():
  collect_us()
  collect_br()
  collect_possible_eu()
  collect_possible_asia()

  all_restaurants = scrape('sg')
  with open(f'sg2018.json', 'w') as fp:
    json.dump(all_restaurants, fp, sort_keys=True, indent=2)

def collect_br():
  br_cities = ['rio-de-janeiro', 'sao-paulo']
  collect_by_cities('br', br_cities)

def collect_us():
  us_cities = ['chicago', 'new-york', 'san-francisco', 'washington-dc']
  collect_by_cities('us', us_cities)

def collect_possible_asia():
  collect_by_cities('th', ['bangkok'])
  collect_by_cities('hk', ['hong-kong-macau'])
  collect_by_cities('tw', ['taipei'])
  sgs = scrape('sg')
  with open(f'sg2018.json', 'w') as fp:
    json.dump(sgs, fp, sort_keys=True, indent=2)


def collect_possible_eu():
  all_possible_countries = ['at', 'cz', 'hr', 'dk', 'fi', 'gr', 'hu', 'is', 'no', 'pl', 'se']
  for country in all_possible_countries:
    all_restaurants = scrape(country)
    with open(f'{country}2018.json', 'w') as fp:
      json.dump(all_restaurants, fp, sort_keys=True, indent=2)

def collect_by_cities(country, cities):
  all_restaurants = []
  for city in cities:
    all_restaurants = all_restaurants + scrape(country, city)
  with open(f'{country}2018.json', 'w') as fp:
    json.dump(all_restaurants, fp, sort_keys=True, indent=2)

def visit_details(restaurants):
  for restaurant in restaurants:
    url = restaurant['url']
    name = restaurant['name']
    print(f'{name} @ {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    address_texts = soup.find('div', {'class': 'location-item__desc'}).find_all('p')[1].text.strip().split(',')
    address = ', '.join(map(lambda x: x.strip(), address_texts))
    restaurant['address'] = address
    info_list = soup.find_all('a', {'class': 'o-link'})
    if (len(info_list) > 1):
      restaurant['website'] = soup.find_all('a', {'class': 'o-link'})[1]['href']
    else:
      restaurant['website'] = ''
  return restaurants

def scrape(country, city=''):
  num_stars_str = ['1-star', '2-stars', '3-stars']
  num_stars = [1, 2, 3]

  result = []
  for num_star_str, num_star in zip(num_stars_str, num_stars):
    is_ended = False
    page_count = 1
    while not is_ended:
      if city != '':
        base_url = f'{root_url}/{country}/{city}'
      else:
        base_url = f'{root_url}/{country}'
      url = f'{base_url}/{num_star_str}-michelin/restaurants/page/{page_count}'
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
      restaurants_container = soup.find('div', {'class': 'grid-restaurants-new_right'})
      rs = restaurants_container.find_all('div', {'class': 'grid-restaurants-new_right_item nested-link'})
      print(f'fetched {url}\n  {len(rs)}')
      for restaurant in rs:
        restaurant_url = restaurant.a['href']
        extracted = extract_restaurant_info(restaurant)
        extracted['url'] = f'{root_url}{restaurant_url}'
        extracted['country'] = country
        extracted['num_star'] = num_star
        result.append(extracted)

      if len(rs) < 30:
        is_ended = True
      page_count += 1

  visit_details(result)
  return result


def extract_restaurant_info(restaurant):
  name = restaurant.find('div', {'class': 'resto-inner-title'}).a.find(text=True, recursive=False).strip()
  categories = restaurant.find('div', {'class': 'resto-inner-category'}).find(text=True, recursive=False).split('·')
  cuisine = categories[0].strip()
  neighborhood = categories[1].strip()
  price_range = categories[2].strip()
  return dict(
    name=name,
    cuisine=cuisine,
    neighborhood=neighborhood,
    price_range=price_range,
    latitude=restaurant['data-latitude'],
    longitude=restaurant['data-longitude']
  )


if __name__ == '__main__':
  main()
