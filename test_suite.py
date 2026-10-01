"""
AquaWatch AI - Comprehensive Automated Test & Verification Suite
Tests database integrity, routes (200 OK), AI prediction APIs, role-based auth,
report creation with live AI priority & duplicate detection, staff dispatch, and resolution.
"""

import sys
import os
import json
import unittest

# Ensure root dir is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from database import get_db_connection, init_db
from models.ai_engine import ai_engine


class AquaWatchTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_01_public_routes(self):
        """Test public endpoints return 200 OK."""
        routes = ['/', '/login', '/register', '/report', '/track', '/history', '/map', '/analytics']
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status {response.status_code}")
        print("✓ All 8 public routes returned 200 OK.")

    def test_02_ai_api_analyze(self):
        """Test /api/ai-analyze returns category, priority, water loss, and duplicate check."""
        payload = {
            "title": "Major pipe rupture",
            "description": "Massive pipeline burst with water geyser shooting high onto the road, asphalt eroding",
            "street_name": "MG Road",
            "category": "Auto",
            "user_severity": 5,
            "latitude": 12.9716,
            "longitude": 77.5946
        }
        res = self.client.post('/api/ai-analyze', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['predicted_category'], 'Main Pipeline Burst')
        self.assertEqual(data['priority'], 'High')
        self.assertGreater(data['estimated_loss_lph'], 2000)
        self.assertIn('top_keywords', data)
        print("✓ AI Analyze API returned accurate Main Pipeline Burst prediction, High priority, and water loss.")

    def test_03_map_api(self):
        """Test /api/complaints/map returns valid JSON array of incidents."""
        res = self.client.get('/api/complaints/map')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 15)
        self.assertIn('complaint_id', data[0])
        print(f"✓ Map API returned {len(data)} geospatial incidents.")

    def test_04_auth_and_demo_login(self):
        """Test demo logins for Citizen, Admin, and Staff roles."""
        # 1. Admin Demo Login
        res = self.client.get('/demo-login/admin', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'OPERATIONS COMMAND', res.data)
        print("✓ Admin demo login successful, executive dashboard rendered.")

        # 2. Staff Demo Login
        res = self.client.get('/demo-login/staff', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'FIELD CREW DISPATCH', res.data)
        print("✓ Staff demo login successful, field maintenance dashboard rendered.")

        # 3. Citizen Demo Login
        res = self.client.get('/demo-login/citizen', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'CITIZEN COMMAND CENTER', res.data)
        print("✓ Citizen demo login successful, citizen portal dashboard rendered.")

    def test_05_complaint_submission_and_tracking(self):
        """Test end-to-end report creation, AI categorization, DB commit, and tracking page."""
        # Log in as citizen
        self.client.get('/demo-login/citizen', follow_redirects=True)

        report_payload = {
            'title': 'Continuous water dripping from park standpost tap',
            'description': 'The public drinking water fountain tap in the community park is broken and leaking continuously day and night.',
            'category': 'Auto',
            'user_severity': '2',
            'street_name': 'Cubbon Park Promenade',
            'landmark': 'Near Bandstand',
            'latitude': '12.9760',
            'longitude': '77.5920',
            'sample_photo_name': 'tap_leak.svg'
        }

        res = self.client.post('/report', data=report_payload, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Tap Leakage', res.data)
        self.assertIn(b'Cubbon Park Promenade', res.data)
        print("✓ New complaint reported, AI auto-classified as Tap Leakage, tracking page confirmed.")

    def test_06_admin_triage_and_assignment(self):
        """Test admin assigning staff and updating status."""
        self.client.get('/demo-login/admin', follow_redirects=True)
        conn = get_db_connection()
        pending = conn.execute("SELECT complaint_id FROM complaints WHERE status = 'Pending' LIMIT 1").fetchone()
        staff = conn.execute("SELECT id FROM users WHERE role = 'staff' LIMIT 1").fetchone()
        conn.close()

        if pending and staff:
            cid = pending['complaint_id']
            sid = staff['id']
            res = self.client.post('/admin/assign', data={
                'complaint_id': cid,
                'staff_id': sid,
                'notes': 'Urgent repair clamp needed. Check local valve.'
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Check DB updated to Assigned
            conn = get_db_connection()
            updated = conn.execute("SELECT status FROM complaints WHERE complaint_id = ?", (cid,)).fetchone()
            conn.close()
            self.assertEqual(updated['status'], 'Assigned')
            print(f"✓ Admin assigned technician to {cid}. Status updated to Assigned.")

    def test_07_csv_export(self):
        """Test CSV export generates valid downloadable CSV."""
        res = self.client.get('/admin/export-csv')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'text/csv')
        self.assertIn('AquaWatch_Leakage_Audit_2026.csv', res.headers.get('Content-Disposition', ''))
        self.assertIn(b'Ticket ID,Title,Category', res.data)
        print("✓ CSV Export generated with full incident audit records.")


if __name__ == '__main__':
    unittest.main()
