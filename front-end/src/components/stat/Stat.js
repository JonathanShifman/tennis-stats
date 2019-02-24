import React, { Component } from 'react';
import './Stat.css';
import flag from '../../assets/flags/sui.jpg';
import star from '../../assets/icons/star.png';

class Stat extends Component {
  render() {
    return (
        <div className={'stat'}>
            <div className={'stat-header'}>
                <div className={'stat-player-wrapper'}>
                    <div className={'stat-player-flag'}>
                        <img src={flag} />
                    </div>
                    <div className={'stat-player-name'}>
                        Roger Federer
                    </div>
                </div>
                <div className={'stat-kind-icon'}>
                    <img src={star} />
                </div>
            </div>

            <div className={'stat-content'}>
                <div className={'stat-number'}>71</div>
                <div className={'stat-text'}>
                    Roger Federer has won 71% of points behind his first serve.
                </div>
            </div>
        </div>
    );
  }
}

export default Stat;
