function isLoggedIn() {
    return localStorage.getItem('token') !== null;
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login.html';
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/login.html';
    }
}

function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        window.location.href = '/dashboard.html';
    }
}