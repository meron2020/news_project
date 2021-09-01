import React from "react";
import {Row, Col} from 'reactstrap';
import "../../App.css"
import {SidebarData} from "./SidebarData";

function Sidebar() {
    return (
        <div className="Sidebar">
            <ul className="SidebarList">
                {SidebarData.map((val, key) => {
                    return <li key={key} className="row"
                               id={window.location.pathname === val.link ? "active": ""} onClick={() => {
                        window.location.pathname = val.link
                    }}>
                        <Col className="text-center">
                            {val.icon} {val.title}
                        </Col>
                    </li>

                })}
            </ul>
        </div>
    );
}

export default Sidebar;