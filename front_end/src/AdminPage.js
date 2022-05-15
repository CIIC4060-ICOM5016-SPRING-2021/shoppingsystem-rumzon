import React, { Component } from 'react';
import { Button, Card, Container, Icon, Menu, Divider, Dropdown, Modal, Form, Message, Header } from "semantic-ui-react";
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

class AdminPage extends Component {

    state = {
        items: [],
        category: 'all',
        editItem: false,
        itemID: '',
        itemName: '',
        itemCategory: '',
        itemStock: '',
        itemPrice: '',
        error: 0,
        deleteItem: false,
        addItem: false
    }

    constructor() {
        super();
        this.sortNameAscending(this.state.category);
        if (localStorage.getItem("userID") != null) {
            this.state.loggedIn = true;
        }
    }

    render() {
        return <>
            <Container alignment="left">
                <this.EditItemModal />
                <this.AddItemModal />
                <this.deleteModal />
                <Menu secondary>
                    <Menu.Item>
                        <Button color='blue' onClick={() => this.setState({ addItem: true })}><Icon name='add' />Add Item</Button>
                    </Menu.Item>
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
                            search
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
                        <Button content='Modify Product' color="blue" onClick={() => { this.openEditModal(item) }} />
                        <Button content='Delete Product' color="red" onClick={() => {
                            this.setState({
                                deleteItem: true,
                                itemID: item["Item ID"]
                            }) }} />
                    </div>
                </Card.Content>
            </Card>
        });
    }

    openEditModal = (item) => {
        console.log(item);
        api.post('/items',
            {
                "item_id": item["Item ID"],
            }).then(res => {
                console.log(res);
                this.setState({
                    itemID: item["Item ID"],
                    itemName: res.data["Item Name"],
                    itemCategory: res.data["Category"],
                    itemStock: res.data["Stock"],
                    itemPrice: res.data["Price"].substring(1),
                    editItem: true
                });
            }).catch(error => {
                console.log(error.response.data);
                console.log(error.response.status);
            })
    }

    EditItemModal = () => {
        return <Modal
            open={this.state.editItem}
        >
            <Modal.Header>Modify Product</Modal.Header>
            <Modal.Content>
                <Form>
                    <Form.Input
                        icon='pencil alternate'
                        iconPosition='left'
                        label='Item Name'
                        placeholder='Name'
                        value={this.state.itemName}
                        error={(this.state.error === 5 && this.state.itemName === '')}
                        onChange={input => this.setState({ itemName: input.target.value })}
                    />
                    <Form.Input
                        icon='dollar sign'
                        iconPosition='left'
                        label='Price'
                        placeholder='Price'
                        value={this.state.itemPrice}
                        error={(this.state.error === 5 && this.state.itemPrice === '')}
                        onChange={input => this.setState({ itemPrice: input.target.value })}
                    />
                    <Form.Input
                        icon='boxes'
                        iconPosition='left'
                        label='Stock'
                        placeholder='Stock'
                        value={this.state.itemStock}
                        error={(this.state.error === 5 && this.state.itemStock === '')}
                        onChange={input => this.setState({ itemStock: input.target.value })}
                    />
                    <Header as="h4">Category</Header>
                    <Dropdown
                        icon='th'
                        floating
                        labeled
                        button
                        className='icon'
                        options={categories}
                        value={this.state.itemCategory}
                        name='category'
                        onChange={this.handleCategoryEdit} />
                </Form>
                <Message
                    hidden={this.state.error != 1}
                    color={'red'}
                    header='Item name and category pair already exist.'
                />
                <Message
                    hidden={this.state.error != 2}
                    color={'red'}
                    header='Please enter a valid stock ammount.'
                />
                <Message
                    hidden={this.state.error != 3}
                    color={'red'}
                    header='Please enter a valid price.'
                />
                <Message
                    hidden={this.state.error != 4}
                    color={'red'}
                    header='Please fill out the form.'
                />
            </Modal.Content>
            <Modal.Actions>
                <Button color='black' onClick={() =>
                    this.setState({
                        itemID: '',
                        itemName: '',
                        itemCategory: '',
                        itemStock: '',
                        itemPrice: '',
                        editItem: false
                    })}>Cancel</Button>
                <Button
                    content="Save Changes"
                    labelPosition='right'
                    icon='checkmark'
                    onClick={() => { this.handleModifyItem() }}
                    positive
                />
            </Modal.Actions>
        </Modal>
    }

    handleCategoryEdit = (e, { name, value }) => {
        this.setState({ itemCategory: value })
    }
    
    handleModifyItem = () => {
        api.put('/items',
            {
                "u_id": parseInt(localStorage.getItem("userID")),
                "item_id": parseInt(this.state.itemID),
                "i_category": this.state.itemCategory,
                "i_name": this.state.itemName,
                "i_price": parseFloat(this.state.itemPrice),
                "i_stock": parseInt(this.state.itemStock)
            }).then(res => {
                console.log("Changed Item");
                console.log(res);
                window.location.reload(false);
            }).catch(error => {
                console.log(error.response.data);
                console.log(error.response.status);
            })
    }


    AddItemModal = () => {
        return <Modal
            open={this.state.addItem}
        >
            <Modal.Header>Create New Product</Modal.Header>
            <Modal.Content>
                <Form>
                    <Form.Input
                        icon='pencil alternate'
                        iconPosition='left'
                        label='Item Name'
                        placeholder='Name'
                        value={this.state.itemName}
                        error={(this.state.error === 5 && this.state.itemName === '')}
                        onChange={input => this.setState({ itemName: input.target.value })}
                    />
                    <Form.Input
                        icon='dollar sign'
                        iconPosition='left'
                        label='Price'
                        placeholder='Price'
                        value={this.state.itemPrice}
                        error={(this.state.error === 5 && this.state.itemPrice === '')}
                        onChange={input => this.setState({ itemPrice: input.target.value })}
                    />
                    <Form.Input
                        icon='boxes'
                        iconPosition='left'
                        label='Stock'
                        placeholder='Stock'
                        value={this.state.itemStock}
                        error={(this.state.error === 5 && this.state.itemStock === '')}
                        onChange={input => this.setState({ itemStock: input.target.value })}
                    />
                    <Header as="h4">Category</Header>
                    <Dropdown
                        icon='th'
                        placeholder='Category'
                        floating
                        labeled
                        button
                        className='icon'
                        options={categories}
                        value={this.state.itemCategory}
                        name='category'
                        onChange={this.handleCategoryEdit} />
                </Form>
                <Message
                    hidden={this.state.error != 1}
                    color={'red'}
                    header='Item name and category pair already exist.'
                />
                <Message
                    hidden={this.state.error != 2}
                    color={'red'}
                    header='Please enter a valid stock ammount.'
                />
                <Message
                    hidden={this.state.error != 3}
                    color={'red'}
                    header='Please enter a valid price.'
                />
                <Message
                    hidden={this.state.error != 4}
                    color={'red'}
                    header='Please fill out the form.'
                />
            </Modal.Content>
            <Modal.Actions>
                <Button color='black' onClick={() =>
                    this.setState({
                        itemID: '',
                        itemName: '',
                        itemCategory: '',
                        itemStock: '',
                        itemPrice: '',
                        addItem: false
                    })}>Cancel</Button>
                <Button
                    content="Create New Product"
                    labelPosition='right'
                    icon='checkmark'
                    onClick={() => { this.handleAddItem() }}
                    positive
                />
            </Modal.Actions>
        </Modal>
    }

    handleAddItem = () => {
        api.post('/items/new',
            {
                "u_id": parseInt(localStorage.getItem("userID")),
                "i_category": this.state.itemCategory,
                "i_name": this.state.itemName,
                "i_price": parseFloat(this.state.itemPrice),
                "i_stock": parseInt(this.state.itemStock)
            }).then(res => {
                console.log("Changed Item");
                console.log(res);
                window.location.reload(false);
            }).catch(error => {
                console.log(error.response.data);
                console.log(error.response.status);
            })
    }

    deleteModal = () => {
        return <Modal
        open={this.state.deleteItem}
    >
        <Modal.Header>DELETE ITEM</Modal.Header>
        <Modal.Content>
            <Modal.Description>
                <Header>Are you sure you want to delete this item?</Header>
            </Modal.Description>
            <Divider hidden/>
        </Modal.Content>
        <Modal.Actions>
            <Button color='black' onClick={() => this.setState({
                deleteItem: false
            })}>
                Cancel
            </Button>
            <Button
                content="Delete this item"
                labelPosition='right'
                icon='trash'
                onClick={() => this.handleDeleteItem()}
                color='red'
            />
        </Modal.Actions>
    </Modal>
    }

    handleDeleteItem = () => {
        api.delete('/items',
            {
                data: {
                    "u_id": parseInt(localStorage.getItem("userID")),
                    "item_id": parseInt(this.state.itemID)
                }
            }).then(res => {
                console.log("Deleted Item");
                console.log(res);
                window.location.reload(false);
            }).catch(error => {
                console.log(error.response.data);
                console.log(error.response.status);
            })
    }
}

export default AdminPage;