import React, { Component, useState } from 'react';
import { Message, Card, Button, Header, Popup } from "semantic-ui-react";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon'
})


class Wishlist extends Component {

    state = {
        items: [],
        loggedIn: false,
        emptyWishlist: false
    }

    constructor() {
        super();
        if (localStorage.getItem("userID") != null) {
            this.getUserWishlist();
            this.state.loggedIn = true;
        }
    }


    render() {
        if (this.state.loggedIn) {
            
            if (this.state.emptyWishlist) {
                return <>
                    <Message
                        header='Your wishlist is empty!'
                        content='Add some items to your wishlist.'
                    />
                </>
            }
            return <>
                <Header as='h1'>Your Wishlist</Header>
                <Card.Group>
                    <this.WishlistCards info={this.state.items} />
                </Card.Group>
            </>
        } else {
            return <>
                <Message
                    header='You are not logged in!'
                    content='Log in or create a new account to view your wishlist.'
                />
            </>
        }
    }

    getUserWishlist = () => {
        api.post('/likes/users', {
            "u_id": parseInt(localStorage.getItem("userID"))
        }).then(res => {
            console.log("wishlist:");
            console.log(res.data);
            this.setState({ items: res.data });
        }).catch(error => {
            if (error.response.status == 405) {
                this.setState({ emptyWishlist: true });
            }
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }

    WishlistCards = (props) => {
        console.log(props)
        return props.info.map(item => {
            return <Card style={{wordWrap: "break-word"}}>
                <Card.Content>
                    <Card.Header>{item["Name"]}</Card.Header>
                    <Card.Meta>{item["Price"]}</Card.Meta>
                    <Card.Description>
                        {item["Category"]}
                    </Card.Description>
                </Card.Content>
                <Card.Content extra>
                    <div className='ui two buttons'>
                        <Popup
                            trigger={
                                <Button content='Add to Cart' color="green" onClick={() => { this.handleAddToCart(item) }} />
                            }
                            content='Added to Cart!'
                            position='bottom center'
                            on='click'
                        />
                        <Button content='Remove From Wishlist' color="red" onClick={() => { this.handleDeleteFromWishlist(item) }} />
                    </div>
                </Card.Content>
            </Card>
        });
    }

    handleDeleteFromWishlist = (item) => {
        api.delete('/likes', {
            data: {
                "item_id": item["Item ID"],
                "u_id": parseInt(localStorage.getItem("userID"))
            }
        }).then(res => {
            console.log(res.data);
            this.getUserWishlist();
        })
    }
    handleAddToCart = (item) => {
        api.post('/cart/add', {
            "item_id": item["Item ID"],
            "u_id": parseInt(localStorage.getItem("userID")),
            "c_amount" : 1
        }).then(res => {
            console.log(res.data);
        })
    }
}

export default Wishlist;