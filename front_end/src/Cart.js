import React, { Component, useState } from 'react';
import { Message, Card, Input, Container, Divider, Button, Icon, Table, TableCell, Header } from "semantic-ui-react";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/'
})


class Cart extends Component {

    state = {
        items: [],
        loggedIn: false,
        emptyCart: false,
        cartTotal: ''
    }

    constructor() {
        super();
        if (localStorage.getItem("userID") != null) {
            this.getUserCart();
            this.state.loggedIn = true;
        }
    }


    render() {
        if (this.state.loggedIn) {
            
            if (this.state.emptyCart) {
                return <>
                    <Message
                        header='Your cart is empty!'
                        content='Add some items to your cart.'
                    />
                </>
            }
            return <>
                <Header as='h1'>Your Cart</Header>
                <Container>
                    <Button color="green" animated='vertical' onClick={() => this.buyCart()}>
                        <Button.Content visible>Checkout</Button.Content>
                        <Button.Content hidden>
                            <Icon name='shop' />
                        </Button.Content>
                    </Button>
                    <Input
                        value={this.state.cartTotal}
                    />
                </Container>
                <Divider horizontal> </Divider>
                <Card.Group>
                    <this.CartCards info={this.state.items} />
                </Card.Group>
                <Divider horizontal> </Divider>
                <Button content='Clear Cart' color="red" onClick={() => { this.clearCart() }} />
            </>
        } else {
            return <>
                <Message
                    header='You are not logged in!'
                    content='Please log in to view your cart.'
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

    buyCart = () => {
        api.post('/cart/buy', {
            "u_id": parseInt(localStorage.getItem("userID"))
        }).then(res => {
            console.log(res.data);
            this.getUserCart();
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    clearCart = () => {
        api.delete('/cart/clear', {
            data: {
                "u_id": parseInt(localStorage.getItem("userID"))
            }
        }).then(res => {
            console.log(res.data);
            this.getUserCart();
        })
    }

    CartCards = (props) => {
        return props.info.map(item => {
            return <Card>
                <Card.Content>
                    <Card.Header>{item["Name"]}</Card.Header>
                    <Card.Meta>{item["Category"]}</Card.Meta>
                    <Card.Description>
                        {item["Price"]}
                    </Card.Description>
                    <this.AmmountButtons item={item} />
                    <Header as="h3" textAlign="right">{item["Item Total"]}</Header>
                    <Divider />
                    <Button content='Remove From Cart' color="red" onClick={() => { this.handleDeleteFromCart(item) }} />
                </Card.Content>
            </Card>
        });
    }

    AmmountButtons = (props) => {
        console.log("ammount buttons:");
        console.log(props);
        return <>
            <Table>
                <TableCell><Button fluid icon="minus" color="grey" onClick={() => { this.handleSubstractOneFromCart(props.item) }} /></TableCell>
                <TableCell><Header as='h4'>{" x".concat(props.item["Amount"])}</Header></TableCell>
                <TableCell><Button fluid icon="plus" color="grey" onClick={() => { this.handleAddToCart(props.item) }} /></TableCell>
            </Table>
        </>
    }

    handleDeleteFromCart = (item) => {
        api.delete('/cart', {
            data: {
                "item_id": item["Item ID"],
                "u_id": parseInt(localStorage.getItem("userID"))
            }
        }).then(res => {
            console.log(res.data);
            this.getUserCart();
        })
    }

    handleAddToCart = (item) => {
        api.post('/cart/add', {
            "item_id": item["Item ID"],
            "u_id": parseInt(localStorage.getItem("userID")),
            "c_amount": 1
        }).then(res => {
            console.log(res.data);
            this.getUserCart();
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            if (error.response.status == 400) {

            }
        })
    }

    handleSubstractOneFromCart = (item) => {
        if ((item["Amount"] - 1) > 0) {
            api.put('/cart', {
                "item_id": item["Item ID"],
                "u_id": parseInt(localStorage.getItem("userID")),
                "c_amount": item["Amount"] - 1
            }).then(res => {
                console.log(res.data);
                this.getUserCart();
            })
        } else {
            this.handleDeleteFromCart(item);
        }
    }

    handleUpdateCart = (item, newAmount) => {
        if (newAmount > 0) {
            api.put('/cart', {
                "item_id": item["Item ID"],
                "u_id": parseInt(localStorage.getItem("userID")),
                "c_amount": newAmount
            }).then(res => {
                console.log(res.data);
                this.getUserCart();
            })
        } else {
            this.handleDeleteFromCart(item);
        }
    }
}

export default Cart;