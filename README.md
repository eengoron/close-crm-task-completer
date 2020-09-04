# Close CRM Task Completer

A Flask app that marks tasks in Close as done for a lead_id taken from a webhook.

In its current iteration, we look for missed call notifications that were from group numbers
and mark those as done when an email or sms is sent on that lead.
