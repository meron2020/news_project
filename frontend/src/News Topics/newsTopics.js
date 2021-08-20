import React from "react";
import NewsArticle from "../News Articles/newsArticle";
import {Row} from 'reactstrap';


class NewsTopics extends React.Component {
    constructor(props) {
        super(props);
        this.topicName = props.topicName
        this.articleList = []
    }

    addArticlesToList() {
        this.props.articleList.forEach((item, index) => {
            this.articleList.push(<NewsArticle article={item}/>)
        })
    }

    render() {
        return (
            <div>
                <Row>
                    <h2>{this.topicName}</h2>
                </Row>
            <div className="NewsTopicList">
                {this.articleList}
            </div>
            </div>
    )
    }
}

export default NewsTopics;