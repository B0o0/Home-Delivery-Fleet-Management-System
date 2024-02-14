import React from 'react'
import './styles.css'
import { Spinner } from 'react-bootstrap'
const OverLoader = () => {
  return (
    <div className='loaderContainer'>
         <Spinner animation="grow" variant="primary" />
    </div>
  )
}

export default OverLoader