import React, {Component, useState} from 'react';
import {Input, Card, Container, Divider, Header, Image, Tab} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Products from "./Products";
import Wishlist from "./Wishlist";
import Cart from "./Cart";

class MainView extends Component {

    state = {
        isAuth: true,
    }

    render() {

        console.log("Login Data:");
        console.log(localStorage.getItem("userID"));

        const panes = [
            {
                menuItem: 'Products', render: () =>
                    <Tab.Pane active={this.state.isAuth}>
                        <Products />
                    </Tab.Pane>
            },
            {
                menuItem: 'Wishlist', render: () => <Tab.Pane active={this.state.isAuth}><Wishlist /></Tab.Pane>
            },
            {
                menuItem: 'Cart', render: () =>
                    <Tab.Pane active={this.state.isAuth}>
                        <Cart />
                    </Tab.Pane>
            },
            {
                menuItem: 'Profile', render: () => <Tab.Pane active={this.state.isAuth}>:)</Tab.Pane>
            },
            {
                menuItem: 'Dashboard', render: () => <Tab.Pane active={this.state.isAuth}><Dashboard /></Tab.Pane>
            }
        ]
        return <>
            <Header dividing textAlign="center" size="huge">
                <Image circular size='medium' src='/man.png' /> RUMZON <Image size='medium' circular src='/man.png' />

            </Header>
            <Tab panes={panes} />
        </>
    }
}

export default MainView;
