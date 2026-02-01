const API_URL = 'http://127.0.0.1:8000/api';

async function register(email, password) {
    console.log(' register() called');
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        console.log(' Register response status:', response.status);
        
        if (!response.ok) {
            const error = await response.json();
            console.error('Register error:', error);
            throw new Error('Registration failed');
        }
        
        const data = await response.json();
        console.log('Register success:', data);
        return data;
    } catch (error) {
        console.error('Register exception:', error);
        throw error;
    }
}

async function login(email, password) {
    console.log(' login() called with:', email);
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                username: email,
                password: password
            })
        });
        
        console.log(' Login response status:', response.status);
        console.log(' Login response ok:', response.ok);
        
        if (!response.ok) {
            const error = await response.json();
            console.error('Login error response:', error);
            throw new Error('Invalid credentials');
        }
        
        const data = await response.json();
        console.log('Login response data:', data);
        
        if (data.access_token) {
            localStorage.setItem('token', data.access_token);
            console.log('Token saved to localStorage');
        } else {
            console.error('No access_token in response');
        }
        
        return data;
    } catch (error) {
        console.error('Login exception:', error);
        throw error;
    }
}

async function searchRoutes(from, to, date) {
    console.log(' searchRoutes() called');
    const token = localStorage.getItem('token');
    let url = `${API_URL}/trains/routes?from_station=${from}&to_station=${to}`;
    if (date) url += `&date=${date}`;
    
    console.log(' Search URL:', url);
    console.log(' Using token:', token ? 'YES' : 'NO');
    
    try {
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        console.log(' Search response status:', response.status);
        
        const data = await response.json();
        console.log(' Search data:', data);
        return data;
    } catch (error) {
        console.error('Search exception:', error);
        throw error;
    }
}

async function createBooking(routeId, carriage, seatNumber) {
    console.log(' createBooking() called');
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/bookings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                route_id: routeId, 
                carriage: carriage,  
                seat_number: seatNumber 
            })
        });
        
        console.log(' Booking response status:', response.status);
        
        if (!response.ok) {
            const error = await response.json();
            console.error('Booking error:', error);
            throw new Error(error.detail || 'Booking failed');
        }
        
        const data = await response.json();
        console.log('Booking data:', data);
        return data;
    } catch (error) {
        console.error('Booking exception:', error);
        throw error;
    }
}

async function getOccupiedSeats(routeId) {
    console.log(' getOccupiedSeats() called');
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/bookings/occupied/${routeId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        console.log('Occupied seats:', data);
        return data.occupied_seats;
    } catch (error) {
        console.error('Get occupied seats exception:', error);
        return [];
    }
}

async function getMyBookings() {
    console.log(' getMyBookings() called');
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/bookings/my`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        console.log(' Get bookings response status:', response.status);
        
        const data = await response.json();
        console.log('Bookings data:', data);
        return data;
    } catch (error) {
        console.error('Get bookings exception:', error);
        throw error;
    }
}

async function cancelBooking(bookingId) {
    console.log(' cancelBooking() called');
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/bookings/${bookingId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        console.log(' Cancel booking response status:', response.status);
        
        const data = await response.json();
        console.log('Cancel data:', data);
        return data;
    } catch (error) {
        console.error('Cancel booking exception:', error);
        throw error;
    }
}