import React , {useState} from 'react'
import { Pagination } from 'react-bootstrap'
const PaginationTable = ({pagesArrary , currentPage ,setCurrentPage}) => {
  
  const handelNext = ()=>{
    setCurrentPage((state)=>{
      if(state === pagesArrary.length) {
        
        return state
      }
      else return state+1
    })
  }
  const handelBack = ()=>{
    
    setCurrentPage((state)=>{
      if(state === 1) {
        
        return state
      }
      else {
        
        return state-1
      }
    })
  }
  const handleSetPage=(e)=>{
    setCurrentPage(()=>{
        return Number(e.target.innerText)
    })
  }
  return (
    <>
      {pagesArrary.length > 1 ?
      <Pagination className="m-auto" >
          <Pagination.Prev  onClick={handelBack}/>
          {pagesArrary.map((e , index)=>{
            return (
              <Pagination.Item onClick={(event)=>{handleSetPage(event)}} key={index} active={e+1===currentPage}>{e+1}</Pagination.Item>
            )
          })}
          <Pagination.Next  onClick={handelNext} />
      </Pagination> 
      :
      null 
    }
    </>
     
  )
}

export default PaginationTable