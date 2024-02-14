import { createSlice } from "@reduxjs/toolkit";

const authSlice  = createSlice({
    name : 'auth' , 
    initialState : {
        userEmail : localStorage.getItem('userEmail') || '',
        isLoggedIn : !!localStorage.getItem('userEmail') ,
        isWaitingForLogin : false , 
        errorInLogin : ''
    } , 
    reducers : {
        userLogin(state,action){
            state.isLoggedIn = true
            localStorage.setItem('userEmail' ,  action.payload ) , 
            state.isWaitingForLogin = false 
            state.errorInLogin = ''
            state.userEmail = action.payload
        } , 
        userLogout(state){
            state.isLoggedIn = false
            localStorage.removeItem('userEmail')
        } , 
        setWating(state , action){
            state.isWaitingForLogin = action.payload
        } ,
        setErrorInLogin(state,action){
            state.errorInLogin = action.payload
        }
    }
})
export const authActions = authSlice.actions
export default authSlice