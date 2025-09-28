Endpoint contract (paste into your README)

POST /mail/observation

Auth: X-API-KEY: <shared secret>

Request JSON:

to_email (str, required)

teacher_name (str, required)

department_name (str, optional; printed on PDF)

obs_date (ISO str, required)

focus_area (str, optional)

strengths (str, optional)

weaknesses (str, optional)

comments (str, optional)

Response JSON: { "email_status": "queued" }
If immediate enqueue error (e.g., missing env/provider keys): { "email_status": "failed" }

Errors:

401 if X-API-KEY missing/invalid

422 for invalid JSON