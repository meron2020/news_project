import React from "react";
import { Container, Row, Col} from 'reactstrap';


class NewsArticle extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div className="NewsArticle">
                <Row>
                    <Col>
                        <h4><a href={this.props.article["url"]}>{this.props.article["title"]}</a></h4>
                    </Col>
                    <Col>
                        <h5><a href="https://www.ynet.co.il/news">Ynet</a></h5>
                    </Col>
                </Row>
            </div>
        )
    }
}

export default NewsArticle;