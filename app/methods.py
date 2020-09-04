from closeio_api import Client as CloseIO_API, APIError
import logging
import os

## Initiate Logger
log_format = "[%(asctime)s] %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

## Initiate Close API
api = CloseIO_API(os.environ.get('CLOSE_API_KEY'))

# Finds all notifications that can be marked as done using
# _find_notifications_to_be_marked_as_done and then makes sure the local_phone
# for that notification is a group number. If so, it sends each notification
# to be marked as done
def mark_notifications_as_done_for_lead(lead_id):
    notifications_to_be_marked = _find_notifications_to_be_marked_as_done(lead_id)
    if notifications_to_be_marked: 
        group_phones = _get_all_group_numbers()
        notifications_to_be_marked = [i for i in notifications_to_be_marked if i.get('local_phone') in group_phones]
        for noti in notifications_to_be_marked:
            _mark_notification_as_done(noti['id'])
    return None

# Marks a notification as done by setting is_complete to True
def _mark_notification_as_done(notification_id):
    try:
        api.put(f'task/{notification_id}', data={'is_complete': True })
    except APIError as e:
        logging.error(f'Failed to mark {notification_id} as done because {str(e)}')
    return None

# Finds all notifications on a lead that can be marked as done and are of a
# given type.
def _find_notifications_to_be_marked_as_done(lead_id):
    type_field = os.environ.get('TYPES_TO_MARK_AS_DONE')
    has_more = True
    offset = 0
    notifications = []
    while has_more:
        try:
            resp = api.get('task', params={ '_skip': offset, '_type__in': type_field, 'is_complete': False, 'lead_id': lead_id, '_fields': 'id,local_phone' })
        except Exception as e:
            logging.error(f'Failed to get task notifications on {lead_id} because {str(e)}')
            return []
        notifications += [i for i in resp['data']]
        offset += len(resp['data'])
        has_more = resp['has_more']
    return notifications
        
    
# Gets all group numbers for an organization and returns the actual numbers in a
# set for use in comparing the local_phone of a notification
def _get_all_group_numbers():
    has_more = True
    offset = 0
    group_numbers = set()
    while has_more:
        try:
            resp = api.get('phone_number', params={ '_fields': 'number', '_skip': offset, 'is_group_number': 'true' })
        except Exception as e:
            logging.error(f'Failed to get group numbers because {str(e)}')
            return group_numbers
        for num in resp['data']:
            group_numbers.add(num['number'])
        offset += len(resp['data'])
        has_more = resp['has_more']
    return group_numbers


