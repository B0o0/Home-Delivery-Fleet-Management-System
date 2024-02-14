import {createSlice} from '@reduxjs/toolkit'

const ordersSlice = createSlice({
    name : 'order' , 
    initialState : {
        allOrders : [] , 
        isWaitingForGetOrders : true , 
        numOfallOrders : 0 , 
        selectedOrder : {} ,
        errorInGetOrders : null
    }
    ,
    reducers : {
        getOrdersFromDB(state , action){
            state.allOrders = action.payload 
            state.numOfallOrders = action.payload.length
            state.isWaitingForGetOrders = false
            state.errorInGetOrders = null

        } , 
        setWaitingTrue(state){
            state.isWaitingForGetOrders = true
        } ,
        setWaitingFalse(state){
            state.isWaitingForGetOrders = false
        } , 
        setErrorInGetOrders(state , action) {
            state.errorInGetOrders = action.payload
        } , 
       
        clearOrdersError(state){
            state.errorInGetOrders = null
        } ,
        setSelectedOrder(state,action){
            state.selectedOrder = action.payload
        }
    }
})
export const ordersActions = ordersSlice.actions
export default ordersSlice