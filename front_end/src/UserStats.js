import React, {Component, useState, useCallback} from 'react';
import {Container, Card, Image, Header, Statistic} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis, PieChart, Pie, Sector} from "recharts";
import axios from 'axios';
import "./styles.css";

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
    }

    constructor() {
      super();
      if (localStorage.getItem("userID") != null) {
          this.getMostBoughtItems();
          this.getMostBoughtCategories();
          this.getMostExpensiveItem();
          this.getCheapestItem();
          this.state.loggedIn = true;
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
            console.log(error.response.data);
            console.log(error.response.status);
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
      return<Container>
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
        if(this.state.mostExpensive.length > 0) {
          for(let i = 0; i < this.state.mostExpensive.length; i++) {
            return this.state.mostExpensive[i];
          }
        } else {
          return "NO ITEM";
        }
    }

    DisplayMostExpensiveItem = () => {
      return<>
          <Statistic.Group>
            <Statistic>
            <Statistic.Label>Item Name</Statistic.Label>
              <Statistic.Value>{this.checkIfMostExpensiveEmpty()["Item Name"]}</Statistic.Value>
            </Statistic>
            <Statistic>
            <Statistic.Label>Category</Statistic.Label>
                  <Statistic.Value>
                      <Image circular size='medium' src='/man.png' />
                      {this.checkIfMostExpensiveEmpty()["Category"]}
                  </Statistic.Value>
            </Statistic>
            <Statistic>
            <Statistic.Label>Order Ammount</Statistic.Label>
              <Statistic.Value>{this.checkIfMostExpensiveEmpty()["Order Ammount"]}</Statistic.Value>
            </Statistic>
            <Statistic>
            <Statistic.Label>Total</Statistic.Label>
                  <Statistic.Value>{this.checkIfMostExpensiveEmpty()["Total"]}</Statistic.Value>
            </Statistic>
          </Statistic.Group>
      </>
    }

    checkIfCheapestEmpty = () => {
        if(this.state.cheapest.length > 0) {
          for(let i = 0; i < this.state.cheapest.length; i++) {
            return this.state.cheapest[i];
          }
        } else {
          return "NO ITEM";
        }
    }
  
    DisplayCheapestItem = () => {
      return<>
          <Statistic.Group>
            <Statistic>
            <Statistic.Label>Item Name</Statistic.Label>
              <Statistic.Value>{this.checkIfCheapestEmpty()["Item Name"]}</Statistic.Value>
            </Statistic>
            <Statistic>
            <Statistic.Label>Category</Statistic.Label>
            <Statistic.Value>{this.checkIfCheapestEmpty()["Category"]}</Statistic.Value>
            </Statistic>
            <Statistic>
            <Statistic.Label>Order Ammount</Statistic.Label>
              <Statistic.Value>{this.checkIfCheapestEmpty()["Order Ammount"]}</Statistic.Value>
            </Statistic>
            <Statistic>
            <Statistic.Label>Total</Statistic.Label>
                  <Statistic.Value>{this.checkIfCheapestEmpty()["Total"]}</Statistic.Value>
            </Statistic>
          </Statistic.Group>
      </>
    }

    render() {
      return <Container textAlign="center">
                  <Header as='h1'>Most Bought Items</Header>
                  <this.DisplayMostBoughtItems />
                  <Header as='h1'>Most Bought Categories</Header>
                  <this.DisplayMostBoughtCategories />
                  <Header as='h1'>Most Expensive Item</Header>
                  <this.DisplayMostExpensiveItem />
                  <Header as='h1'>Cheapest Item</Header>
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
            <PieChart width={750} height={750}>
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
            
                </div >
          </div >
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
                <PieChart width={750} height={750}>
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
export default UserStats;
