from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from collections import Counter
import os

SUPABASE_URL = 'https://eswhkxwybtdbldpebzqc.supabase.co'
SUPABASE_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzd2hreHd5YnRkYmxkcGVienFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5MTg2MTMsImV4cCI6MjA2NjQ5NDYxM30.X5qPz36vOmpK6m6u1mLnZ1Dv_ZgXYKWlvUP7tDUlR_s'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SurveyResponse(BaseModel):
    level: str = None
    department: str = None
    gender: str = None
    residence: str = None
    attendance: str = None
    reason: list = []
    vision: str = None
    fecamds: str = None
    academic: str = None
    connection: str = None
    sports: str = None
    social: str = None
    spiritual: str = None
    male_barrier: str = None
    male_solution: str = None
    best_day: str = None
    duration: str = None
    venue: str = None
    transport: int = None
    communication: str = None
    role: str = None
    leadership: str = None
    alumni: str = None
    idea: str = None
    thoughts: str = None

@app.post("/submit")
async def submit_survey(response: SurveyResponse):
    headers = {
        'apikey': SUPABASE_API_KEY,
        'Authorization': f'Bearer {SUPABASE_API_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    data = response.dict()
    data['reason'] = ','.join(data.get('reason', []))
    r = requests.post(
        f'{SUPABASE_URL}/rest/v1/responses',
        headers=headers,
        json=data
    )
    if r.status_code in (200, 201):
        return {"message": "Response saved successfully"}
    else:
        return {"error": r.text}

@app.get("/results")
async def get_results():
    headers = {
        'apikey': SUPABASE_API_KEY,
        'Authorization': f'Bearer {SUPABASE_API_KEY}',
    }
    r = requests.get(f'{SUPABASE_URL}/rest/v1/responses?select=*', headers=headers)
    if r.status_code != 200:
        return {"error": r.text}
    rows = r.json()
    if not rows:
        return {}
    results = {}
    columns = rows[0].keys()
    for col in columns:
        if col != 'id':
            values = [row[col] for row in rows if row.get(col)]
            if col == 'reason':
                values = [item for sublist in [v.split(',') for v in values] for item in sublist]
            if col == 'idea' or col == 'thoughts':
                results[col] = values
            else:
                results[col] = dict(Counter(values))
    return results 