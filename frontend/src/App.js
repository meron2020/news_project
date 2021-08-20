import React from 'react';
import './App.css';
import ServerConnection from './serverConnection'

class App extends React.Component {
    constructor(props) {
        super(props);
        this.topics = [""]
        this.state = {
            newsArticles: []
        }
    }

    getNews() {
        ServerConnection.getNews().then(news => {
            this.setState({newsArticles: news})
        })
    }
}
//     render() {
//
//     }
// }

// export default App;
