import React , { useState } from "react";
import TableRowItem from "../TableRowItem/TableRowItem";
import "./style.css";
import PaginationTable from "../PaginationTable/PaginationTable";

const TableView = ({ to, columns, data , isRequireApprove}) => {
const [currentPage , setCurrentPage] = useState(1)
    //define the number of dishes per page 
const numOfRowPerPage = 5
// calculate the number of  pages (pagination take it in count property to display the number of pages)
const numberOfPages = Math.ceil(data.length / numOfRowPerPage)
// calculate the last index of current page 
const lastRowOfCurrentPage = numOfRowPerPage * currentPage 
// calculate the first index of current page 
const firstRowOfCurrentPage = lastRowOfCurrentPage - numOfRowPerPage 
// calculate the shown exercise according to first and last index and currentPage
const rowsOfCurrentPage = data.slice(firstRowOfCurrentPage , lastRowOfCurrentPage)
  return (
    <div className='d-flex flex-column'>
      <div className="tbl-header table-responsive">
        <table cellPadding="0" cellSpacing="0" border="0">
          <thead>
            <tr>
              {columns.map((column, index) =>
                column === "_id" && to !== 'orders' ? null : <th key={index}>{column}</th>
              )}
              {isRequireApprove ? <th>Action</th> : null}
            </tr>
          </thead>
          <tbody>
            {rowsOfCurrentPage.map((item, index) => (
              <TableRowItem key={index} columns={columns} item={item} to={to} isRequireApprove={isRequireApprove}/>
            ))}
          </tbody>
        </table>
      </div>
      <PaginationTable pagesArrary={[...Array(numberOfPages).keys()]}
       currentPage={currentPage}
       setCurrentPage={setCurrentPage}
       />
      </div>
   
  );
};

export default TableView;
