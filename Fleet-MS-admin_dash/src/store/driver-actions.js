import { driversActions } from "./driveSlice";
import {toastActions} from './toastSlice'
export const getAllDrivers = () => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch("http://127.0.0.1:8000/admin/getAllDrivers");
      const response = await data.json();
      const formattedResponse = response.map(({password ,user_id
        , user_type ,approved	, approved_at  , ...e})=>{
          return e
      })
  
      return formattedResponse;
    };
    try {
      dispatch(driversActions.setWaitingTrue());
      const data = await getAll();
      dispatch(driversActions.setWaitingFalse());
      dispatch(driversActions.getDriversFromDb(data));
      dispatch(driversActions.clearDriverError());
    } catch (err) {
      
      dispatch(driversActions.setErrorInGetDrivers(err));
      dispatch(driversActions.setWaitingFalse());
    }
  };
};
export const getAllAvailableDrivers = () => {
    return async (dispatch) => {
      const getAll = async () => {
        const data = await fetch("http://127.0.0.1:8000/admin/getAll_available_Drivers");
        const response = await data.json();
        const formattedResponse = response.map(({password ,user_id
          , user_type ,approved	, approved_at , status , ...e})=>{
            return e
        })
       
        return formattedResponse;
      };
      try {
        dispatch(driversActions.setWaitingTrue());
        const data = await getAll();
        dispatch(driversActions.setWaitingFalse());
        dispatch(driversActions.getAvaliableDriversFromDb(data));
        dispatch(driversActions.clearDriverError());
      } catch (err) {
        console.log(err);
        dispatch(driversActions.setErrorInGetDrivers(err));
        dispatch(driversActions.setWaitingFalse());
      }
    };
  };

  export const getAllUnAvailableDrivers = () => {
    return async (dispatch) => {
      const getAll = async () => {
        const data = await fetch("http://127.0.0.1:8000/admin/getAll_Notavailable_Drivers");
        const response = await data.json();
        const formattedResponse = response.map(({password ,user_id
          , user_type ,approved	, approved_at , status , ...e})=>{
            return e
        })
       
        return formattedResponse;
      };
      try {
        dispatch(driversActions.setWaitingTrue());
        const data = await getAll();
        dispatch(driversActions.setWaitingFalse());
        dispatch(driversActions.getUnAvaliableDriversFromDb(data));
        dispatch(driversActions.clearDriverError());
      } catch (err) {
        console.log(err);
        dispatch(driversActions.setErrorInGetDrivers(err));
        dispatch(driversActions.setWaitingFalse());
      }
    };
  };

  export const getAllBusyDrivers = () => {
    return async (dispatch) => {
      const getAll = async () => {
        const data = await fetch("http://127.0.0.1:8000/admin/getAll_busy_Drivers");
        const response = await data.json();
        const formattedResponse = response.map(({password ,user_id
          , user_type ,approved	, approved_at , status , ...e})=>{
            return e
        })
       
        return formattedResponse;
      };
      try {
        dispatch(driversActions.setWaitingTrue());
        const data = await getAll();
        dispatch(driversActions.setWaitingFalse());
        dispatch(driversActions.getBusyDriversFromDb(data));
        dispatch(driversActions.clearDriverError());
      } catch (err) {
        console.log(err);
        dispatch(driversActions.setErrorInGetDrivers(err));
        dispatch(driversActions.setWaitingFalse());
      }
    };
  };


  export const getSingleDriver = (id) => {
    return async (dispatch) => {
      const getAll = async () => {
        const data = await fetch(`http://127.0.0.1:8000/admin/view_driver_details/${id}/`);
  
        const response = await data.json();
        
        const formattedData = JSON.parse(response)
        console.log(formattedData)
        return formattedData
      };
      try {
        dispatch(driversActions.setWaitingTrue());
        const data = await getAll();
        dispatch(driversActions.setWaitingFalse());
        console.log(data)
        dispatch(driversActions.setSelectingDriver(data));
        dispatch(driversActions.clearDriverError());
      } catch (err) {
        console.log(err);
        dispatch(driversActions.setErrorInGetDrivers(err));
        dispatch(driversActions.setWaitingFalse());
      }
    };
  };

  export const updateDriver = (id , information) => {
  
    return async (dispatch) => {
      const getAll = async () => {
         await fetch(`http://127.0.0.1:8000/admin/updateDriver/${id}/` , {
          method : 'PATCH' , 
          body : JSON.stringify({...information}) 
        });
  
       
      };
      try {
        dispatch(driversActions.setWaitingTrue());
        await getAll();
        dispatch(driversActions.setWaitingFalse());
        dispatch(driversActions.clearDriverError());
        dispatch(driversActions.requireRender());
        dispatch(toastActions.setToast({message : `Driver Updated` , close : 5000 , type : 'success' }))
      } catch (err) {
        console.log(err);
        dispatch(driversActions.setErrorInGetDrivers(err));
        dispatch(driversActions.setWaitingFalse());
      }
    };
  };
  
  export const deleteDriver = (id , navigateFn) => {
    
    return async (dispatch) => {
      const getAll = async () => {
         await fetch(`http://127.0.0.1:8000/admin/deleteDriver/${id}/` , {
          method : 'DELETE' , 
  
        });
  
      };
      try {
        dispatch(driversActions.setWaitingTrue());
        await getAll();
        dispatch(driversActions.setWaitingFalse());
        dispatch(driversActions.clearDriverError());
        dispatch(driversActions.requireRender());
        dispatch(toastActions.setToast({message : `Driver Deleted` , close : 5000 , type : 'success' }))
        navigateFn()
      } catch (err) {
        console.log(err);
        dispatch(driversActions.setErrorInGetDrivers(err));
        dispatch(driversActions.setWaitingFalse());
      }
    };
  };