import {createSlice} from '@reduxjs/toolkit'

const pendingDriversSlice = createSlice({
    name : 'pendingDrivers' , 
    initialState : {
        allPendingDrivers : [] , 
        isWaitingForGetPendingDrivers : true , 
        errorInGetPendingDrivers : null , 
        isRequireRender : false ,    
    }
    ,
    reducers : {
        getPendingDriversFromDb(state , action){
            state.allPendingDrivers = action.payload 
            
            state.isWaitingForGetPendingDrivers = false
            state.errorInGetPendingDrivers = null
        } , 
        setWaitingTrue(state){
            state.isWaitingForGetPendingDrivers = true
        } ,
        setWaitingFalse(state){
            state.isWaitingForGetPendingDrivers = false
        } , 
        setErrorInGetPendingDrivers(state , action) {
            state.errorInGetPendingDrivers = action.payload
        } , 
       
        clearPendingDriversError(state){
            state.errorInGetBusiness = null
        } , 
        requireRender(state){
            state.isRequireRender = !state.isRequireRender
        } , 
       
    }
})
export const pendingDriversActions = pendingDriversSlice.actions
export default pendingDriversSlice