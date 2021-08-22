import React from "react";
import NewsArticle from "../News Articles/newsArticle";
import {Row} from 'reactstrap';
import ServerConnection from "../../serverConnection";


class NewsTopics extends React.Component {
    constructor(props) {
        super(props);
        this.topicName = props.topicName
        this.state = {
            articleList:[],
            NewsArticleComponentList: []
        }
        this.getTopicNews = this.getTopicNews.bind(this)
        this.addArticlesToList = this.addArticlesToList.bind(this)


    }

    addArticlesToList() {
        this.state.articleList.forEach((item, index) => {
            this.setState( {
            NewsArticleComponentList: this.state.NewsArticleComponentList.concat([<NewsArticle article={item}/>])})
        })
    }

     async componentDidMount() {
        await this.getTopicNews().then(news => this.setState({articleList: news}))
    }

    async getTopicNews() {
        return await ServerConnection.getNews(this.topicName).then(news => news)}


    render() {
        if (this.state.articleList.length === 0) {
            return (
                <span>Loading Articles ... </span>
            )}
        let articleList = this.state.articleList.map((item, index) => (<NewsArticle key={index} article={item}/>))
        return (
            <div className="NewsTopicList">
                {articleList}
            </div>
    )
    }
}

export default NewsTopics;