import { pendingBuisnessActions } from "./pendingBuisnessSlice";
import {toastActions} from './toastSlice'

export const getAllPendingBusiness = () => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch(
        "http://127.0.0.1:8000/admin/getAll_business_Users"
      );

      const response = await data.json();

      let jsonData = JSON.parse(response);
      const formattedResonse = jsonData
        .map(({ password, contact_name, user_type, postal_code, ...e }) => {
          return e;
        })
        .filter((e) => e.approved !== true);
      return formattedResonse;
    };
    try {
      dispatch(pendingBuisnessActions.setWaitingTrue());
      const data = await getAll();
      dispatch(pendingBuisnessActions.setWaitingFalse());
      dispatch(pendingBuisnessActions.getBuisnessFromDb(data));
      dispatch(pendingBuisnessActions.clearBusinessError());
    } catch (err) {
      dispatch(pendingBuisnessActions.setErrorInGetBusiness(err));
      dispatch(pendingBuisnessActions.setWaitingFalse());
    }
  };
};

export const approvePendingBuisness = (id) => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch(
        `http://127.0.0.1:8000/admin/approve_business/${id}/`,
        {
          method: "PUT",
        }
      );
      const response = await data.json();
      return response;
    };
    try {
      dispatch(pendingBuisnessActions.setWaitingTrue());
      await getAll();
      dispatch(pendingBuisnessActions.setWaitingFalse());
      dispatch(pendingBuisnessActions.requireRender());
      dispatch(pendingBuisnessActions.clearBusinessError());
      dispatch(toastActions.setToast({message : `Buisness Approved` , close : 5000 , type : 'success' }))
    } catch (err) {
      dispatch(pendingBuisnessActions.setErrorInGetBusiness(err));
      dispatch(pendingBuisnessActions.setWaitingFalse());
    }
  };
};
