import {createSlice} from '@reduxjs/toolkit'

const driverSlice = createSlice({
    name : 'driver' , 
    initialState : {
        allDrivers : [] , 
        allAvailableDrivers : [] ,
        driversForPreview : [] ,
        allUnAvailableDrivers : [] , 
        allBusyDrivers : [] ,
        selectedDriver : {} ,
        isWaitingForGetDrivers : true , 
        numOfallDrivers : 0 , 
        errorInGetDrivers : null , 
        isRequireRender : false
    }
    ,
    reducers : {
        getDriversFromDb(state , action){
            state.allDrivers = action.payload 
            state.driversForPreview=action.payload
            state.numOfallDrivers = action.payload.length
            state.isWaitingForGetDrivers = false
            state.errorInGetDrivers = null

        } , 
        getAvaliableDriversFromDb(state , action){
            state.allAvailableDrivers = action.payload 
            state.isWaitingForGetDrivers = false
            state.errorInGetDrivers = null

        } , 
        getUnAvaliableDriversFromDb(state , action){
            state.allUnAvailableDrivers = action.payload 
            state.isWaitingForGetDrivers = false
            state.errorInGetDrivers = null

        } , 
        getBusyDriversFromDb(state , action){
            state.allBusyDrivers = action.payload 
            state.isWaitingForGetDrivers = false
            state.errorInGetDrivers = null

        } , 
        setWaitingTrue(state){
            state.isWaitingForGetDrivers = true
        } ,
        setWaitingFalse(state){
            state.isWaitingForGetDrivers = false
        } , 
        setErrorInGetDrivers(state , action) {
            state.errorInGetDrivers = action.payload
        } , 
        setSelectingDriver(state,action){
            state.selectedDriver = action.payload
        } ,
        clearDriverError(state){
            state.errorInGetDrivers = null
        } , 
        setWhichDriversForPreview(state,action){
            switch(action.payload){
                case 'all' : 
                  state.driversForPreview = state.allDrivers
                 break 
                case 'availiable' :  
                 state.driversForPreview = state.allAvailableDrivers
                 break  
                 case 'unAvailiable' :  
                 state.driversForPreview = state.allUnAvailableDrivers
                 break   
                 case 'busy' :  
                 state.driversForPreview = state.allBusyDrivers
                 break   
                 default : 
                 state.driversForPreview = state.allDrivers
            }
        } ,
        requireRender(state){
            state.isRequireRender = !state.isRequireRender
        }
    }
})
export const driversActions = driverSlice.actions
export default driverSlice