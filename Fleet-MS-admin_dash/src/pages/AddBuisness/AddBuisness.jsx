import React from 'react'
import MainPageText from '../../component/MainPageText/MainPageText'
import AddBuisnessForm from '../../component/AddBuisnessForm/AddBuisnessForm'
const AddBuisness = () => {
  return (
    <div className='container-fluid'>
        <MainPageText text='Add Buisness'/>
        <AddBuisnessForm />
    </div>
  )
}

export default AddBuisness