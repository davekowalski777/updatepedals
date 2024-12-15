from guitar_pedals.wsgi import application
import awsgi
import json

def handler(event, context):
    # Debug logging
    print('Incoming event:', json.dumps(event))
    
    # Get the path and query string
    path = event.get('path', '/')
    query = event.get('queryStringParameters', {})
    
    # Clean up the path
    if path.startswith('/.netlify/functions/django'):
        path = path[len('/.netlify/functions/django'):]
    if not path:
        path = '/'
    
    # Ensure path starts with /
    if not path.startswith('/'):
        path = '/' + path
    
    # Update the event
    event['path'] = path
    event['queryStringParameters'] = query
    
    # Ensure headers exist
    if 'headers' not in event:
        event['headers'] = {}
    
    # Add required headers
    event['headers'].update({
        'host': 'netlify.app',
        'x-forwarded-proto': 'https',
        'x-forwarded-port': '443'
    })
    
    print(f'Processing path: {path} with query: {query}')
    
    try:
        response = awsgi.response(application, event, context)
        print('Response:', response)
        return response
    except Exception as e:
        print('Error:', str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e),
                'path': path,
                'query': query
            })
        }
