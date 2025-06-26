import json
import requests
from http import HTTPStatus

def handler(event, context):
    try:
        body = json.loads(event['body'])
        SUPABASE_URL = 'https://eswhkxwybtdbldpebzqc.supabase.co'
        SUPABASE_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzd2hreHd5YnRkYmxkcGVienFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5MTg2MTMsImV4cCI6MjA2NjQ5NDYxM30.X5qPz36vOmpK6m6u1mLnZ1Dv_ZgXYKWlvUP7tDUlR_s'
        headers = {
            'apikey': SUPABASE_API_KEY,
            'Authorization': f'Bearer {SUPABASE_API_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        # Prepare data for Supabase
        data = {
            'level': body.get('level'),
            'department': body.get('department'),
            'gender': body.get('gender'),
            'residence': body.get('residence'),
            'attendance': body.get('attendance'),
            'reason': ','.join(body.get('reason', [])),
            'vision': body.get('vision'),
            'fecamds': body.get('fecamds'),
            'academic': body.get('academic'),
            'connection': body.get('connection'),
            'sports': body.get('sports'),
            'social': body.get('social'),
            'spiritual': body.get('spiritual'),
            'male_barrier': body.get('male_barrier'),
            'male_solution': body.get('male_solution'),
            'best_day': body.get('best_day'),
            'duration': body.get('duration'),
            'venue': body.get('venue'),
            'transport': int(body.get('transport')) if body.get('transport') is not None else None,
            'communication': body.get('communication'),
            'role': body.get('role'),
            'leadership': body.get('leadership'),
            'alumni': body.get('alumni'),
            'idea': body.get('idea'),
            'thoughts': body.get('thoughts')
        }
        response = requests.post(
            f'{SUPABASE_URL}/rest/v1/responses',
            headers=headers,
            data=json.dumps(data)
        )
        if response.status_code in (200, 201):
            return {
                'statusCode': HTTPStatus.OK,
                'body': json.dumps({'message': 'Response saved successfully'})
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps({'error': response.text})
            }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'error': str(e)})
        }