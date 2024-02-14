
const API_URL = import.meta.env.VITE_APP_API_URL;



export async function startSimulation (speed, drivers_number) {
    const body = JSON.stringify({
        speed,
        drivers_number
    });

    try {
        const apiRes = await fetch(`${API_URL}/map/start_simulation`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: body
        });
        const res = await apiRes.json();
        if (apiRes.status === 200) {
            return res;
        } else {
            return apiRes.error
        }
    } catch(err) {
        return {error: 'somthing went wrong try again'};
    }


};
