import React from "react";
import {  useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import {useDispatch} from 'react-redux'
import { businessActions } from "../../store/buisnessSlice";
import { customersActions } from "../../store/customerSlice";
import { approvePendingBuisness } from "../../store/pendingBuisness-actions";
import { approvePendingDiver } from "../../store/pendingDrivers-actions";
const TableRowItem = ({ to, item, columns , isRequireApprove}) => {
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const handleNavigateClick = ()=>{
     if(to === 'pendingB' || to === 'pendingD' ) return 
     if(!to) return 
     switch (to) {
      case 'buisness':
        dispatch(businessActions.setSelectingBuisness(item))
        break;
      case 'customers': 
        dispatch(customersActions.setSelectingCustomer(item))
        break;
      default:
        break;
     }

        if(typeof item["_id"] === "string"){
          navigate(`/${to}/${item["_id"]}`)
        }
        else {
          navigate(`/${to}/${Object.values(item["_id"])[0]}`)
        }
    }

   const handleApprove = ()=>{
    if(to === 'pendingB') {
      dispatch(approvePendingBuisness(Object.values(item["_id"])[0]))
    }else {
      dispatch(approvePendingDiver(Object.values(item["_id"])[0]))
    }
   
   }
  return (
    
    <tr onClick={handleNavigateClick}>
      
        {columns.map((column, columnIndex) =>
          column === "_id" && to !== 'orders' ? null  
          
           : 
           column === '_id' ? <td key={columnIndex}>{Object.values(item[column])[0]}</td>
           :
           (
            <td key={columnIndex}>{item[column]}</td>
          )
        )}
        {isRequireApprove ? <td >
                 <Button variant="primary" className='text-white' onClick={handleApprove}
                 >Approve</Button>
             </td> 
            : null 
            }
    </tr>
    
  );
};

export default TableRowItem;
