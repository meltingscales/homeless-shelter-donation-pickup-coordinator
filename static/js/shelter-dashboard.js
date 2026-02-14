// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    if (!requireAuth()) return;

    const user = getCurrentUser();

    if (user.role !== 'shelter_staff' && user.role !== 'admin') {
        alert('This page is for shelter staff only');
        window.location.href = '/';
        return;
    }

    if (user.shelter_id) {
        document.getElementById('shelterName').textContent = 'Shelter #' + user.shelter_id;
        loadNearbyDonations();
        loadClaimedDonations();
        loadRoutes();
        loadStats();
    }
});

// Show tab
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    // Show selected tab
    document.getElementById(tabName + 'Tab').style.display = 'block';
    event.target.classList.add('active');
}

// Load nearby donations
async function loadNearbyDonations() {
    const zip = document.getElementById('zipFilter').value;
    const radius = document.getElementById('radiusFilter').value || 25;
    const listEl = document.getElementById('donationsList');

    let url = `/api/donations?status=available`;
    if (zip) {
        url += `&zip_code=${zip}`;
    }

    try {
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            const donations = await response.json();
            renderDonations(donations, 'donationsList', true);
        } else {
            listEl.innerHTML = '<div class="no-results">Failed to load donations</div>';
        }
    } catch (err) {
        listEl.innerHTML = '<div class="no-results">Error loading donations</div>';
    }
}

