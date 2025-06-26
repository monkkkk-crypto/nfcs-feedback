import json
import requests
from http import HTTPStatus
from collections import Counter

def handler(event, context):
    try:
        SUPABASE_URL = 'https://eswhkxwybtdbldpebzqc.supabase.co'
        SUPABASE_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzd2hreHd5YnRkYmxkcGVienFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5MTg2MTMsImV4cCI6MjA2NjQ5NDYxM30.X5qPz36vOmpK6m6u1mLnZ1Dv_ZgXYKWlvUP7tDUlR_s'
        headers = {
            'apikey': SUPABASE_API_KEY,
            'Authorization': f'Bearer {SUPABASE_API_KEY}',
        }
        response = requests.get(
            f'{SUPABASE_URL}/rest/v1/responses?select=*',
            headers=headers
        )
        if response.status_code != 200:
            return {
                'statusCode': response.status_code,
                'body': json.dumps({'error': response.text})
            }
        rows = response.json()
        if not rows:
            return {
                'statusCode': HTTPStatus.OK,
                'body': json.dumps({})
            }
        # Aggregate data
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
        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps(results)
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'error': str(e)})
        }