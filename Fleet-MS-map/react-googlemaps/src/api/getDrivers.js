
const API_URL = process.env.REACT_APP_API_URL;




export async function get_drivers() {
    try {
        const res = await fetch(`${API_URL}/map/get_all_drivers`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            }
        });

        const data = await res.json();
        if (res.status === 200) {
            return data;
        } else {
            return res.error
        }
    } catch(err) {
        return {error: 'Something went wrong when retrieving restaurants'}
    }
};