import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import Navbar from './Components/Navbar';
import TopicPage from "./Pages/TopicPage";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.topics = [""]
        this.state = {
            newsArticles: []
        }
    }

    render() {
        return (<div className="App">
            <>
                <Router>
                    <Navbar/>
                    <Switch>
                        <Route path="/military" component={() => <TopicPage topicTitle="Military" topicName="military"/>}/>
                        <Route path="/general" component={() => <TopicPage topicTitle="General" topicName="general"/>}/>
                        <Route path="/law" component={() => <TopicPage topicTitle="Law" topicName="law"/>}/>
                        <Route path="/palestine" component={() => <TopicPage topicTitle="Palestine" topicName="palestine"/>}/>
                        <Route path="/world" component={() => <TopicPage topicTitle="World" topicName="world"/>}/>
                        <Route path="/state_and_politics" component={() => <TopicPage topicTitle="State and Politics" topicName="state and politics"/>}/>
                        <Route path="/health_and_education" component={() => <TopicPage topicTitle="Health and Education" topicName="health and education"/>}/>
                    </Switch>
                </Router>
            </>

        </div>)

    }
}

export default App;
