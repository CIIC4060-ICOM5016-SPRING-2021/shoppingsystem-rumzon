import React, { Component, useState, useEffect } from 'react';
import { Button, Card, Container, Modal, Tab } from "semantic-ui-react";
import AllProducts from "./AllProducts";
import axios from "axios";


const [gotItens, setGotItens] = useState(false);
const [items, setItems] = useState([]);

function Products() {


    if (!gotItens) {
        let arr = []
        axios.get('https://rumzon-db.herokuapp.com/rumzon/items/all').then(res => {
            res.data.forEach((item) => {
                const newItem = {
                    id: item["Item ID"],
                    name: item["Item Name"],
                    price: item["Price"],
                    stock: item["Stock"],
                    category: item["Category"]
                };
                arr.push(newItem);
            })
        })
        setGotItens(true);
    }

    return <Card.Group>
        <AllProducts info={theArray} />
    </Card.Group>
}

export default Products;