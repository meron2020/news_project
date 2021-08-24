import React from "react";
import './newsArticle.css'


class MainNewsArticle extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div className="NewsArticleWithLink">
                <a href={this.props.article["url"]} target="_blank" rel="noreferrer noopener">
                    <div className="NewsArticle">
                        <article>
                            <h3>{this.props.article["title"]}</h3>
                            <h6>{this.props.article["newspaper"]}</h6>
                        </article>
                    </div>
                </a>
            </div>
        )
    }
}

export default MainNewsArticle;