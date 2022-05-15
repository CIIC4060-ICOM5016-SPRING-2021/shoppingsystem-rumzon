import React, { Component } from 'react';
import { Container, Message, Header, Statistic, Divider } from "semantic-ui-react";
import { ResponsiveContainer, Legend, Tooltip, Pie, PieChart, Cell } from "recharts";
import axios from 'axios';
import "./styles.css";

const COLORS = ['#db2828', '#e03997', '#a333c8', '#6435c9', '#2185d0', '#00b5ad', '#21ba45', '#b5cc18', '#fbbd08', '#f2711c', '#a5673f'];

const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/users/'
})

class UserStats extends Component {
    state = {
        mostBoughtItems: [],
        mostBoughtCategories: [],
        mostExpensive: [],
        cheapest: [],
        loggedIn: false,
        noPurchases: false
    }

    constructor() {
        super();
        if (localStorage.getItem("userID") != null) {
            this.state.loggedIn = true;
            this.getMostBoughtItems();
            if (!this.state.noPurchases) {
                this.getMostBoughtCategories();
                this.getMostExpensiveItem();
                this.getCheapestItem();
            }
        }
    }

    getMostBoughtItems = () => {
        api.post('/hot/items', {
            "u_id": parseInt(localStorage.getItem("userID")),
            "onlyActive": true
        }).then(res => {
            console.log(res.data);
            this.setState({
                mostBoughtItems: res.data
            });
        }).catch(error => {
            if (error.response.status === 404) {
                this.setState({ noPurchases: true })
            }
        })
    }

    getMostBoughtCategories = () => {
        api.post('/hot/category', {
            "u_id": parseInt(localStorage.getItem("userID")),
            "onlyActive": true
        }).then(res => {
            console.log(res.data);
            this.setState({
                mostBoughtCategories: res.data
            });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    getMostExpensiveItem = () => {
        api.post('/itemsinorder/max', {
            "u_id": parseInt(localStorage.getItem("userID")),
            "onlyActive": true
        }).then(res => {
            console.log(res.data);
            this.setState({
                mostExpensive: res.data
            });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    getCheapestItem = () => {
        api.post('/itemsinorder/min', {
            "u_id": parseInt(localStorage.getItem("userID")),
            "onlyActive": true
        }).then(res => {
            console.log(res.data);
            this.setState({
                cheapest: res.data
            });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    DisplayMostBoughtItems = () => {
        return <ResponsiveContainer>
            <this.CoolItemsPieChart />
        </ResponsiveContainer>
    }

    DisplayMostBoughtCategories = () => {
        return <ResponsiveContainer>
                <this.CoolCategoriesPieChart />
            </ResponsiveContainer>
    }

    DisplayMostExpensiveItem = () => {
        return this.state.mostExpensive.map(item => {
            return <>
                <div class="center">
                    <Statistic.Group size="tiny">
                        <Statistic>
                            <Statistic.Label>Item Name</Statistic.Label>
                            <Statistic.Value>{item["Item Name"]}</Statistic.Value>
                        </Statistic>
                        <Statistic>
                            <Statistic.Label>Category</Statistic.Label>
                            <Statistic.Value>
                                {item["Category"]}
                            </Statistic.Value>
                        </Statistic>
                        <Statistic>
                            <Statistic.Label>Order Ammount</Statistic.Label>
                            <Statistic.Value>{item["Order Ammount"]}</Statistic.Value>
                        </Statistic>
                        <Statistic>
                            <Statistic.Label>Total</Statistic.Label>
                            <Statistic.Value>{item["Total"]}</Statistic.Value>
                        </Statistic>
                    </Statistic.Group>
                </div> 
                <Divider hidden/>
            </>
        });
    }

    DisplayCheapestItem = () => {
        return this.state.cheapest.map(item => {
            return <>
                <div class="center">
                    <Statistic.Group size="tiny">
                        <Statistic>
                            <Statistic.Label>Item Name</Statistic.Label>
                            <Statistic.Value>{item["Item Name"]}</Statistic.Value>
                        </Statistic>
                        <Statistic>
                            <Statistic.Label>Category</Statistic.Label>
                            <Statistic.Value>{item["Category"]}</Statistic.Value>
                        </Statistic>
                        <Statistic>
                            <Statistic.Label>Order Ammount</Statistic.Label>
                            <Statistic.Value>{item["Order Ammount"]}</Statistic.Value>
                        </Statistic>
                        <Statistic>
                            <Statistic.Label>Total</Statistic.Label>
                            <Statistic.Value>{item["Total"]}</Statistic.Value>
                        </Statistic>
                    </Statistic.Group>
                </div>
                <Divider hidden />
            </>
        });
    }

    render() {
        if (this.state.loggedIn) {
            if (this.state.noPurchases) {
                return <>
                    <Message
                        header='You have no purchases!'
                    />
                </>
            } else {
                return <Container textAlign="center">
                    <Header as='h1'>Your Most Bought Items</Header>
                    <this.DisplayMostBoughtItems />
                    <Divider />
                    <Header as='h1'>Your Most Bought Categories</Header>
                    <this.DisplayMostBoughtCategories />
                    <Divider />
                    <Header as='h1'>Your Most Expensive Purchase</Header>
                    <this.DisplayMostExpensiveItem />
                    <Divider />
                    <Header as='h1'>Your Least Expensive Purchase</Header>
                    <this.DisplayCheapestItem />
                </Container>
            }
        } else {
                return <>
                    <Message
                        header='You are not logged in!'
                        content='Please log in to view your stats.'
                    />
                </>
        }
    }

    CoolItemsPieChart = () => {
        return (
        <div class="center">
            <PieChart width={850} height={750}>
                <Pie
                    data={this.state.mostBoughtItems}
                    cx="50%"
                    cy="50%"
                    innerRadius={192}
                    outerRadius={296}
                    fill="#067"
                    dataKey="Purchase Count"
                    nameKey="Name"
                    label
                    paddingAngle = {1}
                >
                    {this.state.mostBoughtItems.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Legend />
                <Tooltip />
            </PieChart>
        </div>
        );
    }

    CoolCategoriesPieChart = () => {
        return (
        <div class="center">
            <PieChart width={850} height={750}>
                <Pie
                    data={this.state.mostBoughtCategories}
                    cx="50%"
                    cy="50%"
                    innerRadius={192}
                    outerRadius={296}
                    fill="#067"
                    dataKey="Purchase Count"
                    nameKey="Category"
                    label
                    paddingAngle = {1}
                >
                    {this.state.mostBoughtCategories.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Legend />
                <Tooltip />
            </PieChart>
        </div>
        );
    }
}
export default UserStats;
