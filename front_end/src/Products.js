import React, { Component, useState, useEffect, Link } from 'react';
import { Button, Card, Container, Icon, Menu, Divider, Dropdown, DropdownItem , ListItem} from "semantic-ui-react";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/'
})

const options = [
    { key: 1, text: 'All', value: 1, as: Link, to: '/all'},
    { key: 2, text: 'Clothes', value: 2, as: Link, to: '/clothes'},
    { key: 3, text: 'Elecronics', value: 3, as: Link, to: '/electronics' },
    { key: 4, text: 'Food', value: 4, as: Link, to: '/food' },
    { key: 5, text: 'Furniture', value: 5, as: Link, to: '/furniture' },
    { key: 6, text: 'Household', value: 6, as: Link, to: '/household' },
    { key: 7, text: 'Kitchenware', value: 7, as: Link, to: '/kitchenware' },
    { key: 8, text: 'Medicine', value: 8, as: Link, to: '/medicine' },
    { key: 9, text: 'Pets', value: 9, as: Link, to: '/pets' },
    { key: 10, text: 'Sports', value: 10, as: Link, to: '/sports' },
    { key: 11, text: 'Supplies', value: 11, as: Link, to: '/supplies' },
    { key: 12, text: 'Toys', value: 12, as: Link, to: '/toys' },
  ]
  
class Products extends Component{

    state = {
        items: [],
        category: ''
    }

    constructor() {
        super();
        this.sortNameAscending();
    }


    render() {
        return <>
            <Container alignment="left">
                <Menu secondary>
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
                <Menu.Item>
                    <Menu compact>
                        <Dropdown placeholder ='Categories' options={options} fluid single selection />   
                    </Menu>
                </Menu.Item>
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

    sortByCategory = () => {
        api.get('/items/category'.concat(this.state.category)).then(res => {
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
                    <Card.Description>
                        {"In Stock: ".concat(item["Stock"])}
                    </Card.Description>
                </Card.Content>
                <Card.Content extra>
                    <div className='ui two buttons'>
                        <Button content='Add to Cart' color="green" onClick={() => { this.handleAddToCart(item) }} />
                        <Button content='Add to Wishlist' color="blue" onClick={() => { this.handleAddToWishlist(item) }} />
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

export default Products;