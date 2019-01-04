import React, { Component } from 'react';
import './Nav.css';

class Nav extends Component {
  render() {
      var classNames = require('classnames');
      let nav_items = [];
      for (let i = 1; i <= 5; i++) {
          let classes = classNames(
              'nav-item', {
              'selected-nav-item': this.props.selectedNavItemId === i
          });
          nav_items.push(<div key={i} className={classes} onClick={() => this.props.onNavItemSelected(i)}>Item { i }</div>)
      }

    return (
        <div className={'nav'}>
            { nav_items }
        </div>
    );
  }
}

export default Nav;
