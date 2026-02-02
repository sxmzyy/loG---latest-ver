
import re
from datetime import datetime

line = "Row: 0 formatted_number=NULL, duration=53, subject=, is_call_log_phone_account_migration_pending=0, subscription_id=1, photo_id=0, post_dial_digits=, call_screening_app_name=NULL, priority=-1, number=+916382372387, countryiso=IN, photo_uri=NULL, geocoded_location=India, missed_reason=0, is_business_call=0, block_reason=0, subscription_component_name=com.android.phone/com.android.services.telephony.TelephonyConnectionService, add_for_all_users=1, numbertype=NULL, features=68, transcription=NULL, last_modified=1768411282836, _id=15045, new=1, date=1768411227699, name=BEN, type=1, presentation=1, via_number=, numberlabel=NULL, normalized_number=+916382372387, composer_photo_uri=NULL, phone_account_address=919344458459, phone_account_hidden=0, lookup_uri=NULL, voicemail_uri=NULL, matched_number=NULL, transcription_state=0, data_usage=NULL, location=NULL, asserted_display_name=NULL, call_screening_component_name=NULL, is_read=NULL"

number_match = re.search(r'number=([^,]+)', line)
name_match = re.search(r'name=([^,]+)', line)
duration_match = re.search(r'duration=([^,]+)', line)
type_match = re.search(r'type=([^,]+)', line)
date_match = re.search(r'date=(\d+)', line)
component_match = re.search(r'component_name=([^,]+)', line)

print(f"Number: {number_match.group(1) if number_match else 'None'}")
print(f"Name: {name_match.group(1) if name_match else 'None'}")
print(f"Type: {type_match.group(1) if type_match else 'None'}")
print(f"Component: {component_match.group(1) if component_match else 'None'}")

if name_match:
    print(f"Name Match Raw: {name_match.group(0)}")
