import "../LeftNav/leftNav.css";
import { Link } from "react-router-dom";
import SingleActionItem from "../SingleActionItem/SingleActionItem";

const DropDownMenu = ({
  isNavColsed,
  item,
  setWichListActive,
  isActiveOne,
}) => {
  return (
    <>
      <li className="list-item" onClick={setWichListActive}>
        <i className={`${item.icon} fa-fw icon-color`}></i>
        <Link
          className={!isNavColsed ? 'w-100 d-flex align-items-center justify-content-between' : ""} 
          to={item.link ? item.link : "#"}
          data-bs-target="#icons-nav"
          aria-expanded="true"
        >
          <span  style={{ color: "gray" , fontSize : '14px'  }}>{item.listAction}</span>
          {item.lists ? (
            <i className="fa-solid fa-caret-down text-secondary me-2"></i>
          ) : null}
        </Link>
      </li>
      {item.lists ? (
        <ul
          id="icons-nav"
          className={`nav-content collapse  ${
            isActiveOne && !isNavColsed ? "show" : ""
          }`}
          data-bs-parent="#sidebar-nav"
        >
          {item.lists.map((e, index) => {
            return <SingleActionItem key={index} item={e} />;
          })}
        </ul>
      ) : null}
    </>
  );
};

export default DropDownMenu;
