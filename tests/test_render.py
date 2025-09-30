from mailer.app.pdf_client import build_observation_html, render_pdf_bytes

def test_pdf_generation(tmp_path):
    sample = {"teacher_name": "Test", "obs_date": "2025-09-28"}
    html = build_observation_html(sample)
    pdf = render_pdf_bytes(html)
    out = tmp_path / "test.pdf"
    out.write_bytes(pdf)
    assert out.exists() and out.stat().st_size > 1000
