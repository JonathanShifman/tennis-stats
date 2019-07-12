import React, { Component } from 'react';
import './Grid.css';
import Stat from '../stat/Stat'

class Grid extends Component {
  render() {
    return (
        <div id={'stats-grid'}>
            <Stat num={1} />
            <Stat num={2} />
            <Stat num={3} />
            <Stat num={4} />
        </div>
    );
  }
}

export default Grid;
