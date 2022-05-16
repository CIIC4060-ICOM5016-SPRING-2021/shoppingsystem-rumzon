import React, { Component } from 'react';
import { Button, Card, Container, Icon, Menu, Divider, Dropdown, Header, Popup} from "semantic-ui-react";
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
        wishlist: [],
        category: 'all'
    }

    constructor() {
        super();
        this.sortNameAscending(this.state.category);
        this.getUserWishlist();
    }


    render() {
        return <>
            <Header as='h1'>Rumzon Catalog</Header>
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
            
            this.setState({ items: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }

    getUserWishlist = () => {
        api.post('/likes/users', {
            "u_id": parseInt(localStorage.getItem("userID"))
        }).then(res => {
            console.log("wishlist:");
            console.log(res.data);
            this.setState({ wishlist: res.data });
        }).catch(error => {
            if (error.response.status == 405) {
                this.setState({ wishlist: [] });
            }
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }

    ProductCards = (props) => {
        console.log(props)
        return props.info.map(item => {
            return <Card style = {{ wordWrap: "break-word" }}>
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
                        <Popup
                            trigger={
                                <Button content='Add to Cart' color="green" onClick={() => { this.handleAddToCart(item) }} />
                            }
                            content='Added to Cart!'
                            position='bottom center'
                            on='click'
                        />
                        { this.handleWishlistBtn(item) }
                    </div>
                </Card.Content>
            </Card>
        });
    }

    handleWishlistBtn = (item) => {
        let isLiked = false
        this.state.wishlist.map(itemLiked => {
            if(itemLiked["Item ID"] === item["Item ID"]) {
                isLiked = true
            }
        })
        if(isLiked) {
            return (<Button content='Remove from Wishlist' color="yellow" onClick={() => { this.handleRemoveFromWishlist(item) }} />);
        }
        return (<Button content='Add to Wishlist' color="blue" onClick={() => { this.handleAddToWishlist(item) }} />)
    }

    handleRemoveFromWishlist = (item) => {
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
            "c_amount": 1
        }).then(res => {
            console.log(res.data);
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }
    
    handleAddToWishlist = (item) => {
        api.post('/likes', {
            "item_id": item["Item ID"],
            "u_id": parseInt(localStorage.getItem("userID"))
        }).then(res => {
            console.log(res.data);
            this.getUserWishlist();
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }
}

export default Products;