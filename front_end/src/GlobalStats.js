import React, { Component, useState, useCallback } from 'react';
import { Container, Header, Statistic, Divider } from "semantic-ui-react";
import { ResponsiveContainer, RadialBarChart, RadialBar, Legend, Tooltip, Pie, PieChart } from "recharts";
import axios from 'axios';
import "./index.css";

const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/global/'
})

const itemsArray = []

class GlobalStats extends Component {
    state = {
        mostBoughtItems: [],
        mostBoughtCategories: [],
        mostExpensive: [],
        mostLiked: [],
        cheapest: []
    }

    itemState = {
        name: '',
        purchases: '',
        fill: ''
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
            <this.ItemsPieChart />
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

    ItemsPieChart = () => {
        return (
            <RadialBarChart
                width={512}
                height={512}
                innerRadius={100}
                outerRadius={256}
                data={this.state.mostBoughtItems.reverse()}
                startAngle={180}
                endAngle={0}

            >
                <RadialBar minAngle={180} background clockWise dataKey='Purchase Count' />
                {/* <Legend iconSize={10} width={120} height={140} /> */}
                <Tooltip />
            </RadialBarChart>
        );
    }

    // renderActiveShape = (props: any) => {
    //     const RADIAN = Math.PI / 180;
    //     const {
    //         cx,
    //         cy,
    //         midAngle,
    //         innerRadius,
    //         outerRadius,
    //         startAngle,
    //         endAngle,
    //         fill,
    //         payload,
    //         percent,
    //         value
    //     } = props;
    //     const sin = Math.sin(-RADIAN * midAngle);
    //     const cos = Math.cos(-RADIAN * midAngle);
    //     const sx = cx + (outerRadius + 10) * cos;
    //     const sy = cy + (outerRadius + 10) * sin;
    //     const mx = cx + (outerRadius + 30) * cos;
    //     const my = cy + (outerRadius + 30) * sin;
    //     const ex = mx + (cos >= 0 ? 1 : -1) * 22;
    //     const ey = my;
    //     const textAnchor = cos >= 0 ? "start" : "end";

    //     return (
    //         <g>
    //             <text x={cx} y={cy} dy={8} fontSize='30px' fontWeight='bold' textAnchor="middle" fill="#000">
    //                 {payload.Name ? payload.Name : payload.Category}
    //             </text>
    //             <Sector
    //                 cx={cx}
    //                 cy={cy}
    //                 innerRadius={innerRadius}
    //                 outerRadius={outerRadius}
    //                 startAngle={startAngle}
    //                 endAngle={endAngle}
    //                 fill={fill}
    //             />
    //             <Sector
    //                 cx={cx}
    //                 cy={cy}
    //                 startAngle={startAngle}
    //                 endAngle={endAngle}
    //                 innerRadius={outerRadius + 6}
    //                 outerRadius={outerRadius + 10}
    //                 fill={fill}
    //             />
    //             <path
    //                 d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
    //                 stroke={fill}
    //                 fill="none"
    //             />
    //             <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
    //             <text
    //                 x={ex + (cos >= 0 ? 1 : -1) * 12}
    //                 y={ey}
    //                 textAnchor={textAnchor}
    //                 fill="#333"
    //                 fontSize='50px'
    //             >{`${value}`}</text>
    //             <text
    //                 x={ex + (cos >= 0 ? 1 : -1) * 12}
    //                 y={ey}
    //                 dy={18}
    //                 textAnchor={textAnchor}
    //                 fill="#999"
    //             >
    //                 {`(${(percent * 100).toFixed(2)}%)`}
    //             </text>
    //         </g>
    //     );
    // };

    // CoolItemsPieChart = () => {
    //     const [activeIndex, setActiveIndex] = useState(0);
    //     const onPieEnter = useCallback(
    //         (_, index) => {
    //             setActiveIndex(index);
    //         },
    //         [setActiveIndex]
    //     );

    //     return (
    //         <div class="ui one column stackable center aligned page grid">
    //             <div class="column wide">
    //                 <PieChart width={825} height={750}>
    //                     <Pie
    //                         activeIndex={activeIndex}
    //                         activeShape={this.renderActiveShape}
    //                         data={this.state.mostBoughtItems}
    //                         cx="50%"
    //                         cy="50%"
    //                         innerRadius={192}
    //                         outerRadius={296}
    //                         fill="#0084d8"
    //                         dataKey="Purchase Count"
    //                         onMouseEnter={onPieEnter}
    //                     />
    //                 </PieChart>
    //             </div>
    //         </div>
    //     );
    // }

    // CoolCategoriesPieChart = () => {
    //     const [activeIndex, setActiveIndex] = useState(0);
    //     const onPieEnter = useCallback(
    //         (_, index) => {
    //             setActiveIndex(index);
    //         },
    //         [setActiveIndex]
    //     );

    //     return (
    //         <div class="ui one column stackable center aligned page grid">
    //             <div class="column wide">
    //                 <PieChart width={850} height={750}>
    //                     <Pie
    //                         activeIndex={activeIndex}
    //                         activeShape={this.renderActiveShape}
    //                         data={this.state.mostBoughtCategories}
    //                         cx="50%"
    //                         cy="50%"
    //                         innerRadius={192}
    //                         outerRadius={296}
    //                         fill="#067"
    //                         dataKey="Purchase Count"
    //                         onMouseEnter={onPieEnter}
    //                     />
    //                 </PieChart>
    //             </div>
    //         </div>
    //     );
    // }

    CoolCategoriesPieChart = () => {
        return (
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
                />
                <Legend />
                <Tooltip />
            </PieChart>
        );
    }

}
export default GlobalStats;