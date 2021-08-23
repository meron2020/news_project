import React from "react";
import './newsArticle.css'


class NewsArticle extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div className="NewsArticleWithLink">
            <a href={this.props.article["url"]}>
            <div className="NewsArticle">
                <article>
                        <h5>{this.props.article["title"]}</h5>
                        <h6>{this.props.article["newspaper"]}</h6>
                </article>
            </div>
            </a>
            </div>
        )
    }
}

export default NewsArticle;