import {createSlice} from '@reduxjs/toolkit'

const customerSlice = createSlice({
    name : 'customer' , 
    initialState : {
        allCustomers : [] , 
        selectedCustomers : {} ,
        isWaitingForGetCustomers : true , 
        numOfallCustomers: 0 , 
        errorInGetCustomers : null,
        isRequireRender : false
    }
    ,
    reducers : {
        getCustomersFromDb(state , action){
            state.allCustomers = action.payload 
            state.numOfallCustomers = action.payload.length
            state.isWaitingForGetCustomers = false
            state.errorInGetCustomers = null
        } , 
        setWaitingTrue(state){
            state.isWaitingForGetCustomers = true
        } ,
        setWaitingFalse(state){
            state.isWaitingForGetCustomers = false
        } , 
        setErrorInGetCustomers(state , action) {
            state.errorInGetCustomers = action.payload
        } , 
        setSelectingCustomer(state,action){
            state.selectedCustomers = action.payload
        } ,
        clearCustomerError(state){
            state.errorInGetCustomers = null
        } , 
        requireRender(state){
            state.isRequireRender = !state.isRequireRender
        }
    }
})
export const customersActions = customerSlice.actions
export default customerSlice