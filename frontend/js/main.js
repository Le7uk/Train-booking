document.addEventListener('DOMContentLoaded', function() {

// ==================== LOGIN PAGE ====================
if (window.location.pathname.includes('login.html')) {
    console.log('Login page loaded');
    
    redirectIfLoggedIn();

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            console.log('Form submitted');
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            console.log('Attempting login with:', email);
            
            try {
                await login(email, password);
                const user = await getMe();
                localStorage.setItem('role', user.role);
                console.log('Login successful, role:', user.role);
                window.location.href = 'index.html';
            } catch (error) {
                console.error('Login error:', error);
                document.getElementById('message').innerHTML = 
                    '<p class="error">Invalid email or password</p>';
            }
        });
    }
}

// ==================== REGISTER PAGE ====================
if (window.location.pathname.includes('register.html')) {
    console.log('Register page loaded');
    
    redirectIfLoggedIn();

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            console.log('Form submitted');
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            console.log('Attempting registration with:', email);
            
            try {
                await register(email, password);
                console.log('Registration successful');
                await login(email, password);
                console.log('Auto-login successful');
                window.location.href = 'index.html';
            } catch (error) {
                console.error('Registration error:', error);
                document.getElementById('message').innerHTML = 
                    '<p class="error">Registration failed. Email already exists?</p>';
            }
        });
    }
}

// ==================== INDEX PAGE (SEARCH) ====================
if (window.location.pathname.includes('index.html') || window.location.pathname === '/') {
    requireAuth();

    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const from = document.getElementById('from').value;
            const to = document.getElementById('to').value;
            const date = document.getElementById('date').value;
            
            try {
                const routes = await searchRoutes(from, to, date);
                displayRoutes(routes);
            } catch (error) {
                console.error('Search error:', error);
                alert('Search error');
            }
        });
    }

    window.displayRoutes = function(routes) {
        localStorage.setItem('searchResults', JSON.stringify(routes));
        
        const resultsDiv = document.getElementById('results');
        
        if (routes.length === 0) {
            resultsDiv.innerHTML = '<p>No routes found</p>';
            return;
        }
        
        resultsDiv.innerHTML = routes.map(route => `
            <div class="route-card">
                <h3>Train ${route.train.train_number} - ${route.train.name}</h3>
                <p><strong>${route.from_station}</strong> → <strong>${route.to_station}</strong></p>
                <p>Departure: ${new Date(route.departure_time).toLocaleString('uk-UA')}</p>
                <p>Arrival: ${new Date(route.arrival_time).toLocaleString('uk-UA')}</p>
                <p>Price: ${route.price} USD</p>
                <p>Available seats: ${route.available_seats}</p>
                <button onclick="bookRoute(${route.id})">Book</button>
            </div>
        `).join('');
    }

    window.bookRoute = function(routeId) {
        window.location.href = `booking.html?route=${routeId}`;
    }
}

// ==================== DASHBOARD PAGE ====================
if (window.location.pathname.includes('dashboard.html')) {
    requireAuth();

    async function loadBookings() {
        try {
            const bookings = await getMyBookings();
            displayBookings(bookings);
        } catch (error) {
            console.error('Error loading bookings:', error);
            alert('Error loading bookings: ' + error.message);
        }
    }

    function displayBookings(bookings) {
        const bookingsDiv = document.getElementById('bookings');
        
        if (bookings.length === 0) {
            bookingsDiv.innerHTML = '<p>You have no bookings yet</p>';
            return;
        }
        
        bookingsDiv.innerHTML = bookings.map(booking => `
            <div class="booking-card ${booking.status}">
                <h3>Train ${booking.route.train.train_number}</h3>
                <p><strong>${booking.route.from_station}</strong> → <strong>${booking.route.to_station}</strong></p>
                <p>Carriage: ${booking.carriage || 'N/A'}, Seat: ${booking.seat_number}</p>
                <p>Departure: ${new Date(booking.route.departure_time).toLocaleString('uk-UA')}</p>
                <p>Status: ${booking.status === 'active' ? 'Active' : 'Cancelled'}</p>
                ${booking.status === 'active' ? 
                    `<button onclick="cancelBookingFunc(${booking.id})">Cancel</button>` : 
                    ''}
            </div>
        `).join('');
    }

    window.cancelBookingFunc = async function(bookingId) {
        if (!confirm('Are you sure you want to cancel this booking?')) return;
        
        try {
            await cancelBooking(bookingId);
            alert('Booking cancelled');
            loadBookings();
        } catch (error) {
            console.error('Cancellation error:', error);
            alert('Cancellation error');
        }
    }

    loadBookings();
}

});