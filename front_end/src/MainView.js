import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { Segment, Header, Image, Tab, Menu, Button } from "semantic-ui-react";
import Products from "./Products";
import Wishlist from "./Wishlist";
import Cart from "./Cart";
import Profile from "./Profile";
import UserStats from "./UserStats";
import GlobalStats from "./GlobalStats";
import AdminPage from "./AdminPage";
import Orders from "./Orders";
import "./index.css";


function MainView() {

    const navigate = useNavigate();
    const [isAuth, setisAuth] = useState(true);
    console.log(localStorage.getItem('userID'));
    console.log(localStorage.getItem('username'));
    console.log(localStorage.getItem('isAdmin'));
    const panes = [
        {
            menuItem: 'Products', render: () =>
                <Tab.Pane active={isAuth}>
                    <Products />
                </Tab.Pane>
        },
        {
            menuItem: 'Wishlist', render: () =>
                <Tab.Pane active={isAuth}>
                    <Wishlist />
                </Tab.Pane>
        },
        {
            menuItem: 'Cart', render: () =>
                <Tab.Pane active={isAuth}>
                    <Cart />
                </Tab.Pane>
        },
        {
            menuItem: 'Profile', render: () =>
                <Tab.Pane active={isAuth}>
                    <Profile />
                </Tab.Pane>
        }, {
            menuItem: 'Orders', render: () =>
                <Tab.Pane active={isAuth}>
                    <Orders />
                </Tab.Pane>
        }, {
            menuItem: 'User Statistics', render: () =>
                <Tab.Pane active={isAuth}>
                    <UserStats />
                </Tab.Pane>
        },
        {
            menuItem: 'Global Statistics', render: () =>
                <Tab.Pane active={isAuth}>
                    <GlobalStats />
                </Tab.Pane>
        }
    ]

    if (localStorage.getItem("isAdmin") === 'true') {
        console.log("Not Admin");
        panes.push({
            menuItem: 'Manage Products', render: () =>
                <Tab.Pane active={isAuth}>
                    <AdminPage />
                </Tab.Pane>
        })
    } else {
        console.log("Not Admin");
    }


    return <>
        <Segment inverted >
            <Menu inverted>
                <Menu.Item color='red'>
                    <Segment inverted >
                        <Header
                            as='h1'
                            textAlign='center'
                            style={{
                                fontSize: '5em',
                                fontWeight: 'bold',
                                color: '#2ed24b'
                            }}> <Image rounded style={{ width: '85px' }} src='/rumzon-logo.jpeg' /> UMZON </Header>
                    </Segment>
                </Menu.Item>

                <LoginButtons />
            </Menu>
            <Tab
                menu={{ color: 'green', inverted: true, attached: true, tabular: true }}
                panes={panes}
            />
        </Segment>
    </>


    function signIn() {
        navigate('/login');
    }
    function signOut() {
        localStorage.removeItem("userID");
        localStorage.removeItem("Username");
        localStorage.removeItem("IsAdmin");
        window.location.reload(false);
    }

    function LoginButtons() {
        if (localStorage.getItem("userID") != null) {
            return <Menu.Item position='right'>
                <Header inverted as='h1' style={{
                    fontSize: '2em',
                    fontWeight: 'bold',
                    marginRight: '0.5em',
                    paddingTop: '0.65em'
                }}>
                    {"Hello, ".concat(localStorage.getItem("username")).concat("!")}
                </Header>
                <Button content='Sign out' icon='log out' color='grey' onClick={signOut} />
            </Menu.Item >
        } else {
            return <Menu.Item position='right'>
                <Button as='a' onClick={signIn} content='Sign out' icon='log out' color='green'>
                    Sign in
                </Button>
            </Menu.Item>
        }
    }
}
export default MainView;
