// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    if (!requireAuth()) return;

    const user = getCurrentUser();
    document.getElementById('userName').textContent = user.name;

    loadMyDonations();
    loadStats();
});

// Load user's donations
async function loadMyDonations() {
    const status = document.getElementById('statusFilter').value;
    const listEl = document.getElementById('donationsList');

    let url = '/api/donations/my-donations';
    if (status) {
        url = `/api/donations/my-donations?status=${status}`;
    }

    try {
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            const donations = await response.json();
            renderDonations(donations);
        } else {
            listEl.innerHTML = '<div class="no-results">Failed to load donations</div>';
        }
    } catch (err) {
        listEl.innerHTML = '<div class="no-results">Error loading donations</div>';
    }
}

// Render donations list
function renderDonations(donations) {
    const listEl = document.getElementById('donationsList');

    if (donations.length === 0) {
        listEl.innerHTML = '<div class="no-results">No donations found. Create your first donation!</div>';
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
            <div style="margin-top: 10px;">
                <span class="status-badge status-${d.status}">${formatStatus(d.status)}</span>
            </div>
        </div>
    `).join('');
}

// Load stats
async function loadStats() {
    try {
        const response = await fetch('/api/donations/my-donations', {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            const donations = await response.json();

            document.getElementById('totalDonations').textContent = donations.length;
            document.getElementById('availableDonations').textContent =
                donations.filter(d => d.status === 'available').length;
            document.getElementById('claimedDonations').textContent =
                donations.filter(d => d.status === 'claimed').length;
        }
    } catch (err) {
        console.error('Failed to load stats');
    }
}

// Show create modal
function showCreateModal() {
    document.getElementById('createModal').style.display = 'flex';
    const user = getCurrentUser();
    if (user) {
        document.getElementById('donorName').value = user.name;
        document.getElementById('donorEmail').value = user.email;
    }
}

// Close create modal
function closeCreateModal() {
    document.getElementById('createModal').style.display = 'none';
    document.getElementById('createDonationForm').reset();
    document.getElementById('createError').style.display = 'none';
}

// Handle create donation
async function handleCreateDonation(e) {
    e.preventDefault();
    const errorEl = document.getElementById('createError');

    const payload = {
        donor_name: document.getElementById('donorName').value,
        donor_email: document.getElementById('donorEmail').value,
        address: document.getElementById('donorAddress').value,
        city: document.getElementById('donorCity').value,
        state: document.getElementById('donorState').value,
        zip_code: document.getElementById('donorZip').value,
        items_text: document.getElementById('donorItems').value,
        notes: document.getElementById('donorNotes').value || null
    };

    const phone = document.getElementById('donorPhone').value;
    if (phone) payload.donor_phone = phone;

    try {
        const response = await fetch('/api/donations', {
            method: 'POST',
            headers: {
                ...getAuthHeaders(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            closeCreateModal();
            loadMyDonations();
            loadStats();
        } else {
            const error = await response.json();
            errorEl.textContent = error.detail || 'Failed to create donation';
            errorEl.style.display = 'block';
        }
    } catch (err) {
        errorEl.textContent = 'Network error. Please try again.';
        errorEl.style.display = 'block';
    }
}

// Format status for display
function formatStatus(status) {
    return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
