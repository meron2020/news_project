import React from "react";
import NewsArticle from "../News Articles/newsArticle";
import {Row} from 'reactstrap';
import ServerConnection from "../../serverConnection";
import ClusterId from "../News Clusters/newsClusters";


class NewsTopics extends React.Component {
    constructor(props) {
        super(props);
        this.topicName = props.topicName
        this.state = {
            articleList:[],
            NewsArticlesClustersDict: {},
            ClusterDictFilled: false
        }
        this.getTopicNews = this.getTopicNews.bind(this)
        this.addElementToClusterDict = this.addElementToClusterDict.bind(this)

    }

    addElementToClusterDict(cluster ,element) {
        if (cluster in this.state.NewsArticlesClustersDict) {
            let newsArticleDict = this.state.NewsArticlesClustersDict
            newsArticleDict[cluster].push(element)
            this.setState({NewsArticleClusterDict:newsArticleDict})
        }
        else {
            let newsArticleDict = this.state.NewsArticlesClustersDict
            newsArticleDict[cluster] = [element]
            this.setState({NewsArticleClusterDict:newsArticleDict})
        }

    }

    splitArticlesToClusters() {
        this.state.articleList.map((item, index) =>
            this.addElementToClusterDict(item['cluster_id'], item))

        this.setState({ClusterDictFilled:true})
    }

     async componentDidMount() {
        await this.getTopicNews().then(news => this.setState({articleList: news}))
         this.splitArticlesToClusters()
    }

    async getTopicNews() {
        return await ServerConnection.getNews(this.topicName).then(news => news)}


    render() {
        if (this.state.ClusterDictFilled === false) {
            return (
                <span>Loading Articles ... </span>
            )}

        let clustersList = []
        for (const [key, value] of Object.entries(this.state.NewsArticlesClustersDict)) {
            clustersList.push(<ClusterId id_cluster={value}/>)
        }
        return (
            <div className="NewsTopicList">
                {clustersList}
            </div>
    )
    }
}

export default NewsTopics;