import React, { Component, useState, useCallback } from 'react';
import { Container, Card, Image, Header, Statistic, Divider } from "semantic-ui-react";
import { Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis, PieChart, Pie, Sector } from "recharts";
import axios from 'axios';
import "./index.css";

const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/global/'
})

class GlobalStats extends Component {
    state = {
        mostBoughtItems: [],
        mostBoughtCategories: [],
        mostExpensive: [],
        cheapest: []
    }

    constructor() {
        super();
        this.getMostBoughtItems();
        this.getMostBoughtCategories();
        this.getMostExpensiveItem();
        this.getCheapestItem();
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
        api.get('/price/max').then(res => {
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
        api.get('/price/min').then(res => {
            console.log("cheapest item");
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
        return <Container>
            <this.CoolItemsPieChart />
        </Container>
    }

    DisplayMostBoughtCategories = () => {
        return <>
            <Container>
                <this.CoolCategoriesPieChart />
            </Container>
        </>
    }

    checkIfMostExpensiveEmpty = () => {
        if (this.state.mostExpensive.length > 0) {
            for (let i = 0; i < this.state.mostExpensive.length; i++) {
                return this.state.mostExpensive[i];
            }
        } else {
            return "NO ITEM";
        }
    }

    DisplayMostExpensiveItem = () => {
        let mostExpensiveItem = this.checkIfMostExpensiveEmpty()

        return <>
            <div class="center">
                <Statistic.Group>
                    <Statistic>
                        <Statistic.Label>Item Name</Statistic.Label>
                        <Statistic.Value>{mostExpensiveItem["Item Name"]}</Statistic.Value>
                    </Statistic>
                    <Statistic>
                        <Statistic.Label>Category</Statistic.Label>
                        <Statistic.Value>{mostExpensiveItem["Category"]}</Statistic.Value>
                    </Statistic>
                    <Statistic>
                        <Statistic.Label>Price</Statistic.Label>
                        <Statistic.Value>{mostExpensiveItem["Price"]}</Statistic.Value>
                    </Statistic>
                </Statistic.Group>
            </div>
        </>
    }

    checkIfCheapestEmpty = () => {
        if (this.state.cheapest.length > 0) {
            for (let i = 0; i < this.state.cheapest.length; i++) {
                return this.state.cheapest[i];
            }
        } else {
            return "NO ITEM";
        }
    }

    DisplayCheapestItem = () => {
        let cheapestItem = this.checkIfCheapestEmpty()

        return <>
            <div class="center">
                <Statistic.Group>
                    <Statistic>
                        <Statistic.Label>Item Name</Statistic.Label>
                        <Statistic.Value>{cheapestItem["Item Name"]}</Statistic.Value>
                    </Statistic>
                    <Statistic>
                        <Statistic.Label>Category</Statistic.Label>
                        <Statistic.Value>{cheapestItem["Category"]}</Statistic.Value>
                    </Statistic>
                    <Statistic>
                        <Statistic.Label>Price</Statistic.Label>
                        <Statistic.Value>{cheapestItem["Price"]}</Statistic.Value>
                    </Statistic>
                </Statistic.Group>
            </div>
        </>
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
        </Container>
    }

    renderActiveShape = (props: any) => {
        const RADIAN = Math.PI / 180;
        const {
            cx,
            cy,
            midAngle,
            innerRadius,
            outerRadius,
            startAngle,
            endAngle,
            fill,
            payload,
            percent,
            value
        } = props;
        const sin = Math.sin(-RADIAN * midAngle);
        const cos = Math.cos(-RADIAN * midAngle);
        const sx = cx + (outerRadius + 10) * cos;
        const sy = cy + (outerRadius + 10) * sin;
        const mx = cx + (outerRadius + 30) * cos;
        const my = cy + (outerRadius + 30) * sin;
        const ex = mx + (cos >= 0 ? 1 : -1) * 22;
        const ey = my;
        const textAnchor = cos >= 0 ? "start" : "end";

        return (
            <g>
                <text x={cx} y={cy} dy={8} fontSize='30px' fontWeight='bold' textAnchor="middle" fill="#000">
                    {payload.Name ? payload.Name : payload.Category}
                </text>
                <Sector
                    cx={cx}
                    cy={cy}
                    innerRadius={innerRadius}
                    outerRadius={outerRadius}
                    startAngle={startAngle}
                    endAngle={endAngle}
                    fill={fill}
                />
                <Sector
                    cx={cx}
                    cy={cy}
                    startAngle={startAngle}
                    endAngle={endAngle}
                    innerRadius={outerRadius + 6}
                    outerRadius={outerRadius + 10}
                    fill={fill}
                />
                <path
                    d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
                    stroke={fill}
                    fill="none"
                />
                <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
                <text
                    x={ex + (cos >= 0 ? 1 : -1) * 12}
                    y={ey}
                    textAnchor={textAnchor}
                    fill="#333"
                    fontSize='50px'
                >{`${value}`}</text>
                <text
                    x={ex + (cos >= 0 ? 1 : -1) * 12}
                    y={ey}
                    dy={18}
                    textAnchor={textAnchor}
                    fill="#999"
                >
                    {`(${(percent * 100).toFixed(2)}%)`}
                </text>
            </g>
        );
    };

    CoolItemsPieChart = () => {
        const [activeIndex, setActiveIndex] = useState(0);
        const onPieEnter = useCallback(
            (_, index) => {
                setActiveIndex(index);
            },
            [setActiveIndex]
        );

        return (
            <div class="ui one column stackable center aligned page grid">
                <div class="column wide">
                    <PieChart width={825} height={750}>
                        <Pie
                            activeIndex={activeIndex}
                            activeShape={this.renderActiveShape}
                            data={this.state.mostBoughtItems}
                            cx="50%"
                            cy="50%"
                            innerRadius={192}
                            outerRadius={296}
                            fill="#0084d8"
                            dataKey="Purchase Count"
                            onMouseEnter={onPieEnter}
                        />
                    </PieChart>
                </div>
            </div>
        );
    }

    CoolCategoriesPieChart = () => {
        const [activeIndex, setActiveIndex] = useState(0);
        const onPieEnter = useCallback(
            (_, index) => {
                setActiveIndex(index);
            },
            [setActiveIndex]
        );

        return (
            <div class="ui one column stackable center aligned page grid">
                <div class="column wide">
                    <PieChart width={850} height={750}>
                        <Pie
                            activeIndex={activeIndex}
                            activeShape={this.renderActiveShape}
                            data={this.state.mostBoughtCategories}
                            cx="50%"
                            cy="50%"
                            innerRadius={192}
                            outerRadius={296}
                            fill="#067"
                            dataKey="Purchase Count"
                            onMouseEnter={onPieEnter}
                        />
                    </PieChart>
                </div>
            </div>
        );
    }

}
export default GlobalStats;