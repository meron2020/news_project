import React from 'react';
import NewsTopics from "../Components/News Topics/newsTopics";
import NewsArticle from "../Components/News Articles/newsArticle";
import './TopicPage.css'

class TopicPage extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div className="TopicPage">
                <div className="topicTitle">
                <h1>{this.props.topicTitle}</h1>
                </div>
                <div className="NewsTopics">
                <NewsTopics topicName={this.props.topicName}/>
                </div>
            </div>
        )
}
}

export default TopicPage;