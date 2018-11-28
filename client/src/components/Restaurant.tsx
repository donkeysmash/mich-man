import * as React from "react";

export class Restaurants extends React.Component<any, object> {
  state = {
    currentRestaurants: [] as any
  };

  onChangeHandler = (e: any) => {
    this.setState({
      currentRestaurants: values.filter(v => v['name'].includes(e.target.value) && e.target.value.length > 0)
    });
  };

  render() {
    const results = [];
    for (const x of this.state.currentRestaurants) {
      const result =
        <div key={x['name']}>
          <div>{x['address']}</div>
          <div>{x['country']}</div>
          <div>{x['latitude']}</div>
          <div>{x['longitude']}</div>
        </div>;
      results.push(result);
  }
  return (
    <div>
      {/* <h1>Hello from {this.props.compiler} and {this.props.framework}!</h1>
      <h2>{this.state.currentValue}</h2> */}
      <input
        type='text'
        onChange={this.onChangeHandler}
      />
      {results}
    </div>
  )
}
}

const values = [
{
    "address": "U Milosrdn\u00fdch 12, Praha, 110 00",
    "country": "cz",
    "cuisine": "Modern cuisine",
    "latitude": "50.0919",
    "longitude": "14.42193",
    "name": "Field",
    "neighborhood": "Praha",
    "num_star": 1,
    "price_range": "From CZK1,160.00",
    "url": "https://guide.michelin.com/cz/field/restaurant",
    "website": "http://www.fieldrestaurant.cz"
  },
  {
    "address": "Ha\u0161talsk\u00e1 18, Praha, 110 00",
    "country": "cz",
    "cuisine": "Modern cuisine",
    "latitude": "50.09115",
    "longitude": "14.42511",
    "name": "La Degustation Boh\u00eame Bourgeoise",
    "neighborhood": "Praha",
    "num_star": 1,
    "price_range": "From CZK3,450.00",
    "url": "https://guide.michelin.com/cz/la-degustation-boheme-bourgeoise/restaurant",
    "website": "http://www.ladegustation.cz"
  }
]