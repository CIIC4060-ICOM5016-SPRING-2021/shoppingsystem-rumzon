import React, { Component, useState, useEffect } from 'react';
import { Button, Card, Container, Icon, Menu, Divider } from "semantic-ui-react";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/'
})


class Admin extends Component{

    state = {
        items: []
    }

    constructor() {
        super();
        this.sortNameAscending();
    }


    render() {
        return <>
            <Container alignment="left">
                <Menu secondary widths={4}>
                    <Menu.Item>
                <Button onClick={this.sortNameDescending}>
                <Button.Content visible><Icon name='sort alphabet down' />Name Descending</Button.Content>
                </Button>
                </Menu.Item>
                <Menu.Item>
                <Button onClick={this.sortNameAscending}><Icon name='sort alphabet up' />Name Ascending</Button>
                </Menu.Item>
                <Menu.Item>
                <Button onClick={this.sortPriceDescending}><Icon name='sort numeric down' />Price Descending</Button>
                </Menu.Item>
                <Menu.Item>
                <Button onClick={this.sortPriceAscending}><Icon name='sort numeric up' />Price Ascending</Button>
                    </Menu.Item >
                </Menu>

                <Divider hidden />

            </Container>
            <Card.Group>
                <this.ProductCards info={this.state.items} />
            </Card.Group>
            </>
    }

    sortNameDescending = () => {
        api.post('/items/sort', { "sortBy": "name", "sortType": "descending" }).then(res => {
            console.log(res.data);
            this.setState({ items: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }
    sortNameAscending = () => {
        api.post('/items/sort', { "sortBy": "name", "sortType": "ascending" }).then(res => {
            console.log(res.data);
            this.setState({ items: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }
    sortPriceDescending = () => {
        api.post('/items/sort', { "sortBy": "price", "sortType": "descending" }).then(res => {
            console.log(res.data);
            this.setState({ items: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }
    sortPriceAscending = () => {
        api.post('/items/sort', { "sortBy": "price", "sortType": "ascending" }).then(res => {
            console.log(res.data);
            this.setState({ items: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }

    ProductCards = (props) => {
        console.log(props)
        return props.info.map(item => {
            return <Card>
                <Card.Content>
                    <Card.Header>{item["Item Name"]}</Card.Header>
                    <Card.Meta>{item["Price"]}</Card.Meta>
                    <Card.Description>
                        {item["Category"]}
                    </Card.Description>
                </Card.Content>
                <Card.Content extra>
                    <div className='ui two buttons'>
                        <Button content='Modify Product' color="blue" onClick={() => { console.log("PPPUPU") }} />
                        <Button content='Delete Product' color="red" onClick={() => { SVGFEMorphologyElement() }} />
                    </div>
                </Card.Content>
            </Card>
        });
    }

    handleAddToCart = (item) => {
        api.post('/cart/add', {
            "item_id": item["Item ID"],
            "u_id": parseInt(localStorage.getItem("userID")),
            "c_amount": 1
        }).then(res => {
            console.log(res.data);
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            if (error.response.status == 400) {

            }
        })
    }
    handleAddToWishlist = (item) => {
        api.post('/likes', {
            "item_id": item["Item ID"],
            "u_id": parseInt(localStorage.getItem("userID"))
        }).then(res => {
            console.log(res.data);
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }
}

export default Admin;