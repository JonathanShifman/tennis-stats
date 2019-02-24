import React, { Component } from 'react';
import './Grid.css';
import Stat from '../stat/Stat'

class Grid extends Component {
  render() {
    return (
        <div id={'stats-grid'}>
            <Stat />
            <Stat />
            <Stat />
            <Stat />
        </div>
    );
  }
}

export default Grid;
