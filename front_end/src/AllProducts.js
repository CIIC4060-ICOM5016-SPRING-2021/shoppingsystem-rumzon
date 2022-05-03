import React, { Component, useState } from 'react';
import { Button, Card, Container, Modal, Tab } from "semantic-ui-react";

function AllProducts(props) {
    console.log(props)
    return props.info.map(value => {
        return <Card>
            <Card.Content>
                <Card.Header>{value["Item Name"]}</Card.Header>
                <Card.Meta>{value["Price"]}</Card.Meta>
                <Card.Description>
                    {value["Category"]}
                </Card.Description>
            </Card.Content>
            <Card.Content extra>
                <div className='ui two buttons'>
                    <Button basic color='green'>
                        Add to Wish List
                    </Button>
                    <Button basic color='yellow'>
                        Add to Cart
                    </Button>
                </div>
            </Card.Content>
        </Card>
    });
}
export default AllProducts;