import React, { Component, useState } from 'react';
import { Message, Card, Input, Container, Divider, Button, Icon, Dimmer, Loader, Segment } from "semantic-ui-react";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/'
})


class Cart extends Component{

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
        api.delete('/cart/buy', {
            data: {
                "u_id": parseInt(localStorage.getItem("userID"))
            }
        }).then(res => {
            console.log(res.data);
            this.getUserCart();
        })
    }

    CartCards = (props) => {
        console.log(props)
        return props.info.map(item => {
            return <Card>
                <Card.Content>
                    <Card.Header>{item["Name"]}</Card.Header>
                    <Card.Meta>{item["Category"]}</Card.Meta>
                    <Card.Description>
                        {item["Price"]}{" x".concat(item["Amount"])}
                    </Card.Description>
                    <Card.Description >
                        {item["Item Total"]}
                    </Card.Description>
                </Card.Content>
                <Card.Content extra>
                    <div className='ui two buttons'>
                        <Button content='Remove From Cart' color="red" onClick={ () => {this.handleDeleteFromCart(item)}}/>
                    </div>
                </Card.Content>
            </Card>
        });
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
}

export default Cart;