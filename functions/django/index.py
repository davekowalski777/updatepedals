from guitar_pedals.wsgi import application
import awsgi
import json
import os
import sys

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def handler(event, context):
    print('Current directory:', os.getcwd())
    print('Directory contents:', os.listdir('.'))
    print('Incoming event:', json.dumps(event))
    
    path = event.get('path', '/')
    if path.startswith('/.netlify/functions/django'):
        path = path[len('/.netlify/functions/django'):]
    if not path:
        path = '/'
    
    event['path'] = path
    
    if 'headers' not in event:
        event['headers'] = {}
    
    event['headers'].update({
        'host': 'netlify.app',
        'x-forwarded-proto': 'https',
        'x-forwarded-port': '443'
    })
    
    try:
        return awsgi.response(application, event, context)
    except Exception as e:
        print('Error:', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'path': path})
        }
