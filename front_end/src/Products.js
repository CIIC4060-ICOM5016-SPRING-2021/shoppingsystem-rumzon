import React, { Component, useState, useEffect } from 'react';
import { Button, Card, Container, Modal, Tab } from "semantic-ui-react";
import AllProducts from "./AllProducts";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/items/'
})


class Products extends Component{

    state = {
        items: []
    }

    constructor() {
        super();
        this.sortNameAscending()
    }


    render() {
        return <>
            <Button onClick={this.sortNameDescending}>Name Descending</Button>
            <Button onClick={this.sortNameAscending}>Name Ascending</Button>
            <Button onClick={this.sortPriceDescending}>Price Descending</Button>
            <Button onClick={this.sortPriceAscending}>Price Ascending</Button>
            <Card.Group>
            <AllProducts info={this.state.items} />
            </Card.Group>
            </>
    }

    sortNameDescending = () => {
        api.post('/sort', { "sortBy": "name", "sortType": "descending" }).then(res => {
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
        api.post('/sort', { "sortBy": "name", "sortType": "ascending" }).then(res => {
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
        api.post('/sort', { "sortBy": "price", "sortType": "descending" }).then(res => {
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
        api.post('/sort', { "sortBy": "price", "sortType": "ascending" }).then(res => {
            console.log(res.data);
            this.setState({ items: res.data });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            console.log(error.message);
        })
    }
}

export default Products;