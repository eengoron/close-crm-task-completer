from flask import request
from app import app
import json
from .methods import mark_notifications_as_done_for_lead
import logging

## Initiate logger 
log_format = "[%(asctime)s] %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

@app.route('/', methods=['POST'])
def index():
    try:
        data = json.loads(request.data)
        event_data = data['event']
        if event_data['data'].get('lead_id'):
            lead_id = event['data']['lead_id']
            mark_notifications_as_done_for_lead(lead_id)
            return f"Processed Webhook for {lead_id}", 200
    except Exception as e:
        logging.error(f"Failed to process Webhook because {str(e)}...")
        return 'Failed to process Webhook', 400
    return "Webhook skipped because it was missing the criteria", 200