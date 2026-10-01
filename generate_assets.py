import os

svg_burst = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <linearGradient id="sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#bae6fd"/>
      <stop offset="100%" stop-color="#e0f2fe"/>
    </linearGradient>
    <linearGradient id="waterJet" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="asphalt" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="url(#sky)"/>
  <rect y="280" width="600" height="120" fill="url(#asphalt)"/>
  <line x1="0" y1="340" x2="600" y2="340" stroke="#facc15" stroke-dasharray="20,20" stroke-width="4"/>
  <ellipse cx="300" cy="290" rx="80" ry="25" fill="#0f172a"/>
  <path d="M260,290 C270,180 230,80 300,40 C370,80 330,180 340,290 Z" fill="url(#waterJet)"/>
  <path d="M280,290 C290,140 260,60 300,30 C340,60 310,140 320,290 Z" fill="#ffffff" opacity="0.7"/>
  <circle cx="240" cy="90" r="12" fill="#38bdf8" opacity="0.7"/>
  <circle cx="360" cy="80" r="14" fill="#38bdf8" opacity="0.7"/>
  <circle cx="210" cy="140" r="8" fill="#0284c7" opacity="0.8"/>
  <circle cx="390" cy="130" r="10" fill="#0284c7" opacity="0.8"/>
  <circle cx="190" cy="220" r="15" fill="#7dd3fc" opacity="0.6"/>
  <circle cx="420" cy="210" r="16" fill="#7dd3fc" opacity="0.6"/>
  <ellipse cx="300" cy="305" rx="190" ry="35" fill="#0284c7" opacity="0.55"/>
  <ellipse cx="300" cy="310" rx="140" ry="20" fill="#38bdf8" opacity="0.7"/>
  <text x="300" y="380" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">CRITICAL MAIN PIPELINE BURST (PHOTO EVIDENCE)</text>
</svg>'''

svg_pipe = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <linearGradient id="pipeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="50%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="#f1f5f9"/>
  <rect y="240" width="600" height="160" fill="#78716c"/>
  <rect y="200" width="600" height="40" fill="#cbd5e1"/>
  <rect x="50" y="250" width="500" height="50" rx="10" fill="url(#pipeGrad)"/>
  <rect x="180" y="245" width="25" height="60" rx="4" fill="#1e293b"/>
  <rect x="380" y="245" width="25" height="60" rx="4" fill="#1e293b"/>
  <path d="M290,265 L310,285 L305,290 L285,270 Z" fill="#0f172a"/>
  <path d="M295,265 C310,210 320,160 300,120 C280,160 290,210 295,265 Z" fill="#38bdf8" opacity="0.8"/>
  <ellipse cx="300" cy="200" rx="90" ry="15" fill="#0284c7" opacity="0.6"/>
  <text x="300" y="375" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">UNDERGROUND PIPE JOINT LEAKAGE EVIDENCE</text>
</svg>'''

svg_flood = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#94a3b8"/>
  <rect x="40" y="100" width="90" height="160" fill="#475569"/>
  <rect x="160" y="70" width="110" height="190" fill="#334155"/>
  <rect x="310" y="110" width="130" height="150" fill="#475569"/>
  <rect x="480" y="80" width="80" height="180" fill="#1e293b"/>
  <rect y="250" width="600" height="150" fill="#0284c7" opacity="0.85"/>
  <path d="M0,270 Q150,255 300,270 T600,270" fill="none" stroke="#38bdf8" stroke-width="4"/>
  <path d="M0,310 Q150,295 300,310 T600,310" fill="none" stroke="#e0f2fe" stroke-width="3"/>
  <path d="M0,350 Q150,335 300,350 T600,350" fill="none" stroke="#bae6fd" stroke-width="2.5"/>
  <polygon points="290,290 310,290 300,230" fill="#ea580c"/>
  <rect x="294" y="255" width="12" height="8" fill="#ffffff"/>
  <text x="300" y="385" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">ROADWAY INUNDATION &amp; OVERFLOW</text>
</svg>'''

svg_tap = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f8fafc"/>
  <rect x="100" y="140" width="160" height="40" rx="5" fill="#64748b"/>
  <path d="M260,130 L320,130 L320,200 L280,200 L280,170 L260,170 Z" fill="#94a3b8" stroke="#475569" stroke-width="3"/>
  <rect x="305" y="90" width="30" height="15" rx="3" fill="#ef4444"/>
  <rect x="315" y="105" width="10" height="25" fill="#64748b"/>
  <path d="M280,200 L320,200 L315,225 L285,225 Z" fill="#64748b"/>
  <path d="M300,235 C295,245 290,255 300,265 C310,255 305,245 300,235 Z" fill="#0284c7"/>
  <path d="M300,285 C293,297 288,310 300,320 C312,310 307,297 300,285 Z" fill="#38bdf8"/>
  <ellipse cx="300" cy="350" rx="70" ry="15" fill="#0ea5e9" opacity="0.5"/>
  <text x="300" y="385" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">DEFECTIVE PUBLIC STANDPOST TAP EVIDENCE</text>
</svg>'''

svg_sewage = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f1f5f9"/>
  <rect y="220" width="600" height="180" fill="#3f3f46"/>
  <ellipse cx="300" cy="240" rx="75" ry="22" fill="#18181b" stroke="#71717a" stroke-width="4"/>
  <ellipse cx="300" cy="270" rx="160" ry="40" fill="#713f12" opacity="0.85"/>
  <ellipse cx="300" cy="275" rx="110" ry="25" fill="#451a03" opacity="0.9"/>
  <text x="300" y="375" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#fef08a" text-anchor="middle">SEWAGE &amp; CONTAMINATION HAZARD EVIDENCE</text>
</svg>'''

svg_meter = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f8fafc"/>
  <rect x="150" y="80" width="300" height="240" rx="15" fill="#0284c7" stroke="#0369a1" stroke-width="6"/>
  <circle cx="300" cy="200" r="80" fill="#ffffff" stroke="#334155" stroke-width="4"/>
  <circle cx="300" cy="200" r="65" fill="#f8fafc"/>
  <line x1="300" y1="200" x2="340" y2="160" stroke="#dc2626" stroke-width="4" stroke-linecap="round"/>
  <path d="M260,180 L290,210 L330,190" stroke="#38bdf8" stroke-width="3" fill="none"/>
  <path d="M310,185 C350,150 400,160 440,140" stroke="#0284c7" stroke-width="4" fill="none" stroke-dasharray="6,4"/>
  <text x="300" y="375" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">COMMERCIAL METER VALVE LEAKAGE EVIDENCE</text>
</svg>'''

mapping = {
    'main_burst.svg': svg_burst,
    'pipe_leak.svg': svg_pipe,
    'road_flood.svg': svg_flood,
    'tap_leak.svg': svg_tap,
    'sewage_contamination.svg': svg_sewage,
    'meter_leak.svg': svg_meter
}

for name, content in mapping.items():
    p1 = os.path.join('static', 'images', 'sample_leaks', name)
    p2 = os.path.join('static', 'uploads', name)
    with open(p1, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(p2, 'w', encoding='utf-8') as f:
        f.write(content)

print('Sample leak SVG images generated successfully.')
