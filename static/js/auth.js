// API base URL
const API_BASE = window.location.origin;

// Token storage
const TOKEN_KEY = 'shelter_token';
const USER_KEY = 'shelter_user';

// Get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem(TOKEN_KEY);
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

// Check if user is logged in
function checkAuth() {
    const token = localStorage.getItem(TOKEN_KEY);
    const user = JSON.parse(localStorage.getItem(USER_KEY) || 'null');

    if (token && user) {
        // Show logged in state
        document.getElementById('authSection').style.display = 'none';
        const userSection = document.getElementById('userSection');
        userSection.style.display = 'block';
        document.getElementById('welcomeMessage').textContent = `Welcome, ${user.name}!`;
        document.getElementById('userRole').textContent = roleDisplay(user.role);

        // Show appropriate dashboard link
        if (user.role === 'donor') {
            document.getElementById('donorDashboard').style.display = 'inline-block';
        } else if (user.role === 'shelter_staff') {
            document.getElementById('shelterDashboard').style.display = 'inline-block';
        } else if (user.role === 'admin') {
            document.getElementById('donorDashboard').style.display = 'inline-block';
            document.getElementById('shelterDashboard').style.display = 'inline-block';
        }
    } else {
        // Show logged out state
        document.getElementById('authSection').style.display = 'grid';
        document.getElementById('userSection').style.display = 'none';
    }
}

function roleDisplay(role) {
    const roles = {
        'donor': 'Donor',
        'shelter_staff': 'Shelter Staff',
        'admin': 'Administrator'
    };
    return roles[role] || role;
}

// Show login modal
function showLogin() {
    document.getElementById('loginModal').style.display = 'flex';
    document.getElementById('registerModal').style.display = 'none';
}

// Show register modal
function showRegister() {
    document.getElementById('registerModal').style.display = 'flex';
    document.getElementById('loginModal').style.display = 'none';
}

// Close all modals
function closeModals() {
    document.getElementById('loginModal').style.display = 'none';
    document.getElementById('registerModal').style.display = 'none';
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const errorEl = document.getElementById('loginError');

    try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem(TOKEN_KEY, data.access_token);
            localStorage.setItem(USER_KEY, JSON.stringify(data.user));
            closeModals();
            checkAuth();
        } else {
            const error = await response.json();
            errorEl.textContent = error.detail || 'Login failed';
            errorEl.style.display = 'block';
        }
    } catch (err) {
        errorEl.textContent = 'Network error. Please try again.';
        errorEl.style.display = 'block';
    }
}

// Handle registration
async function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const role = document.getElementById('registerRole').value;
    const shelterId = document.getElementById('registerShelterId').value;
    const phone = document.getElementById('registerPhone').value;
    const errorEl = document.getElementById('registerError');

    const payload = { name, email, password, role };
    if (phone) payload.phone = phone;
    if (role === 'shelter_staff') {
        payload.shelter_id = shelterId ? parseInt(shelterId) : null;
    }

    try {
        const response = await fetch(`${API_BASE}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem(TOKEN_KEY, data.access_token);
            localStorage.setItem(USER_KEY, JSON.stringify(data.user));
            closeModals();
            checkAuth();
        } else {
            const error = await response.json();
            errorEl.textContent = error.detail || 'Registration failed';
            errorEl.style.display = 'block';
        }
    } catch (err) {
        errorEl.textContent = 'Network error. Please try again.';
        errorEl.style.display = 'block';
    }
}

// Logout
function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    window.location.reload();
}

// Get current user
function getCurrentUser() {
    return JSON.parse(localStorage.getItem(USER_KEY) || 'null');
}

// Check if user has specific role
function hasRole(role) {
    const user = getCurrentUser();
    return user && user.role === role;
}

// Redirect if not authenticated
function requireAuth() {
    if (!localStorage.getItem(TOKEN_KEY)) {
        window.location.href = '/';
        return false;
    }
    return true;
}

// Redirect if not the right role
function requireRole(role) {
    if (!requireAuth()) return false;
    if (!hasRole(role)) {
        alert('Access denied');
        window.location.href = '/';
        return false;
    }
    return true;
}
