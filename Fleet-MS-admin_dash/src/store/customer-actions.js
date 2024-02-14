import { customersActions } from "./customerSlice";
import { toastActions } from './toastSlice'
export const getAllCustomers = () => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch("http://127.0.0.1:8000/admin/get_all_customers");
      const response = await data.json();
      let jsonData = JSON.parse(response)
      const formatResponse = jsonData.map(({ confirm_password, password, cart, ...e }) => {
        return e
      })
      console.log(formatResponse)
      return formatResponse
    };
    try {
      dispatch(customersActions.setWaitingTrue());
      dispatch(customersActions.clearCustomerError());
      const data = await getAll();
      dispatch(customersActions.setWaitingFalse());
      dispatch(customersActions.getCustomersFromDb(data));

    } catch (err) {
      dispatch(customersActions.setErrorInGetCustomers(err));
      dispatch(customersActions.setWaitingFalse());
    }
  };
};


export const getSingleCustomer = (id) => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch(`http://127.0.0.1:8000/admin/getCustomer/${id}/`);

      const response = await data.json();
      let jsonData = JSON.parse(response)
      console.log(response)


      return jsonData
    };
    try {
      dispatch(customersActions.setWaitingTrue());
      const data = await getAll();
      dispatch(customersActions.setWaitingFalse());
      console.log(data)
      dispatch(customersActions.setSelectingCustomer(data));
      dispatch(customersActions.clearCustomerError());
    } catch (err) {
      console.log(err);
      dispatch(customersActions.setErrorInGetCustomers(err));
      dispatch(customersActions.setWaitingFalse());
    }
  };
};

export const updateCustomer = (id, customerInformation) => {

  return async (dispatch) => {
    const getAll = async () => {
      await fetch(`http://127.0.0.1:8000/admin/updateCustomer/${id}/`, {
        method: 'PATCH',
        body: JSON.stringify({ ...customerInformation })
      });


    };
    try {
      dispatch(customersActions.setWaitingTrue());
      await getAll();
      dispatch(customersActions.setWaitingFalse());
      dispatch(customersActions.clearCustomerError());
      dispatch(customersActions.requireRender());
      dispatch(toastActions.setToast({ message: `Customer Updated`, close: 5000, type: 'success' }))
    } catch (err) {
      console.log(err);
      dispatch(customersActions.setErrorInGetCustomers(err));
      dispatch(customersActions.setWaitingFalse());
    }
  };
};

export const deleteCustomer = (id, navigateFn) => {

  return async (dispatch) => {
    const getAll = async () => {
      await fetch(`http://127.0.0.1:8000/admin/deleteCustomer/${id}/`, {
        method: 'DELETE',

      });

    };
    try {
      dispatch(customersActions.setWaitingTrue());
      await getAll();
      dispatch(customersActions.setWaitingFalse());
      dispatch(customersActions.clearCustomerError());
      dispatch(customersActions.requireRender());
      dispatch(toastActions.setToast({ message: `Customer Deleted`, close: 5000, type: 'success' }))
      navigateFn()
    } catch (err) {
      console.log(err);
      dispatch(customersActions.setErrorInGetCustomers(err));
      dispatch(customersActions.setWaitingFalse());
    }
  };
};