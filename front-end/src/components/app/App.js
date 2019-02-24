import React, {Component, Fragment} from 'react';
import './App.css';
import Nav from "../nav/Nav";
import Grid from "../grid/Grid";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedNavItemId: 0,
            content: <Grid/>,
        };

        this.selectNavItem = this.selectNavItem.bind(this);
    }

    render() {
        return (
            <Fragment>
                {/*<Nav onNavItemSelected={this.selectNavItem} selectedNavItemId={this.state.selectedNavItemId} />*/}
                { this.state.content }
            </Fragment>
        );
    }

    selectNavItem(selectedNavItemId) {
        this.setState({
            selectedNavItemId: selectedNavItemId
        }, () => this.updateContent());
    }

    updateContent() {
        let content = null;
        if (this.state.selectedNavItemId === 1) {
            content = <Grid/>
        }
        this.setState({
            content: content
        })
    }

}

export default App;
