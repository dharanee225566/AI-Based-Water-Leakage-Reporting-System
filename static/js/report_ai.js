// AquaWatch AI - Interactive Leak Report & Live Machine Learning Assistant

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const descInput = document.getElementById('description');
  const titleInput = document.getElementById('title');
  const streetInput = document.getElementById('street_name');
  const categorySelect = document.getElementById('category');
  const severityInput = document.getElementById('user_severity');
  const severityValueLabel = document.getElementById('severity-val-label');
  const latInput = document.getElementById('latitude');
  const lngInput = document.getElementById('longitude');

  // AI Live Preview Elements
  const aiBox = document.getElementById('ai-preview-box');
  const aiCategoryBadge = document.getElementById('ai-cat-badge');
  const aiConfidenceText = document.getElementById('ai-confidence-text');
  const aiConfidenceBar = document.getElementById('ai-confidence-bar');
  const aiPriorityBadge = document.getElementById('ai-priority-badge');
  const aiWaterLossText = document.getElementById('ai-water-loss-text');
  const aiKeywordsList = document.getElementById('ai-keywords-list');
  const aiDuplicateWarning = document.getElementById('ai-duplicate-warning');
  const aiDuplicateDetails = document.getElementById('ai-duplicate-details');

  // Sample photo selector elements
  const samplePhotoCards = document.querySelectorAll('.sample-photo-card');
  const selectedSamplePhotoInput = document.getElementById('sample_photo_name');
  const photoFileInput = document.getElementById('photo');
  const photoPreviewImg = document.getElementById('photo-preview-img');
  const photoPreviewContainer = document.getElementById('photo-preview-container');

  // 1. Initialize Leaflet Map for Pin Drop
  const defaultLat = parseFloat(latInput ? latInput.value : 12.9716) || 12.9716;
  const defaultLng = parseFloat(lngInput ? lngInput.value : 77.5946) || 77.5946;

  let reportMap, marker;
  const mapElement = document.getElementById('report-map');

  if (mapElement && typeof L !== 'undefined') {
    reportMap = L.map('report-map').setView([defaultLat, defaultLng], 14);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(reportMap);

    const customIcon = L.divIcon({
      className: 'custom-pin',
      html: '<div style="background-color:#0284c7; width:22px; height:22px; border-radius:50%; border:3px solid white; box-shadow:0 2px 8px rgba(0,0,0,0.35);"></div>',
      iconSize: [22, 22],
      iconAnchor: [11, 11]
    });

    marker = L.marker([defaultLat, defaultLng], {
      draggable: true,
      icon: customIcon
    }).addTo(reportMap);

    function updateCoordinates(lat, lng) {
      if (latInput) latInput.value = lat.toFixed(5);
      if (lngInput) lngInput.value = lng.toFixed(5);
      triggerAIAnalysis();
    }

    marker.on('dragend', function (e) {
      const position = marker.getLatLng();
      updateCoordinates(position.lat, position.lng);
    });

    reportMap.on('click', function (e) {
      marker.setLatLng(e.latlng);
      updateCoordinates(e.latlng.lat, e.latlng.lng);
    });

    // Detect GPS button
    const locateBtn = document.getElementById('btn-detect-location');
    if (locateBtn) {
      locateBtn.addEventListener('click', () => {
        if ('geolocation' in navigator) {
          locateBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Locating...';
          navigator.geolocation.getCurrentPosition(
            (pos) => {
              const lat = pos.coords.latitude;
              const lng = pos.coords.longitude;
              reportMap.setView([lat, lng], 16);
              marker.setLatLng([lat, lng]);
              updateCoordinates(lat, lng);
              locateBtn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i> GPS Location Found';
              setTimeout(() => {
                locateBtn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i> Detect My GPS Location';
              }, 3000);
            },
            (err) => {
              alert('Could not detect location. Please click directly on the map.');
              locateBtn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i> Detect My GPS Location';
            }
          );
        } else {
          alert('Geolocation is not supported by your browser.');
        }
      });
    }
  }

  // 2. Severity Slider Interaction
  if (severityInput && severityValueLabel) {
    const severityLabels = {
      '1': '1 - Minor Drip / Dampness',
      '2': '2 - Moderate Steady Leak',
      '3': '3 - Notable Pool / Sidewalk Flooding',
      '4': '4 - Heavy Gushing / Road Inundation',
      '5': '5 - Catastrophic Main Burst / Structural Threat'
    };

    severityInput.addEventListener('input', () => {
      severityValueLabel.textContent = severityLabels[severityInput.value] || severityInput.value;
      triggerAIAnalysis();
    });
  }

  // 3. Sample Photo Selection & File Upload Preview
  if (samplePhotoCards.length > 0) {
    samplePhotoCards.forEach(card => {
      card.addEventListener('click', () => {
        samplePhotoCards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        const photoName = card.getAttribute('data-photo');
        if (selectedSamplePhotoInput) selectedSamplePhotoInput.value = photoName;

        // Reset file upload
        if (photoFileInput) photoFileInput.value = '';

        // Show preview
        if (photoPreviewImg && photoPreviewContainer) {
          photoPreviewImg.src = `/static/images/sample_leaks/${photoName}`;
          photoPreviewContainer.style.display = 'block';
        }
      });
    });
  }

  if (photoFileInput) {
    photoFileInput.addEventListener('change', () => {
      if (photoFileInput.files && photoFileInput.files[0]) {
        // Deselect sample photos
        samplePhotoCards.forEach(c => c.classList.remove('selected'));
        if (selectedSamplePhotoInput) selectedSamplePhotoInput.value = '';

        const reader = new FileReader();
        reader.onload = (e) => {
          if (photoPreviewImg && photoPreviewContainer) {
            photoPreviewImg.src = e.target.result;
            photoPreviewContainer.style.display = 'block';
          }
        };
        reader.readAsDataURL(photoFileInput.files[0]);
      }
    });
  }

  // 4. Live AI Analysis Debounce
  let debounceTimer;
  function triggerAIAnalysis() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(performAIAnalysis, 350);
  }

  if (descInput) descInput.addEventListener('input', triggerAIAnalysis);
  if (titleInput) titleInput.addEventListener('input', triggerAIAnalysis);
  if (streetInput) streetInput.addEventListener('input', triggerAIAnalysis);
  if (categorySelect) categorySelect.addEventListener('change', triggerAIAnalysis);

  async function performAIAnalysis() {
    const descText = descInput ? descInput.value.trim() : '';
    if (descText.length < 5) {
      if (aiBox) aiBox.style.opacity = '0.5';
      if (aiDuplicateWarning) aiDuplicateWarning.style.display = 'none';
      return;
    }

    if (aiBox) aiBox.style.opacity = '1';

    try {
      const payload = {
        title: titleInput ? titleInput.value : '',
        description: descText,
        street_name: streetInput ? streetInput.value : '',
        category: categorySelect ? categorySelect.value : '',
        user_severity: severityInput ? parseInt(severityInput.value) : 3,
        latitude: latInput ? parseFloat(latInput.value) : 0.0,
        longitude: lngInput ? parseFloat(lngInput.value) : 0.0
      };

      const response = await fetch('/api/ai-analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) return;
      const data = await response.json();

      // Update AI Category
      if (aiCategoryBadge) {
        aiCategoryBadge.textContent = data.predicted_category;
        // If user hasn't explicitly locked in a category or left it on Auto, auto-update
        if (categorySelect && categorySelect.value === 'Auto') {
          // Keep Auto in select but display prediction
        }
      }

      // Update AI Confidence
      if (aiConfidenceText) aiConfidenceText.textContent = `${data.confidence}%`;
      if (aiConfidenceBar) aiConfidenceBar.style.width = `${Math.min(100, Math.max(10, data.confidence))}%`;

      // Update Priority & Water Loss
      if (aiPriorityBadge) {
        aiPriorityBadge.textContent = `${data.priority} Priority (${data.priority_score}/100)`;
        aiPriorityBadge.className = 'badge';
        if (data.priority === 'High') aiPriorityBadge.classList.add('badge-prio-high');
        else if (data.priority === 'Medium') aiPriorityBadge.classList.add('badge-prio-med');
        else aiPriorityBadge.classList.add('badge-prio-low');
      }

      if (aiWaterLossText) {
        aiWaterLossText.textContent = `~${data.estimated_loss_lph.toLocaleString()} L/hr estimated water loss`;
      }

      // Update Top Keywords
      if (aiKeywordsList && data.top_keywords) {
        aiKeywordsList.innerHTML = data.top_keywords
          .map(kw => `<span class="badge" style="background:#e0f2fe; color:#0369a1; font-size:0.75rem;">${kw}</span>`)
          .join(' ');
      }

      // Check Duplicates
      if (aiDuplicateWarning && aiDuplicateDetails) {
        if (data.duplicate && data.duplicate.is_duplicate) {
          aiDuplicateWarning.style.display = 'flex';
          const match = data.duplicate.match;
          aiDuplicateDetails.innerHTML = `
            <strong>Possible duplicate ticket detected!</strong> 
            A similar incident (<a href="/track?id=${match.complaint_id}" target="_blank" style="text-decoration:underline; font-weight:bold;">${match.complaint_id}</a> - <em>${match.title}</em>) is already active near this location.
            <div style="font-size:0.8rem; margin-top:4px; color:#92400e;">
              Similarity Score: <strong>${data.duplicate.duplicate_score}%</strong> | Match Reason: ${data.duplicate.match_reason}
            </div>
          `;
        } else {
          aiDuplicateWarning.style.display = 'none';
        }
      }

    } catch (err) {
      console.error('Error during AI analysis:', err);
    }
  }

  // Trigger initial check if fields are pre-filled
  if (descInput && descInput.value.length > 5) {
    performAIAnalysis();
  }
});
