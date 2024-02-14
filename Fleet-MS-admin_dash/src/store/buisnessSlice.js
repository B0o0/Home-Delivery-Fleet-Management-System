import {createSlice} from '@reduxjs/toolkit'

const buisnessSlice = createSlice({
    name : 'buisness' , 
    initialState : {
        allBuisness : [] , 
        selectedBuisness : {} ,
        isWaitingForGetBusiness : true , 
        numOfallBuisness : 0 , 
        errorInGetBusiness : null , 
        isRequireRender : false , 
        numOfResOrders : 0 , 
        numOfMarketOreders : 0 ,
    }
    ,
    reducers : {
        getBuisnessFromDb(state , action){
            state.allBuisness = action.payload 
            state.numOfallBuisness = action.payload.length
            state.isWaitingForGetBusiness = false
            state.errorInGetBusiness = null
        } , 
        setNumOfResOrders(state,action){
            state.numOfResOrders = action.payload   
        } ,  
        setNumOfMarketOrders(state,action){
            state.numOfMarketOreders = action.payload
        }  ,    
        setWaitingTrue(state){
            state.isWaitingForGetBusiness = true
        } ,
        setWaitingFalse(state){
            state.isWaitingForGetBusiness = false
        } , 
        setErrorInGetBusiness(state , action) {
            state.errorInGetBusiness = action.payload
        } , 
        setSelectingBuisness(state,action){
            state.selectedBuisness = action.payload
        } ,
        clearBusinessError(state){
            state.errorInGetBusiness = null
        } , 
        requireRender(state){
            state.isRequireRender = !state.isRequireRender
        } , 
       
    }
})
export const businessActions = buisnessSlice.actions
export default buisnessSlice