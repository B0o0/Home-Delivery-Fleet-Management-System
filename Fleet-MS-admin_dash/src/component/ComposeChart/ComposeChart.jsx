import React from "react";

import { ResponsiveContainer } from "recharts";
import {
  PieChart,
  Pie,
  Tooltip,
  Cell,
  ComposedChart,
  Line,
  Area,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
  Scatter,
} from "recharts";

import {} from "recharts";
import { Col } from "react-bootstrap";
import { useSelector } from "react-redux";
const ComposeChart = () => {
 
   const allBuisness = useSelector((state)=>state.buisness.allBuisness)
   const numOfRes  =   allBuisness &&  allBuisness.filter((item)=> item.type ==='Restaurant').length
   const numOfMarket  =  allBuisness && allBuisness.filter((item)=> item.type ==='Market').length
   const numOfResOrders = useSelector((state)=>state.buisness.numOfResOrders)
   const numOfMarketOreders = useSelector((state)=>state.buisness.numOfMarketOreders)

    const data = [
        {
          name: "Resturant",
          number: numOfRes,
          totalOrders: numOfResOrders,
         
        },
        {
          name: "Super Market",
          number: numOfMarket,
          totalOrders: numOfMarketOreders,
         
        },
       
      ];

  return (
    // <di className="col-md-5   ">
    <Col md={5} sm={3} className="bg-white rounded m-2 shadow-sm">
      <h3 className="text-center my-3">Buisness Chart</h3>
      <div
        style={{ position: "relative", width: "100%", padding: "250px 0px" }}
      >
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 0,
            top: 0,
          }}
        >
          <ResponsiveContainer>
          <ComposedChart
          className="chart"
            width={500}
            height={400}
            data={data}
            margin={{
              top: 20,
              right: 20,
              bottom: 20,
              left: 20,
            }}
          >
            <CartesianGrid data={data} stroke="#f5f5f5" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Area
              type="monotone"
              dataKey="totalOrders"
              fill="#8884d8"
              stroke="#8884d8"
            />
            <Bar dataKey="number" barSize={20} fill="#413ea0" />
            <Line type="monotone" dataKey="totalOrders" stroke="#ff7300" />
            <Scatter dataKey="number" fill="red" />
          </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>
    </Col>
  );
};

export default ComposeChart;
