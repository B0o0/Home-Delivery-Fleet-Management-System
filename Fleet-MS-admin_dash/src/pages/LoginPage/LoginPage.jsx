import React from 'react'
import './loginStyle.css'
import Banner from '../../component/Banner/Banner'
import Login from '../../component/Login/Login'
import { useSelector } from 'react-redux'
import { Navigate } from 'react-router-dom'
const LoginPage = () => {
  const isUserLoggedIn = useSelector((state)=> state.auth.isLoggedIn)  
  if(isUserLoggedIn)  return <Navigate to='/' replace/>
  return (
    <div className='authBackground'>
       <Banner />
       <Login />
    </div>
  )
}

export default LoginPage