import * as React from "react";
import { Restaurants } from "./Restaurant";

export interface HelloProps {
  compiler: string;
  framework: string;
}

// export const Hello = (props: HelloProps) => <h1>Hello from {props.compiler} and {props.framework}!</h1>;


export class Hello extends React.Component<HelloProps, object> {
  state = {
    currentValue: ""
  };

  onChangeHandler = (e:any) => {
    this.setState({
      currentValue: e.target.value
    });
  };

  // onChangeHandler(e) {
  //   this.setState({
  //     currentValue: e.target.value
  //   });
  // }

  render() {
    return (
      <div>
        <h1>Hello from {this.props.compiler} and {this.props.framework}!</h1>
        {/* <h2>{this.state.currentValue}</h2>
        <input
          type='text'
          onChange={this.onChangeHandler}
        /> */}
        <Restaurants />
      </div>
    )
  }
}