# Close CRM Task Completer

A Flask app that marks tasks/notifications in Close CRM as done for a lead_id taken from a Close CRM webhook.

In its current iteration, we look for missed call notifications that were from group numbers on each lead and mark those as done when an email or sms is sent on that lead.

The way this works is:
 - An `activity.email.sent` or `activity.sms.sent` webhook is sent to this Flask App
 - We parse the lead_id from the webhook and try to find any incomplete missed call tasks for that lead
 - If an incomplete missed call task is found and the Close number that generated the task is a group number, we mark the task as done. 

 The type of task/notification we look for on the lead to mark as done is controlled by the environment variable `TYPES_TO_MARK_AS_DONE`.
 
 This app runs on the heroku instance in the Makespace organization.
