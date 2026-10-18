/**
 * StockSense AI - Global Client Application JavaScript
 * Handles global stock search, dynamic watchlist toggles, transaction modals, and real-time helpers.
 */

// Helper: Get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const CSRF_TOKEN = getCookie('csrftoken');

// Initialize Lucide icons if available
document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }
  setupGlobalSearch();
});

// Global Stock Quick-Search with Autocomplete
function setupGlobalSearch() {
  const searchInput = document.getElementById('globalStockSearch');
  const dropdown = document.getElementById('globalSearchDropdown');
  if (!searchInput || !dropdown) return;

  let debounceTimer;

  searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    const query = e.target.value.trim();

    if (query.length < 1) {
      dropdown.style.display = 'none';
      dropdown.innerHTML = '';
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/stocks/?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        const results = data.results || [];

        if (results.length === 0) {
          dropdown.innerHTML = `<div style="padding: 12px; color: var(--text-muted); font-size: 13px;">No stocks matching "${query}"</div>`;
          dropdown.style.display = 'block';
          return;
        }

        dropdown.innerHTML = results.slice(0, 8).map(s => `
          <a href="/stocks/${s.symbol}/" style="display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; border-bottom: 1px solid var(--border-subtle); color: var(--text-primary); text-decoration: none;">
            <div>
              <div style="font-weight: 600; font-size: 13px;">${s.symbol}</div>
              <div style="font-size: 11px; color: var(--text-muted);">${s.name}</div>
            </div>
            <div style="text-align: right;">
              <span class="brand-tag">${s.exchange}</span>
            </div>
          </a>
        `).join('');

        dropdown.style.display = 'block';
      } catch (err) {
        console.error('Search error:', err);
      }
    }, 250);
  });

  // Close dropdown on outside click
  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });
}

// Watchlist Fast Toggle
async function toggleWatchlist(symbol, buttonElement) {
  try {
    const res = await fetch(`/api/watchlists/toggle/${symbol}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CSRF_TOKEN || ''
      },
      body: JSON.stringify({})
    });
    const data = await res.json();

    if (data.success) {
      if (buttonElement) {
        if (data.is_in_watchlist) {
          buttonElement.classList.add('btn-secondary');
          buttonElement.classList.remove('btn-primary');
          buttonElement.innerHTML = `★ In Watchlist`;
        } else {
          buttonElement.classList.remove('btn-secondary');
          buttonElement.classList.add('btn-primary');
          buttonElement.innerHTML = `☆ Add to Watchlist`;
        }
      }
    } else {
      alert(data.error || 'Failed to update watchlist');
    }
  } catch (err) {
    console.error('Toggle error:', err);
  }
}

// Modal Controllers
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.style.display = 'flex';
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.style.display = 'none';
}
