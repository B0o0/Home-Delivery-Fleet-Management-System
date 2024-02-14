import React from "react";
import { Link } from "react-router-dom";
import "./anal.css";
const AnalysticCard = ({ number, text, icon, bgColor, iconColor }) => {
  return (
    <div className="col-xl-3">
      <div
        className="shadow-sm d-flex justify-content-between bg-white p-4 m-2 text-nowrap  rounded-3 cart"
        style={{ borderBottom: `1px solid ${iconColor}` }}
      >
        <div>
          <p className="fs-5 text-muted">{text}(s)</p>
          <div className="d-flex align-items-center">
            <div
              className="card-icon  d-flex align-items-center justify-content-center"
              style={{
                background: bgColor,
              }}
            >
              <i className={`${icon} fs-4`} style={{ color: iconColor }}></i>
            </div>

            <h4 className="ml-2">{number}</h4>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysticCard;
