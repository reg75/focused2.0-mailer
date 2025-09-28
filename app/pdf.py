from html import escape
from weasyprint import HTML

A4_CSS = """@page { size: A4; margin: 18mm; }
body {font-family: Calibri, Arial, sans-serif; font-size: 12pt; }
h1 { margin: 0 0 8px 0; }
table { width: 100%; border-collapse: collapse; margin-top: 12px; }
th, td { border: 1px solid #999; padding: 6px; vertical-align: top; }
.muted { color:#555; } .pre {white-space: pre-wrap; }
"""
def build_observation_html(d: dict) -> str:
    # escape all user-provided text to avoid HTML injection
    e = {k: escape(str(d.get(k,"") or "")) for k in d.keys()}
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{A4_CSS}</style></head><body>
<h1>FocusEd Lesson Observation</h1>
<p class="muted">{e.get('obs_date','')} • {e.get('department_name','') or '—'}</p>
<h2>{e.get('teacher_name','')}</h2>
<table>
<tr><th>Class</th><td>{e.get('class_name','') or '—'}</td></tr>
<tr><th>Focus Area</th><td>{e.get('focus_area','') or '—'}</td></tr>
<tr><th>Strengths</th><td class="pre">{e.get('strengths','') or '—'}</td></tr>
<tr><th>Areas for Development</th><td class="pre">{e.get('weaknesses','') or '—'}</td></tr>
<tr><th>Other Comments</th><td class="pre">{e.get('comments','') or '—'}</td></tr>
</table></body></html>"""

def render_pdf_bytes(html_str: str) -> bytes:
    return HTML(string=html_str).write_pdf()