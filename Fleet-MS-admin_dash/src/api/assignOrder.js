
const API_URL = import.meta.env.VITE_APP_API_URL;



export async function assignOrder () {

    try {
        const res = await fetch(`${API_URL}/map/assign_order`, {
            method: 'POST',
        });
        console.log("res", res);
        const data = await res.json();
        return data
        

    } catch(err) {
        return {error: 'Something went wrong when assigning Order'}
    }
};
