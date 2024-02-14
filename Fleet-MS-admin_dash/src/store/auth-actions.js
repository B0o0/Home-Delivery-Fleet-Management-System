import { authActions }  from "./authSlice";
import { toastActions } from "./toastSlice";
export const loginHandler = (email , password , setError)=>{
    return async (dispatch)=>{
        const login = async ()=>{
            
            const data =  await fetch('http://127.0.0.1:8000/admin/login' , {
            method : 'POST' , 
            body : JSON.stringify({email , password}) 
          })
          console.log(data)
          if(data.status === 401) {
            await  setError('email' , 'Invalid Email Or Password')
            await  setError('password' , 'Invalid Email Or Password')
            throw new Error('Invalid Email Or Password')
          }
          if(!data.ok){
            throw new Error('SomeThing Went Wrong')
          }
        }

        try{
            
            dispatch(authActions.setWating(true))
             await login()
            dispatch(authActions.userLogin(email))
        }
        catch(err){
            dispatch(authActions.setWating(false))
            console.log(err.message)
            dispatch(authActions.setErrorInLogin(err.message))
            
        }
    }
}

export const addNewAdmin = (adminInformation , reset , setError) => {
  
  return async (dispatch) => {
    const getAll = async () => {
      const response =  await fetch(`http://127.0.0.1:8000/admin/add_admin` , {
        method : 'POST' , 
        body : JSON.stringify({...adminInformation}) 
      });
      
      console.log(response)
      return response

     
    };
    try {
      dispatch(authActions.setWating(true));
      await getAll();
      dispatch(authActions.setWating(false));
      dispatch(authActions.setErrorInLogin(""));
      dispatch(toastActions.setToast({message : `New Admin Added` , close : 5000 , type : 'success' }))
      reset()
    } catch (err) {
      dispatch(authActions.setWating(false));
      console.log(err.message);
      if(err.message === 'dup'){
       await setError('email' , 'this email exist try another')
       window.scrollTo({ top: 0, behavior: "smooth" });
      }
      else {
        dispatch(authActions.setErrorInLogin(err));
      }
            
    }
  };
};