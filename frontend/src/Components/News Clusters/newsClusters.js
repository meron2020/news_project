import React from 'react';
import NewsArticle from "../News Articles/newsArticle";
import MainNewsArticle from "../News Articles/mainNewsArticle";
import './newsClusters.css'


class ClusterId extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            numberOfitemsShown: 2,
            showCoverageButton: true
        }
    }

    showMore = () => {
        this.setState({numberOfitemsShown: this.props.id_cluster.length})
        this.setState({showCoverageButton: false})
    }

    render() {
        let itemsToShow = this.props.id_cluster.slice(1, this.state.numberOfitemsShown).map((item, index) =>
            <NewsArticle key={index} article={item}/>);

        return (
            <div className="newsClusters">
                <MainNewsArticle article={this.props.id_cluster[0]}/>
                <ul>
                    {itemsToShow}
                </ul>
                <div className="button-full-coverage">
                    {(this.state.showCoverageButton && this.props.id_cluster.length > 2) &&
                    <button onClick={this.showMore}>
                        Full Coverage
                    </button>}
                </div>
            </div>
        );
    }
}

export default ClusterId;