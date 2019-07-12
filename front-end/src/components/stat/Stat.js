import React, { Component } from 'react';
import './Stat.css';
import flag from '../../assets/flags/sui.jpg';
import star from '../../assets/icons/star.png';
import func from './circle';

class Stat extends Component {
    componentDidMount() {
        func(this.props.num);
        // var circle = new ProgressBar.Circle('#progress');
        // circle.animate(1);
    }

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
                <div className={'stat-number'} id={'progress' + this.props.num}>
                    {/*71*/}
                </div>
                <div className={'stat-text'}>
                    71% of points won behind first serve
                </div>
            </div>
        </div>
    );
  }
}

export default Stat;
