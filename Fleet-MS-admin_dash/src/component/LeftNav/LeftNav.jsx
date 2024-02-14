import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./leftNav.css";
import DropDownMenu from "../DropDownMenu/DropDownMenu";
import leftNavActions from "../../data/leftNavActions";


const LeftNav = ({ isNotActive , setNotActive }) => {
  const [isDropdownActive, setDropdownActive] = useState(false);

  const setWichListActive = (index) => {
    if (isDropdownActive === index) {
      setDropdownActive(false);
    } else {
      setDropdownActive(() => index);
    }
  };
  return (
    <div>
      <div className="wrapper">
        <nav id="sidebar" className={isNotActive ? "active" : ""}>
          <ul className="list-unstyled components">
            <li className="main-list w-100 rounded mt-4">
              <i
                className="fas fa-tachometer-alt fa-fw text-white"
                style={{ fontSize: "2rem" }}
              ></i>
              <Link to="/" className="text-white " aria-current="true">
                <span className='bg-white rounded text-primary p-1 flex-nowrap ' style={{fontSize : '18px'}}>FASTX BOARD</span> 
              </Link>
            </li>

            {leftNavActions.map((e, index) => {
              return (
                <DropDownMenu
                  isNavColsed={isNotActive}
                  key={index}
                  item={e}
                  isActiveOne={index === isDropdownActive}
                  setWichListActive={() => setWichListActive(index)}
                />
              );
            })}
          </ul>
        </nav>
      </div>
     
    </div>
  );
};
export default LeftNav;
