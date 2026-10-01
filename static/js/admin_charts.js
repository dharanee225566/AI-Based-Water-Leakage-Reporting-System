// AquaWatch AI - Chart.js Visual Analytics Engine

document.addEventListener('DOMContentLoaded', () => {
  // Check if Chart.js is loaded
  if (typeof Chart === 'undefined') return;

  // Chart Global Defaults for Modern Clean Aesthetic
  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.color = '#64748b';
  Chart.defaults.borderColor = '#e2e8f0';

  // 1. Admin Dashboard Category Doughnut Chart
  const categoryChartCanvas = document.getElementById('categoryDoughnutChart');
  if (categoryChartCanvas) {
    const rawCategories = JSON.parse(categoryChartCanvas.getAttribute('data-categories') || '{}');
    const labels = Object.keys(rawCategories);
    const dataValues = Object.values(rawCategories);

    new Chart(categoryChartCanvas, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: dataValues,
          backgroundColor: [
            '#0284c7', // Ocean blue - Pipe Leakage
            '#38bdf8', // Sky blue - Tap Leakage
            '#f59e0b', // Amber - Road Flooding
            '#ef4444', // Red - Main Burst
            '#8b5cf6', // Purple - Sewage
            '#64748b'  // Slate - Meter / Other
          ],
          borderWidth: 2,
          borderColor: '#ffffff',
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              padding: 14,
              font: { size: 12, weight: 600 }
            }
          }
        },
        cutout: '68%'
      }
    });
  }

  // 2. Priority Distribution Bar Chart
  const priorityChartCanvas = document.getElementById('priorityBarChart');
  if (priorityChartCanvas) {
    const rawPriorities = JSON.parse(priorityChartCanvas.getAttribute('data-priorities') || '{}');
    const prioLabels = ['High Priority', 'Medium Priority', 'Low Priority'];
    const prioValues = [
      rawPriorities['High'] || 0,
      rawPriorities['Medium'] || 0,
      rawPriorities['Low'] || 0
    ];

    new Chart(priorityChartCanvas, {
      type: 'bar',
      data: {
        labels: prioLabels,
        datasets: [{
          label: 'Active Incident Count',
          data: prioValues,
          backgroundColor: [
            'rgba(239, 68, 68, 0.85)',
            'rgba(245, 158, 11, 0.85)',
            'rgba(16, 185, 129, 0.85)'
          ],
          borderColor: ['#dc2626', '#d97706', '#059669'],
          borderWidth: 1.5,
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            ticks: { precision: 0 }
          },
          x: {
            grid: { display: false }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // 3. Temporal Trend Line Chart (Reported vs Resolved)
  const trendsChartCanvas = document.getElementById('trendsLineChart');
  if (trendsChartCanvas) {
    // Generate recent 7 days labels
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    
    new Chart(trendsChartCanvas, {
      type: 'line',
      data: {
        labels: days,
        datasets: [
          {
            label: 'Reported Incidents',
            data: [3, 5, 2, 8, 4, 6, 7],
            borderColor: '#0284c7',
            backgroundColor: 'rgba(2, 132, 199, 0.12)',
            fill: true,
            tension: 0.35,
            pointBackgroundColor: '#0284c7',
            pointRadius: 5
          },
          {
            label: 'Resolved & Closed',
            data: [2, 3, 4, 6, 5, 5, 6],
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            fill: true,
            tension: 0.35,
            pointBackgroundColor: '#10b981',
            pointRadius: 5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { font: { weight: 600 } }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { precision: 0 }
          }
        }
      }
    });
  }

  // 4. Status Progress Doughnut Chart
  const statusChartCanvas = document.getElementById('statusDoughnutChart');
  if (statusChartCanvas) {
    const rawStatuses = JSON.parse(statusChartCanvas.getAttribute('data-status') || '{}');
    new Chart(statusChartCanvas, {
      type: 'doughnut',
      data: {
        labels: ['Pending', 'Assigned', 'In Progress', 'Resolved'],
        datasets: [{
          data: [
            rawStatuses['Pending'] || 0,
            rawStatuses['Assigned'] || 0,
            rawStatuses['In Progress'] || 0,
            rawStatuses['Resolved'] || 0
          ],
          backgroundColor: ['#f59e0b', '#8b5cf6', '#3b82f6', '#10b981'],
          borderWidth: 2,
          borderColor: '#ffffff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { boxWidth: 10, padding: 12 }
          }
        },
        cutout: '65%'
      }
    });
  }
});
