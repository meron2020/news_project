// import ReactTable from 'react-table'
import React from 'react';
import ServerConnection from "../serverConnection";

class scoreLogsPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tableData: [],
            columns: [{Header: 'First Url', accessor: 'first_url'},
                {Header: 'Second Url', accessor: 'second_url'},
                {Header: 'First Title', accessor: 'first_title'},
                {Header: 'Second Title', accessor: 'second_title'},
                {Header: 'Title Score', accessor: 'title_score'},
                {Header: 'Text Score', accessor: 'text_score'},
                {Header: 'Score', accessor: 'score'},
            ],
            loading: true
        }
        this.getScoreLogs = this.getScoreLogs.bind(this);
    }

    async componentDidMount() {
        await this.getScoreLogs().then(score => this.setState({tableData: score, loading: false}))
        this.splitArticlesToClusters()
    }

    async getScoreLogs() {
        return await ServerConnection.getScoreLogs().then(score => score)
    }

    render() {

        // if (this.state.loading === true) {
        //     return (
        //         <span>Loading Logs ... </span>
        //     )
        // }
        return (
            <div>
            {/*<div>*/}
            {/*    <ReactTable data={this.state.tableData} columns={this.state.columns}*/}
            {/*                defaultPageSize={2}*/}
            {/*                pageSizeOptions={[2, 4, 6, 8]}/>*/}
            {/*</div>*/}
            <h1>Score Logs</h1>
            </div>
    )
    }
}

export default scoreLogsPage;