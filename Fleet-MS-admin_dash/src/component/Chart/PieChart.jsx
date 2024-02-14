import React from "react";
import "./pie.css";
import { useSelector } from "react-redux";
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
const PieChartt = () => {
  const available = useSelector((state)=>state.driver.allAvailableDrivers).length || 0
  const busy = useSelector((state)=>state.driver.allBusyDrivers).length || 0
  const unAvailable = useSelector((state)=>state.driver.allUnAvailableDrivers).length || 0
  //   data to first dash
  const data01 = [
    { name: "Available Drivers", value: available },
    { name: "Busy Drivers", value: busy },
    { name: "Not available Drivers", value: unAvailable },
  ];

  //  data to second dash

  const COLORS = ["#66da5e", "#FFA500", "#ff0e0e"];

  return (
    // <di className="col-md-5   ">
    <Col md={5} sm={3} className="bg-white rounded m-2 shadow-sm">
      <h3 className="text-center my-3">Drivers Chart</h3>
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
            <PieChart>
              <Pie
                dataKey="value"
                isAnimationActive={true}
                data={data01}
                fill="#8884d8"
                label
              >
                {data01.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </Col>
  );
};

export default PieChartt;
