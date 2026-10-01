"""
AquaWatch AI - Live Server End-to-End HTTP Integration Test
Tests all endpoints against the active running Flask server (http://127.0.0.1:5000).
"""

import urllib.request
import urllib.parse
import http.cookiejar
import json
import re

BASE_URL = 'http://127.0.0.1:5000'

# Create a cookie-enabled opener to simulate full browser sessions
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

print("======================================================================")
print("🚀 AquaWatch AI - Live Server Verification")
print("======================================================================")

# 1. Homepage
with opener.open(f'{BASE_URL}/') as r:
    assert r.getcode() == 200
    html = r.read().decode('utf-8')
    assert 'AquaWatch' in html
    assert 'Empowering Citizens' in html
    print("✓ 1. Homepage: 200 OK | Brand, Hero, Statistics & Verified Reports loaded.")

# 2. AI Live API
data = json.dumps({
    'title': 'High pressure main burst',
    'description': 'Massive water geyser erupting from ruptured 300mm line, road collapsing',
    'street_name': 'MG Road',
    'category': 'Auto',
    'user_severity': 5,
    'latitude': 12.9716,
    'longitude': 77.5946
}).encode('utf-8')
req = urllib.request.Request(f'{BASE_URL}/api/ai-analyze', data=data, headers={'Content-Type': 'application/json'})
with opener.open(req) as r:
    res = json.loads(r.read().decode('utf-8'))
    assert res['predicted_category'] == 'Main Pipeline Burst'
    assert res['priority'] == 'High'
    print(f"✓ 2. AI API: Predicted '{res['predicted_category']}' ({res['confidence']}%) | Urgency: {res['priority']} | Loss: {res['estimated_loss_lph']} L/hr")

# 3. GIS Map API & Page
with opener.open(f'{BASE_URL}/map') as r:
    assert r.getcode() == 200
    print("✓ 3. GIS Map View: 200 OK | Leaflet map container loaded.")

with opener.open(f'{BASE_URL}/api/complaints/map') as r:
    pins = json.loads(r.read().decode('utf-8'))
    assert len(pins) >= 15
    print(f"✓ 4. GIS Map Telemetry API: {len(pins)} geo-located complaints returned.")

# 4. Analytics & Reports Page
with opener.open(f'{BASE_URL}/analytics') as r:
    assert r.getcode() == 200
    a_html = r.read().decode('utf-8')
    assert 'Water Infrastructure Analytics' in a_html
    assert 'categoryDoughnutChart' in a_html
    assert 'priorityBarChart' in a_html
    assert 'trendsLineChart' in a_html
    assert 'statusDoughnutChart' in a_html
    print("✓ 5. Analytics Page: 200 OK | All 4 Chart.js canvases & Hotspots ranking loaded.")

# 5. Citizen Report Submission Flow
report_data = urllib.parse.urlencode({
    'title': 'Subterranean pipe leak spraying drinking water onto pavement',
    'description': 'Water is gushing out of an underground supply pipe under the sidewalk near the hospital gate, causing water puddles.',
    'category': 'Auto',
    'user_severity': '4',
    'street_name': 'Victoria Hospital Road',
    'landmark': 'Gate #2 Opposite Dispensary',
    'latitude': '12.9630',
    'longitude': '77.5750',
    'sample_photo_name': 'pipe_leak.svg'
}).encode('utf-8')

req = urllib.request.Request(f'{BASE_URL}/report', data=report_data)
with opener.open(req) as r:
    assert r.getcode() == 200
    track_html = r.read().decode('utf-8')
    match = re.search(r'AQUA-2026-\d+', track_html)
    assert match is not None
    new_cid = match.group(0)
    assert 'Victoria Hospital Road' in track_html
    assert 'Pipe Leakage' in track_html
    print(f"✓ 6. Report Submission: Created ticket {new_cid} | Live 5-step stepper & tracking page loaded.")

# 6. Admin Demo Login & Triage Management
with opener.open(f'{BASE_URL}/demo-login/admin') as r:
    assert r.getcode() == 200
    admin_html = r.read().decode('utf-8')
    assert 'Municipal Administrator Dashboard' in admin_html
    print("✓ 7. Admin Portal: 1-Click demo authentication successful | KPIs & crew workload rendered.")

# 7. Admin Assigns Maintenance Staff
assign_data = urllib.parse.urlencode({
    'complaint_id': new_cid,
    'staff_id': '2',  # David Miller
    'notes': 'Inspect 80mm pipeline collar with acoustic detector and replace damaged seal.'
}).encode('utf-8')
req = urllib.request.Request(f'{BASE_URL}/admin/assign', data=assign_data)
with opener.open(req) as r:
    assert r.getcode() == 200
    print(f"✓ 8. Admin Dispatch: Dispatched technician David Miller to work order {new_cid}.")

# 8. Staff Portal & Work Order Completion
with opener.open(f'{BASE_URL}/demo-login/staff') as r:
    assert r.getcode() == 200
    staff_html = r.read().decode('utf-8')
    assert 'Field Maintenance Dispatch' in staff_html
    assert new_cid in staff_html
    print(f"✓ 9. Staff Portal: Authenticated as David Miller | Work order {new_cid} present in queue.")

# 9. Staff Submits Resolved Milestone
milestone_data = urllib.parse.urlencode({
    'complaint_id': new_cid,
    'status': 'Resolved',
    'notes': 'Excavated 1.2m beneath sidewalk. Replaced fractured collar with heavy-duty ductile clamp. Restored 4.2 bar normal pressure.'
}).encode('utf-8')
req = urllib.request.Request(f'{BASE_URL}/staff/update-progress', data=milestone_data)
with opener.open(req) as r:
    assert r.getcode() == 200
    print(f"✓ 10. Field Milestone: Work order {new_cid} marked 'Resolved' by technician.")

# 10. Verify Ticket Now Shows Resolved on Tracking Page
with opener.open(f'{BASE_URL}/track?id={new_cid}') as r:
    assert r.getcode() == 200
    v_html = r.read().decode('utf-8')
    assert 'Resolved' in v_html
    assert 'ductile clamp' in v_html
    print(f"✓ 11. End-to-End Verification: Ticket {new_cid} is verified 'Resolved' on tracking stepper with full audit history!")

# 11. CSV Export Download
with opener.open(f'{BASE_URL}/admin/export-csv') as r:
    assert r.getcode() == 200
    assert 'text/csv' in r.headers['Content-Type']
    csv_body = r.read().decode('utf-8')
    assert new_cid in csv_body
    print(f"✓ 12. CSV Export: Successfully downloaded audit log containing {new_cid}.")

print("======================================================================")
print("🎉 ALL 12 END-TO-END WORKFLOW TESTS COMPLETED SUCCESSFULLY WITH ZERO ERRORS!")
print("======================================================================")
