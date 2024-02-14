import { createSlice } from "@reduxjs/toolkit";


const  initialState = {
    toast : {
        message : "" , 
        close : 5000 , 
        type : 'success'

    }
}

const toastSlice = createSlice({
    name :'toast' ,
    initialState , 
    reducers : {
        setToast(state , action) {
            state.toast.message = action.payload.message 
            state.toast.type = action.payload.type  
            state.toast.close = action.payload.close
        } ,
    }
})


export const toastActions = toastSlice.actions 
export default toastSlice