// Load claimed donations
async function loadClaimedDonations() {
    const listEl = document.getElementById('claimedList');

    try {
        const response = await fetch(`/api/donations?status=claimed`, {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            const donations = await response.json();
            // Filter for donations claimed by this shelter
            const user = getCurrentUser();
            const ourClaims = donations.filter(d => d.claimed_by_id === user.shelter_id);
            renderDonations(ourClaims, 'claimedList', false);
        } else {
            listEl.innerHTML = '<div class="no-results">Failed to load claims</div>';
        }
    } catch (err) {
        listEl.innerHTML = '<div class="no-results">Error loading claims</div>';
    }
}

// Load routes
async function loadRoutes() {
    const listEl = document.getElementById('routesList');

    try {
        const response = await fetch('/api/routes', {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            const routes = await response.json();
            renderRoutes(routes);
        } else {
            listEl.innerHTML = '<div class="no-results">Failed to load routes</div>';
        }
    } catch (err) {
        listEl.innerHTML = '<div class="no-results">Error loading routes</div>';
    }
}

// Render donations list
function renderDonations(donations, containerId, showClaimButton) {
    const listEl = document.getElementById(containerId);

    if (donations.length === 0) {
        listEl.innerHTML = '<div class="no-results">No donations found</div>';
        return;
    }

    listEl.innerHTML = donations.map(d => `
        <div class="donation-card">
            <div class="donation-header">
                <span class="donation-id">#${d.id}</span>
                <span class="donation-date">${new Date(d.created_at).toLocaleDateString()}</span>
            </div>
            <div class="donation-items">
                ${escapeHtml(d.items_summary || 'No items')}
            </div>
            ${d.notes ? `<div class="donation-notes">${escapeHtml(d.notes)}</div>` : ''}
            <div class="donation-location">
                📍 ${escapeHtml(d.address)}, ${escapeHtml(d.city)}, ${d.state} ${d.zip_code}
            </div>
            <div class="donation-contact">
                👤 ${escapeHtml(d.donor_name)} - ${escapeHtml(d.donor_email)}
                ${d.donor_phone ? ` (${escapeHtml(d.donor_phone)})` : ''}
            </div>
            <div style="margin-top: 10px;">
                <span class="status-badge status-${d.status}">${formatStatus(d.status)}</span>
            </div>
            ${showClaimButton && d.status === 'available' ? `
                <button class="btn btn-primary btn-small" style="margin-top: 10px;" onclick="claimDonation(${d.id})">
                    Claim This Donation
                </button>
            ` : ''}
        </div>
    `).join('');
}

// Render routes list
function renderRoutes(routes) {
    const listEl = document.getElementById('routesList');

    if (routes.length === 0) {
        listEl.innerHTML = '<div class="no-results">No routes found. Create your first route!</div>';
        return;
    }

    listEl.innerHTML = routes.map(r => `
        <div class="donation-card">
            <div class="donation-header">
                <span class="donation-id">Route: ${escapeHtml(r.name)}</span>
                <span class="donation-date">${new Date(r.created_at).toLocaleDateString()}</span>
            </div>
            ${r.description ? `<div class="donation-notes">${escapeHtml(r.description)}</div>` : ''}
            <div>Status: <span class="status-badge status-${r.status}">${formatStatus(r.status)}</span></div>
            <div style="margin-top: 10px;">
                ${r.pickups ? `${r.pickups.length} pickups` : '0 pickups'}
            </div>
        </div>
    `).join('');
}

// Claim a donation
async function claimDonation(donationId) {
    try {
        const response = await fetch(`/api/donations/${donationId}/claim`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        if (response.ok) {
            alert('Donation claimed successfully!');
            loadNearbyDonations();
            loadStats();
        } else {
            const error = await response.json();
            alert('Failed to claim: ' + (error.detail || 'Unknown error'));
        }
    } catch (err) {
        alert('Error claiming donation');
    }
}

// Load stats
async function loadStats() {
    try {
        const [availableResp, claimedResp, routesResp] = await Promise.all([
            fetch('/api/donations?status=available', { headers: getAuthHeaders() }),
            fetch('/api/donations?status=claimed', { headers: getAuthHeaders() }),
            fetch('/api/routes', { headers: getAuthHeaders() })
        ]);

        if (availableResp.ok) {
            const available = await availableResp.json();
            document.getElementById('availableCount').textContent = available.length;
        }

        if (claimedResp.ok) {
            const claimed = await claimedResp.json();
            const user = getCurrentUser();
            const ourClaims = claimed.filter(d => d.claimed_by_id === user.shelter_id);
            document.getElementById('claimedCount').textContent = ourClaims.length;
        }

        if (routesResp.ok) {
            const routes = await routesResp.json();
            document.getElementById('routesCount').textContent = routes.length;
        }
    } catch (err) {
        console.error('Failed to load stats');
    }
}

// Create route
async function handleCreateRoute(e) {
    e.preventDefault();

    const user = getCurrentUser();
    if (!user.shelter_id) {
        alert('Please register a shelter first');
        showRegisterModal();
        return;
    }

    const payload = {
        name: document.getElementById('routeName').value,
        description: document.getElementById('routeDescription').value || null,
        shelter_id: user.shelter_id,
        driver_user_id: user.id
    };

    try {
        const response = await fetch('/api/routes', {
            method: 'POST',
            headers: {
                ...getAuthHeaders(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert('Route created successfully!');
            document.getElementById('createRouteForm').reset();
            loadRoutes();
            loadStats();
        } else {
            const error = await response.json();
            alert('Failed to create route: ' + (error.detail || 'Unknown error'));
        }
    } catch (err) {
        alert('Error creating route');
    }
}

// Register shelter
function showRegisterModal() {
    document.getElementById('registerModal').style.display = 'flex';
}

function closeRegisterModal() {
    document.getElementById('registerModal').style.display = 'none';
    document.getElementById('registerShelterForm').reset();
    document.getElementById('shelterError').style.display = 'none';
}

async function handleRegisterShelter(e) {
    e.preventDefault();
    const errorEl = document.getElementById('shelterError');

    const payload = {
        name: document.getElementById('shelterNameInput').value,
        contact_name: document.getElementById('shelterContact').value,
        email: document.getElementById('shelterEmail').value,
        address: document.getElementById('shelterAddress').value,
        city: document.getElementById('shelterCity').value,
        state: document.getElementById('shelterState').value,
        zip_code: document.getElementById('shelterZip').value,
        description: document.getElementById('shelterDescription').value || null,
        needed_items_text: document.getElementById('shelterNeeds').value || null
    };

    const phone = document.getElementById('shelterPhone').value;
    if (phone) payload.phone = phone;

    try {
        const response = await fetch('/api/shelters', {
            method: 'POST',
            headers: {
                ...getAuthHeaders(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert('Shelter registered! Please log out and re-register your account with the shelter ID.');
            closeRegisterModal();
        } else {
            const error = await response.json();
            errorEl.textContent = error.detail || 'Failed to register shelter';
            errorEl.style.display = 'block';
        }
    } catch (err) {
        errorEl.textContent = 'Network error. Please try again.';
        errorEl.style.display = 'block';
    }
}

// Format status
function formatStatus(status) {
    return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
