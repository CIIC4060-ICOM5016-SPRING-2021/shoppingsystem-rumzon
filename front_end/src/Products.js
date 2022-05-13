import React, { Component } from 'react';
import { Button, Card, Container, Icon, Menu, Divider, Dropdown } from "semantic-ui-react";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/'
})

const categories = [
    { key: 0, text: 'All', value: 'all' },
    { key: 1, text: 'Clothes', value: 'clothes' },
    { key: 2, text: 'Electronics', value: 'electronics' },
    { key: 3, text: 'Food', value: 'food' },
    { key: 4, text: 'Furniture', value: 'furniture' },
    { key: 5, text: 'Household', value: 'household' },
    { key: 6, text: 'Kitchenware', value: 'kitchenware' },
    { key: 7, text: 'Medicine', value: 'medicine' },
    { key: 8, text: 'Pets', value: 'pets' },
    { key: 9, text: 'Sports', value: 'sports' },
    { key: 10, text: 'Supplies', value: 'supplies' },
    { key: 11, text: 'Toys', value: 'toys' },
]

class Products extends Component {

    state = {
        items: [],
        category: 'all'
    }

    constructor() {
        super();
        this.sortNameAscending(this.state.category);
    }


    render() {
        return <>
            <Container alignment="left">
                <Menu secondary>
                    
                    <Menu.Item>
                        <Button onClick={() => this.sortNameAscending(this.state.category)}><Icon name='sort alphabet up' />Name Ascending</Button>
                    </Menu.Item>
                    <Menu.Item>
                        <Button onClick={() => this.sortNameDescending(this.state.category)}><Icon name='sort alphabet down' />Name Descending</Button>
                    </Menu.Item>
                    <Menu.Item>
                        <Button onClick={() => this.sortPriceAscending(this.state.category)}><Icon name='sort numeric up' />Price Ascending</Button>
                    </Menu.Item >
                    <Menu.Item>
                        <Button onClick={() => this.sortPriceDescending(this.state.category)}><Icon name='sort numeric down' />Price Descending</Button>
                    </Menu.Item>
                    <Menu.Item>
                        <Menu compact>
                            <Dropdown
                                placeholder='Filter Category'
                                icon='filter'
                                floating
                                labeled
                                button
                                className='icon'
                                options={categories}
                                name='category'
                                onChange={this.handleCategoryDropdown} />
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

    handleCategoryDropdown = (e, { name, value }) => {
        this.sortNameAscending(value)
        this.setState({ [name]: value })
        }

    sortNameDescending = (value) => {
        api.post('/items/sort', { "sortBy": "name", "sortType": "descending", "category": value }).then(res => {
            console.log(res.data);
            this.setState({ items: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }
    sortNameAscending = (value) => {
        api.post('/items/sort', { "sortBy": "name", "sortType": "ascending", "category": value }).then(res => {
            console.log(res.data);
            this.setState({ items: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }
    sortPriceDescending = (value) => {
        api.post('/items/sort', { "sortBy": "price", "sortType": "descending", "category": value }).then(res => {
            console.log(res.data);
            this.setState({ items: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }
    sortPriceAscending = (value) => {
        api.post('/items/sort', { "sortBy": "price", "sortType": "ascending", "category": value }).then(res => {
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