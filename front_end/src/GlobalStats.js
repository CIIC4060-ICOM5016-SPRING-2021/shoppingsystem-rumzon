import React, { Component } from 'react';
import { Container, Header, Statistic, Divider } from "semantic-ui-react";
import { ResponsiveContainer, Legend, Tooltip, Pie, PieChart, Cell } from "recharts";
import axios from 'axios';
import "./index.css";

const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/global/'
})

const COLORS = ['#db2828', '#e03997', '#a333c8', '#6435c9', '#2185d0', '#00b5ad', '#21ba45', '#b5cc18', '#fbbd08', '#f2711c', '#a5673f', '#a53f3f'];

//const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#B413EC', '#FF1493', '#32CD32', '#B03060', '#EE82EE', '#A0A0A0', '#000000'];
class GlobalStats extends Component {
    state = {
        mostBoughtItems: [],
        mostBoughtCategories: [],
        mostExpensive: [],
        mostLiked: [],
        cheapest: []
    }

    constructor() {
        super();
        this.getMostBoughtItems();
        this.getMostBoughtCategories();
        this.getMostExpensiveItem();
        this.getCheapestItem();
        this.getMostLikedItem();
    }

    getMostBoughtItems = () => {
        api.post('/hot/items', {
            "onlyActive": true
        }).then(res => {
            console.log(res.data);
            this.setState({
                mostBoughtItems: res.data
            });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    getMostBoughtCategories = () => {
        api.post('/hot/category', {
            "onlyActive": true
        }).then(res => {
            this.setState({
                mostBoughtCategories: res.data
            });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    getMostExpensiveItem = () => {
        api.get('/price/max').then(res => {
            this.setState({
                mostExpensive: res.data
            });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    getCheapestItem = () => {
        api.get('/price/min').then(res => {
            this.setState({
                cheapest: res.data
            });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    getMostLikedItem = () => {
        api.get('/likes').then(res => {
            console.log("most liked item");
            console.log(res.data);
            this.setState({
                mostLiked: res.data
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
                            <Statistic.Value>{item["Category"]}</Statistic.Value>
                        </Statistic>
                        <Statistic>
                            <Statistic.Label>Price</Statistic.Label>
                            <Statistic.Value>{item["Price"]}</Statistic.Value>
                        </Statistic>
                    </Statistic.Group>
                </div>
                <Divider hidden />
            </>
        });
    }

    DisplayMostLikedItem = () => {
        return this.state.mostLiked.map(item => {
            return <>
                <div class="center">
                    <Statistic.Group size="tiny">
                        <Statistic>
                            <Statistic.Label>Item Name</Statistic.Label>
                            <Statistic.Value>{item["Name"]}</Statistic.Value>
                        </Statistic>
                        <Statistic>
                            <Statistic.Label>Category</Statistic.Label>
                            <Statistic.Value>{item["Category"]}</Statistic.Value>
                        </Statistic>
                        <Statistic>
                            <Statistic.Label>Wishlist Count</Statistic.Label>
                            <Statistic.Value>{item["Like Count"]}</Statistic.Value>
                        </Statistic>
                    </Statistic.Group>
                </div>
                <Divider hidden />
            </>
        })
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
                            <Statistic.Label>Price</Statistic.Label>
                            <Statistic.Value>{item["Price"]}</Statistic.Value>
                        </Statistic>
                    </Statistic.Group>
                </div>
                <Divider hidden />
            </>
        })
    }

    render() {
        return <Container textAlign="center">
            <Header as='h1'>Rumzon Most Bought Items</Header>
            <div class="center">
                <this.DisplayMostBoughtItems />
            </div>
            <Header as='h1'>Rumzon Most Bought Categories</Header>
            <div class="center">
                <this.DisplayMostBoughtCategories />
            </div>
            <Divider />
            <Header as='h1'>Rumzon Most Expensive Item</Header>
            <this.DisplayMostExpensiveItem />
            <Divider />
            <Header as='h1'>Rumzon Least Expensive Item</Header>
            <this.DisplayCheapestItem />
            <Divider />
            <Header as='h1'>Rumzon Most Liked Item</Header>
            <this.DisplayMostLikedItem />
        </Container>
    }

    CoolItemsPieChart = () => {
        return (
            <div class="center">
                <PieChart width={900} height={450}>
                    <Pie
                        data={this.state.mostBoughtItems}
                        cx="50%"
                        cy="50%"
                        innerRadius={75}
                        outerRadius={150}
                        fill="#067"
                        dataKey="Purchase Count"
                        nameKey="Name"
                        label
                        paddingAngle={3}
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
                <PieChart width={950} height={450}>
                    <Pie
                        data={this.state.mostBoughtCategories}
                        cx="50%"
                        cy="50%"
                        innerRadius={75}
                        outerRadius={150}
                        fill="#067"
                        dataKey="Purchase Count"
                        nameKey="Category"
                        label
                        paddingAngle={2}
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
export default GlobalStats;