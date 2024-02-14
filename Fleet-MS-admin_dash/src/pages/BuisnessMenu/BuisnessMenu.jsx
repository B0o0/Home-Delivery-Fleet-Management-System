import React from 'react'
import { useParams } from 'react-router-dom'
const BuisnessMenu = () => {
  const {menu} = useParams()  
  return (
    <div>{menu} this is buisness menu</div>
  )
}

export default BuisnessMenu