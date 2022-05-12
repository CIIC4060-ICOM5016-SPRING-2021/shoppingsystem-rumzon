import React, { Component } from 'react';
import { Button, Card, Header, Message, Icon } from "semantic-ui-react";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/'
})

class Orders extends Component {

    state = {
        orders: [],
        loggedIn: false,
        orderId: null,
        currOrder: []
    }

    render() {
        if (this.state.loggedIn) {
            if (this.state.orderId === null) {
                return <>
                    <Header as='h1'>Order History</Header>
                    <Card.Group>
                        <this.OrderCards orders={this.state.orders} />
                    </Card.Group>
                </>
            } else {
                return <>
                    <this.OrderPage order={this.state.currOrder} />
                </>
            }
        } else {
            return <>
                <Message
                    header='You are not logged in!'
                    content='Please log in to view your order history.'
                />
            </>
        }
    }

    constructor() {
        super();
        if (localStorage.getItem("userID") != null) {
            this.getOrders();
            this.state.loggedIn = true;
        }
    }

    getOrders = () => {
        api.post('/orders/user', {
            "u_id": parseInt(localStorage.getItem("userID"))
        }).then(res => {
            console.log(res.data);
            this.setState({ orders: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }


    OrderCards = (props) => {
        console.log(props)
        return props.orders.map(order => {
            return <Card>
                <Card.Content>
                    <Card.Header>{"Order# ".concat(order["Order ID"])}</Card.Header>
                    <Card.Content>{order["Order Total"]}</Card.Content>
                    <Card.Description>
                        {order["Order Time"]}
                    </Card.Description>
                </Card.Content>
                <Card.Content extra>
                    <div className='ui two buttons'>
                        <Button content='View Order' color="grey" onClick={() => {
                            this.setState({
                                orderId: order["Order ID"],
                                currOrder: this.state.orders.find(orderInList => orderInList["Order ID"] == order["Order ID"])
                            })
                        }} />
                    </div>
                </Card.Content>
            </Card>
        });
    }

    OrderPage = (props) => {
        console.log(props)
        return <>
            <Button color="grey" animated='horizontal' onClick={() => this.setState({
                orderId: null,
                currOrder: []
            })}>
                <Button.Content visible>Return to All Orders</Button.Content>
                <Button.Content hidden>
                    <Icon name='arrow left' />
                </Button.Content>
            </Button>
            <Header as='h1'>{"Order# ".concat(props.order["Order ID"])}</Header>
            <this.OrderItems items={props.order["Items in Order"]} />
            <Header as='h2'>{"Order Total: ".concat(props.order["Order Total"])}</Header>
            <Header as='h2'>{"Time of Order: ".concat(props.order["Order Time"])}</Header>
        </>
    }

    OrderItems = (props) => {
        return props.items.map(item => {
            var itemPrice = ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ";
            itemPrice = this.setCharAt(itemPrice, 0, 'x'.concat(item['Amount']));
            itemPrice = this.setCharAt(itemPrice, (itemPrice.length - 1 - item['Item Total'].length), ' '.concat(item['Item Total']));
            return <>
                <Header as='h3' textAlign='justified'>
                    {item['Item Name']}
                    <Header sub>
                        { item['Category']}
                        <Header as='h4' textAlign='justified'>
                            {itemPrice}
                        </Header>
                    </Header>
                </Header>
            </>
        });
    }

    setCharAt = (str, index, chr) => {
        if (index > str.length - 1) return str;
        return str.substring(0, index) + chr + str.substring(index + chr.length);
    }
}

export default Orders;