import { businessActions } from "./buisnessSlice";
import {toastActions} from './toastSlice'
export const getAllBusiness = () => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch("http://127.0.0.1:8000/admin/getAllBusiness");

      const response = await data.json();
     
      let jsonData = JSON.parse(response)
      const formattedResonse = jsonData.map(({password , ...e})=>{
          return e
      })
      return formattedResonse
    };
    try {
      dispatch(businessActions.setWaitingTrue());
      const data = await getAll();
      dispatch(businessActions.setWaitingFalse());
      dispatch(businessActions.getBuisnessFromDb(data));
      dispatch(businessActions.clearBusinessError());
    } catch (err) {
      console.log(err);
      dispatch(businessActions.setErrorInGetBusiness(err));
      dispatch(businessActions.setWaitingFalse());
    }
  };
};


export const getAllResOrders = () => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch("http://127.0.0.1:8000/admin/get_restaurants_orders");
      const response = await data.json();
      return response.length
    };
    try {
      dispatch(businessActions.setWaitingTrue());
      const data = await getAll();
      dispatch(businessActions.setWaitingFalse());
      dispatch(businessActions.setNumOfResOrders(data));
      dispatch(businessActions.clearBusinessError());
    } catch (err) {
      console.log(err);
      dispatch(businessActions.setErrorInGetBusiness(err));
      dispatch(businessActions.setWaitingFalse());
    }
  };
};


export const getAllMarketOrders = () => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch("http://127.0.0.1:8000/admin/get_market_orders");
      const response = await data.json();
      
      return response.length
    };
    try {
      dispatch(businessActions.setWaitingTrue());
      const data = await getAll();
      dispatch(businessActions.setWaitingFalse());
      dispatch(businessActions.setNumOfMarketOrders(data));
      dispatch(businessActions.clearBusinessError());
    } catch (err) {
      console.log(err);
      dispatch(businessActions.setErrorInGetBusiness(err));
      dispatch(businessActions.setWaitingFalse());
    }
  };
};

export const getSingleBusiness = (id) => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch(`http://127.0.0.1:8000/admin/get_business/${id}`);

      const response = await data.json();
      
      let jsonData = JSON.parse(response)
      console.log(jsonData)
      return jsonData
    };
    try {
      dispatch(businessActions.setWaitingTrue());
      const data = await getAll();
      dispatch(businessActions.setWaitingFalse());
      dispatch(businessActions.setSelectingBuisness(data));
      dispatch(businessActions.clearBusinessError());
    } catch (err) {
      console.log(err);
      dispatch(businessActions.setErrorInGetBusiness(err));
      dispatch(businessActions.setWaitingFalse());
    }
  };
};

export const updateBuisness = (id , businessInformation) => {
  
  return async (dispatch) => {
    const getAll = async () => {
       await fetch(`http://127.0.0.1:8000/admin/update_business/${id}/` , {
        method : 'PATCH' , 
        body : JSON.stringify({...businessInformation}) 
      });

     
    };
    try {
      dispatch(businessActions.setWaitingTrue());
      await getAll();
      dispatch(businessActions.setWaitingFalse());
      dispatch(businessActions.clearBusinessError());
      dispatch(businessActions.requireRender());
      dispatch(toastActions.setToast({message : `Buisness Updated` , close : 5000 , type : 'success' }))
    } catch (err) {
      console.log(err);
      dispatch(businessActions.setErrorInGetBusiness(err));
      dispatch(businessActions.setWaitingFalse());
    }
  };
};

export const deleteBuisness = (id , navigateFn) => {
  
  return async (dispatch) => {
    const getAll = async () => {
       await fetch(`http://127.0.0.1:8000/admin/delete_business/${id}/` , {
        method : 'DELETE' , 

      });

    };
    try {
      dispatch(businessActions.setWaitingTrue());
      await getAll();
      dispatch(businessActions.setWaitingFalse());
      dispatch(businessActions.clearBusinessError());
      dispatch(businessActions.requireRender());
      dispatch(toastActions.setToast({message : `Business Deleted` , close : 5000 , type : 'success' }))
      navigateFn()
    } catch (err) {
      console.log(err);
      dispatch(businessActions.setErrorInGetBusiness(err));
      dispatch(businessActions.setWaitingFalse());
    }
  };
};

export const addNewBuisness = (businessInformation , reset , setError) => {
  
  return async (dispatch) => {
    const getAll = async () => {
      const response =  await fetch(`http://127.0.0.1:8000/admin/add_business` , {
        method : 'POST' , 
        body : JSON.stringify({...businessInformation}) 
      });
       if(response.statusText === "Bad Request") {
          throw new Error('dup')
      }
     
     return response
    };
    try {
      dispatch(businessActions.setWaitingTrue());
      await getAll();
      dispatch(businessActions.setWaitingFalse());
      dispatch(businessActions.clearBusinessError());
      dispatch(businessActions.requireRender());
      dispatch(toastActions.setToast({message : `Business Added` , close : 5000 , type : 'success' }))
      reset()
    } catch (err) {
      dispatch(businessActions.setWaitingFalse());
      console.log(err.message);
      if(err.message === 'dup'){
       await setError('name' , 'Duplicate Buisness Name')
       window.scrollTo({ top: 0, behavior: "smooth" });
      }
      else {
        dispatch(businessActions.setErrorInGetBusiness(err));
      }
            
    }
  };
};
