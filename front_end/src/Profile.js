import React, { Component, useState } from 'react';
import { Message, Card, Input, Header, Divider, Button, Text } from "semantic-ui-react";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/'
})


class Profile extends Component{

    state = {
        items: [],
        loggedIn: false,
        username: '',
        email: ''
    }

    constructor() {
        super();
        if (localStorage.getItem("userID") != null) {
            this.getUser();
            this.state.loggedIn = true;
        }
    }

    getUser = () => {
        api.post('/users', {
            "u_id": parseInt(localStorage.getItem("userID"))
        }).then(res => {
            console.log("User:");
            console.log(res.data);
            this.setState({
                username: res.data["Username"],
                email: res.data["Email"]
            });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    render() {
        if (this.state.loggedIn) {
            return <>
                <Header as='h2'>Username</Header>
                <Header as='h4'> {this.state.username} </Header>
                <Button content='Change Username' color="yellow" onClick={() => { }} />
                <Divider />
                <Header as='h2'>Email</Header>
                <Header as='h4'> {this.state.email} </Header>
                <Button content='Change Email' color="yellow" onClick={() => { }} />
                <Divider /> 
                <Header as='h2'>Password</Header>
                <Button content='Change Password' color="yellow" onClick={() => { }} />
            </>
        } else {
            return <>
                <Message
                    header='You are not logged in!'
                    content='Please log in to view your profile.'
                />
            </>
        }
    }

    getUserCart = () => {
        api.post('/cart', {
            "u_id": parseInt(localStorage.getItem("userID"))
        }).then(res => {
            console.log(res.data);
            this.setState({
                items: res.data["Cart Items"],
                cartTotal: res.data["Cart Total"]
            });
        }).catch(error => {
            if (error.response.status == 404) {
                this.setState({ emptyCart: true });
            }
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }
}

export default Profile;