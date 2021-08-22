import React from "react";
import LocalHospitalIcon from '@material-ui/icons/LocalHospital';
import PublicIcon from '@material-ui/icons/Public';
import LocationOnIcon from '@material-ui/icons/LocationOn';
import GavelIcon from '@material-ui/icons/Gavel';
import SecurityIcon from '@material-ui/icons/Security';
import HomeIcon from '@material-ui/icons/Home';
import FlagIcon from '@material-ui/icons/Flag';
import PolicyIcon from '@material-ui/icons/Policy';
export const SidebarData = [
    {
        title: "Military",
        icon: <SecurityIcon/>,
        path: "/military",
        cName: 'nav-text'
    },
    {
        title: "World",
        icon: <PublicIcon/>,
        path: "/world",
        cName: 'nav-text'
    },
    {
        title: "State and Politics",
        icon: <PolicyIcon/>,
        path: "/state_and_politics",
        cName: 'nav-text'
    },
    {
        title: "Palestine",
        icon: <FlagIcon/>,
        path: "/palestine",
        cName: 'nav-text'
    },
    {
        title: "General",
        icon: <LocationOnIcon/>,
        path: "/general",
        cName: 'nav-text'
    },
    {
        title: "Law",
        icon: <GavelIcon/>,
        path: "/law",
        cName: 'nav-text'
    },

    {
        title: "Health and Education",
        icon: <LocalHospitalIcon/>,
        path: "/health_and_education",
        cName: 'nav-text'
    },
]
