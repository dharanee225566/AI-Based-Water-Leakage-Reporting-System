// AquaWatch AI - Interactive City-Wide Leakage GIS Map View

document.addEventListener('DOMContentLoaded', () => {
  const mapElement = document.getElementById('leakage-full-map');
  if (!mapElement || typeof L === 'undefined') return;

  // Filter elements
  const statusFilter = document.getElementById('map-filter-status');
  const categoryFilter = document.getElementById('map-filter-category');
  const priorityFilter = document.getElementById('map-filter-priority');
  const countDisplay = document.getElementById('map-filtered-count');

  // Initialize Map
  const map = L.map('leakage-full-map').setView([12.9716, 77.5946], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors | AquaWatch AI GIS',
    maxZoom: 19
  }).addTo(map);

  let markersLayer = L.layerGroup().addTo(map);
  let allComplaints = [];

  // Helper for pin styling
  function getPinColor(priority, status) {
    if (status === 'Resolved') return '#10b981'; // Green
    if (priority === 'High') return '#ef4444';    // Red
    if (priority === 'Medium') return '#f59e0b';  // Amber
    return '#0284c7';                             // Ocean Blue
  }

  function createMarkerIcon(priority, status) {
    const color = getPinColor(priority, status);
    return L.divIcon({
      className: 'custom-leak-pin',
      html: `
        <div style="
          background-color: ${color};
          width: 24px;
          height: 24px;
          border-radius: 50% 50% 50% 0;
          transform: rotate(-45deg);
          border: 2px solid white;
          box-shadow: 0 3px 8px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          <div style="width: 8px; height: 8px; background: white; border-radius: 50%; transform: rotate(45deg);"></div>
        </div>
      `,
      iconSize: [24, 24],
      iconAnchor: [12, 24],
      popupAnchor: [0, -24]
    });
  }

  async function loadMapData() {
    try {
      const response = await fetch('/api/complaints/map');
      if (!response.ok) throw new Error('Failed to load map data');
      allComplaints = await response.json();
      renderMarkers();
    } catch (err) {
      console.error('Map loading error:', err);
    }
  }

  function renderMarkers() {
    markersLayer.clearLayers();

    const selectedStatus = statusFilter ? statusFilter.value : 'all';
    const selectedCategory = categoryFilter ? categoryFilter.value : 'all';
    const selectedPriority = priorityFilter ? priorityFilter.value : 'all';

    const filtered = allComplaints.filter(c => {
      if (selectedStatus !== 'all' && c.status !== selectedStatus) return false;
      if (selectedCategory !== 'all' && c.category !== selectedCategory) return false;
      if (selectedPriority !== 'all' && c.priority !== selectedPriority) return false;
      return true;
    });

    if (countDisplay) {
      countDisplay.textContent = `${filtered.length} reported leaks displayed`;
    }

    const bounds = [];

    filtered.forEach(c => {
      const lat = parseFloat(c.latitude);
      const lng = parseFloat(c.longitude);

      if (isNaN(lat) || isNaN(lng)) return;

      bounds.push([lat, lng]);

      const marker = L.marker([lat, lng], {
        icon: createMarkerIcon(c.priority, c.status)
      });

      const photoUrl = c.photo_path 
        ? `/static/uploads/${c.photo_path}` 
        : `/static/images/sample_leaks/pipe_leak.svg`;

      const popupContent = `
        <div style="min-width: 240px; font-family: inherit; line-height: 1.4;">
          <img src="${photoUrl}" alt="Leak Photo" style="width: 100%; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 8px; background: #e2e8f0;" onerror="this.src='/static/images/sample_leaks/pipe_leak.svg';">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px;">
            <span style="font-size:0.75rem; font-weight:700; color:#0284c7;">${c.complaint_id}</span>
            <span class="badge badge-${c.status.toLowerCase().replace(' ', '-')}" style="font-size:0.7rem; padding: 2px 6px;">${c.status}</span>
          </div>
          <h4 style="font-size: 0.95rem; margin-bottom: 4px; color:#0f172a;">${c.title}</h4>
          <p style="font-size: 0.8rem; color: #475569; margin-bottom: 6px;">
            <i class="fa-solid fa-location-dot" style="color:#0284c7;"></i> ${c.street_name}
          </p>
          <div style="display:flex; gap:6px; font-size:0.72rem; margin-bottom: 10px;">
            <span class="badge" style="background:#e0f2fe; color:#0369a1;">${c.category}</span>
            <span class="badge" style="background:${c.priority === 'High' ? '#fee2e2' : '#fef3c7'}; color:${c.priority === 'High' ? '#dc2626' : '#b45309'};">${c.priority}</span>
          </div>
          <a href="/track?id=${c.complaint_id}" class="btn btn-primary btn-sm" style="width: 100%; text-align: center; font-size: 0.8rem; padding: 6px 10px;">
            <i class="fa-solid fa-compass"></i> Track Ticket Details
          </a>
        </div>
      `;

      marker.bindPopup(popupContent);
      markersLayer.addLayer(marker);
    });

    if (bounds.length > 0) {
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 });
    }
  }

  // Attach filter event listeners
  if (statusFilter) statusFilter.addEventListener('change', renderMarkers);
  if (categoryFilter) categoryFilter.addEventListener('change', renderMarkers);
  if (priorityFilter) priorityFilter.addEventListener('change', renderMarkers);

  // Initial load
  loadMapData();
});
