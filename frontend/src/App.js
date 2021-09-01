import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import Navbar from './Components/SideBar/Navbar';
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
                    <div className="NavBar">
                    <Navbar/>
                    </div>
                    <Switch>
                        <Route path="/military" component={() => <TopicPage topicTitle="צבא וביטחון" topicName="military"/>}/>
                        <Route path="/general" component={() => <TopicPage topicTitle="כללי" topicName="general"/>}/>
                        <Route path="/law" component={() => <TopicPage topicTitle="משפט ופלילים" topicName="law"/>}/>
                        <Route path="/palestine" component={() => <TopicPage topicTitle="פלסטינים" topicName="palestine"/>}/>
                        <Route path="/world" component={() => <TopicPage topicTitle="חדשות בעולם" topicName="world"/>}/>
                        <Route path="/state_and_politics" component={() => <TopicPage topicTitle="מדיני-פוליטי" topicName="state and politics"/>}/>
                        <Route path="/health_and_education" component={() => <TopicPage topicTitle="בריאות וחינוך" topicName="health and education"/>}/>
                    </Switch>
                </Router>
            </>

        </div>)

    }
}

export default App;
