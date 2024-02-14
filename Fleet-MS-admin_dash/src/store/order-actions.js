import { ordersActions } from "./orderSlice";

export const getAllOrders = () => {
  return async (dispatch) => {
    const getAll = async () => {
      const data = await fetch("http://127.0.0.1:8000/admin/get_all_orders");

      const response = await data.json();

      
     
      return response.orders
    };
    try {
      dispatch(ordersActions.setWaitingTrue());
      const data = await getAll();
      dispatch(ordersActions.setWaitingFalse());
      dispatch(ordersActions.getOrdersFromDB(data));
      dispatch(ordersActions.clearOrdersError());
    } catch (err) {
      
      dispatch(ordersActions.setErrorInGetOrders(err));
      dispatch(ordersActions.setWaitingFalse());
    }
  };
};
