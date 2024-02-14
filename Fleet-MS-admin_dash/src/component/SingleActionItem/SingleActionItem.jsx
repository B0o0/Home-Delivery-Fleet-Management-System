import React from 'react'
import {Link} from 'react-router-dom'
import './singleActionStyle.css'
const SingleActionItem = ({item}) => {
  return (
      <li className='li-item'>
         <Link to={item.link} >
            {item.txt}
         </Link>
       </li>
  )
}

export default SingleActionItem