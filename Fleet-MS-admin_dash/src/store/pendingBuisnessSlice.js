import {createSlice} from '@reduxjs/toolkit'

const pendingBuisnessSlice = createSlice({
    name : 'pendingBuisness' , 
    initialState : {
        allPendingBuisness : [] , 
        isWaitingForGetPendingBusiness : true , 
        errorInGetPendingBusiness : null , 
        isRequireRender : false ,    
    }
    ,
    reducers : {
        getBuisnessFromDb(state , action){
            state.allPendingBuisness = action.payload 
            
            state.isWaitingForGetPendingBusiness = false
            state.errorInGetPendingBusiness = null
        } , 
        setWaitingTrue(state){
            state.isWaitingForGetPendingBusiness = true
        } ,
        setWaitingFalse(state){
            state.isWaitingForGetPendingBusiness = false
        } , 
        setErrorInGetBusiness(state , action) {
            state.errorInGetBusiness = action.payload
        } , 
       
        clearBusinessError(state){
            state.errorInGetBusiness = null
        } , 
        requireRender(state){
            state.isRequireRender = !state.isRequireRender
        } , 
       
    }
})
export const pendingBuisnessActions = pendingBuisnessSlice.actions
export default pendingBuisnessSlice