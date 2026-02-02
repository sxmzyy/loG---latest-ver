import re

log_content = """
Row: 0 formatted_number=NULL, duration=53, subject=, is_call_log_phone_account_migration_pending=0, subscription_id=1, photo_id=0, post_dial_digits=, call_screening_app_name=NULL, priority=-1, number=+916382372387, countryiso=IN, photo_uri=NULL, geocoded_location=India, missed_reason=0, is_business_call=0, block_reason=0, subscription_component_name=com.android.phone/com.android.services.telephony.TelephonyConnectionService, add_for_all_users=1, numbertype=NULL, features=68, transcription=NULL, last_modified=1768411282836, _id=15045, new=1, date=1768411227699, name=BEN, type=1, presentation=1, via_number=, numberlabel=NULL, normalized_number=+916382372387, composer_photo_uri=NULL, phone_account_address=919344458459, phone_account_hidden=0, lookup_uri=NULL, voicemail_uri=NULL, matched_number=NULL, transcription_state=0, data_usage=NULL, location=NULL, asserted_display_name=NULL, call_screening_component_name=NULL, is_read=NULL
Row: 4 formatted_number=NULL, duration=0, subject=, is_call_log_phone_account_migration_pending=0, subscription_id=1, photo_id=0, post_dial_digits=, call_screening_app_name=NULL, priority=-1, number=+917092222575, countryiso=IN, photo_uri=NULL, geocoded_location=India, missed_reason=589824, is_business_call=0, block_reason=0, subscription_component_name=com.android.phone/com.android.services.telephony.TelephonyConnectionService, add_for_all_users=1, numbertype=NULL, features=68, transcription=NULL, last_modified=1768453597050, _id=15049, new=0, date=1768443413263, name=BENNY, type=3, presentation=1, via_number=, numberlabel=NULL, normalized_number=+917092222575, composer_photo_uri=NULL, phone_account_address=919344458459, phone_account_hidden=0, lookup_uri=NULL, voicemail_uri=NULL, matched_number=NULL, transcription_state=0, data_usage=NULL, location=NULL, asserted_display_name=NULL, call_screening_component_name=NULL, is_read=1
Row: 5 formatted_number=NULL, duration=16, subject=, is_call_log_phone_account_migration_pending=0, subscription_id=1, photo_id=0, post_dial_digits=, call_screening_app_name=NULL, priority=-1, number=+919952408001, countryiso=IN, photo_uri=NULL, geocoded_location=India, missed_reason=0, is_business_call=0, block_reason=0, subscription_component_name=com.android.phone/com.android.services.telephony.TelephonyConnectionService, add_for_all_users=1, numbertype=NULL, features=68, transcription=NULL, last_modified=1768454206105, _id=15050, new=1, date=1768454179865, name=Annie, type=1, presentation=1, via_number=, numberlabel=NULL, normalized_number=+919952408001, composer_photo_uri=NULL, phone_account_address=919344458459, phone_account_hidden=0, lookup_uri=NULL, voicemail_uri=NULL, matched_number=NULL, transcription_state=0, data_usage=NULL, location=NULL, asserted_display_name=NULL, call_screening_component_name=NULL, is_read=NULL
"""

contact_map = {}

lines = log_content.strip().split('\n')
for line in lines:
    # Use STRICT matches for number and name independently to avoid false positives
    # \b ensures word boundary (e.g. avoids 'formatted_number' or 'app_name')
    m_num = re.search(r'\bnumber=([^,]+)', line)
    m_name = re.search(r'\bname=([^,]+)', line)
    
    if m_num and m_name:
        num = m_num.group(1).strip()
        name = m_name.group(1).strip()
        print(f"Found: {num} -> {name}")
        if name != 'NULL' and name != '':
            contact_map[num] = name

print("\nFinal Map:")
print(contact_map)
