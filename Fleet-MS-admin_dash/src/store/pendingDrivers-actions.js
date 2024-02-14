import {toastActions} from './toastSlice'
import { pendingDriversActions } from "./pendingDriversSlice";
export const getAllPendingDrivers = () => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch(
        "http://127.0.0.1:8000/admin/getAll_driver_Users"
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
      dispatch(pendingDriversActions.setWaitingTrue());
      const data = await getAll();
      dispatch(pendingDriversActions.setWaitingFalse());
      dispatch(pendingDriversActions.getPendingDriversFromDb(data));
      dispatch(pendingDriversActions.clearPendingDriversError());
    } catch (err) {
      dispatch(pendingDriversActions.setErrorInGetPendingDrivers(err));
      dispatch(pendingDriversActions.setWaitingFalse());
    }
  };
};

export const approvePendingDiver = (id) => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch(
        `http://127.0.0.1:8000/admin/approve_driver/${id}/`,
        {
          method: "PUT",
        }
      );
      const response = await data.json();
      return response;
    };
    try {
      dispatch(pendingDriversActions.setWaitingTrue());
      await getAll();
      dispatch(pendingDriversActions.setWaitingFalse());
      dispatch(pendingDriversActions.requireRender());
      dispatch(pendingDriversActions.clearPendingDriversError());
      dispatch(toastActions.setToast({message : `Driver Approved` , close : 5000 , type : 'success' }))
    } catch (err) {
      dispatch(pendingDriversActions.setErrorInGetPendingDrivers(err));
      dispatch(pendingDriversActions.setWaitingFalse());
    }
  };
};
