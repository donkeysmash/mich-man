import requests
import json
from bs4 import BeautifulSoup

def main():
  collect_us()
  collect_br()
  collect_possible_eu()
  collect_possible_asia()



def collect_possible_asia():
  collect_by_cities('th', ['bangkok'])
  collect_by_cities('hk', ['hong-kong-macau'])
  collect_by_cities('tw', ['taipei'])

def collect_possible_eu():
  all_possible_countries = ['at', 'cz', 'hr', 'dk', 'fi', 'gr', 'hu', 'is', 'no', 'pl', 'se']
  all_restaurants = []
  for country in all_possible_countries:
    all_restaurants = all_restaurants + scrape(country)
  with open(f'eu2018.json', 'w') as fp:
    json.dump(all_restaurants, fp, sort_keys=True, indent=2)

def collect_by_cities(region, cities):
  all_restaurants = []
  for city in cities:
    all_restaurants = all_restaurants + scrape(region, city)
  with open(f'{region}2018.json', 'w') as fp:
    json.dump(all_restaurants, fp, sort_keys=True, indent=2)

def collect_br():
  br_cities = ['rio-de-janeiro', 'sao-paulo']
  collect_by_cities('br', br_cities)

def collect_us():
  us_cities = ['chicago', 'new-york', 'san-francisco', 'washington-dc']
  collect_by_cities('us', us_cities)


def scrape(country, city=''):
  num_stars_str = ['1-star', '2-stars', '3-stars']
  num_stars = [1, 2, 3]

  result = []
  for num_star_str, num_star in zip(num_stars_str, num_stars):
    is_ended = False
    page_count = 1
    while not is_ended:
      if city != '':
        url = f'https://guide.michelin.com/{country}/{city}/{num_star_str}-michelin/restaurants/page/{page_count}'
      else:
        url = f'https://guide.michelin.com/{country}/{num_star_str}-michelin/restaurants/page/{page_count}'
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
      restaurants_container = soup.find('div', {'class': 'grid-restaurants-new_right'})
      rs = restaurants_container.find_all('div', {'class': 'grid-restaurants-new_right_item nested-link'})
      print(f'fetched {url}\n  {len(rs)}')
      for restaurant in rs:
        extracted = extract_restaurant_info(restaurant)
        extracted['num_star'] = num_star
        extracted['city'] = city
        extracted['country'] = country
        result.append(extracted)

      if len(rs) < 30:
        is_ended = True
      page_count += 1

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
