import frappe
from frappe import _
from frappe.utils import sanitize_html
from datetime import datetime, timedelta
from collections import defaultdict

frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("voice_bank", allow_site=True, file_count=50)

def search_users_by_age(age):
    # Assign default values
    min_age = 0
    max_age = 0
    
    # Cases to set min_age and max_age
    if age == "r1":
        min_age = 5
        max_age = 10
    elif age == "r2":
        min_age = 10
        max_age = 15
    elif age == "r3":
        min_age = 15
        max_age = 20
    elif age == "r4":
        min_age = 20
        max_age = 25
    elif age == "r5":
        min_age = 25
        max_age = 30
    elif age == "r6":
        min_age = 30
        max_age = 35
    elif age == "r7":
        min_age = 35
        max_age = 40
    elif age == "r8":
        min_age = 40
        max_age = 45
    elif age == "r9":
        min_age = 45
        max_age = 50

    date_range = ""
    if age:
        min_date = convert_age_to_dob(min_age)
        max_date = convert_age_to_dob(max_age)
        # Convert datetime object to string of (YY-MM-DD) format
        min_date = min_date.strftime('%Y-%m-%d')
        max_date = max_date.strftime('%Y-%m-%d')
    
        # Example for date range ['2020-04-01', '2021-03-31']
        date_range = ['between', [max_date, min_date]]

    return date_range

# Function to search users by age
def convert_age_to_dob(age):
    current_date = datetime.now()
    dob = current_date - timedelta(days=365.25 * age)
    logger.info(f"VoiceBank: dob.date(): {dob.date()}")
    return dob.date()

def get_context(context):
    context.no_cache = 1
    if frappe.form_dict.language or frappe.form_dict.gender or frappe.form_dict.age or frappe.form_dict.slang:
        language = sanitize_html(frappe.form_dict.get('language')) or ""
        gender = sanitize_html(frappe.form_dict.get('gender')) or ""
        age = sanitize_html(frappe.form_dict.get('age')) or ""
        slang = sanitize_html(frappe.form_dict.get('slang')) or ""
        context.results = search(language, gender, slang, age, frappe.form_dict.get('scope'))
        context.update(context.results)
    else:
        context.title = _("Search")

@frappe.whitelist(allow_guest=True)
def search(language, gender, slang, age, scope=None):  # Added scope parameter with default None
    date_range = search_users_by_age(age)
    logger.info(f"VoiceBank: date_range {date_range}")

    voice_bank_filters_org = {
        "language": language,
        "slang": slang
    }

    artist_profile_filters_org = {
        "gender": gender,
        "date_of_birth": date_range
    }

    logger.info(f"VoiceBank: Original Value from Search filter")
    logger.info(f"VoiceBank: voice_bank_filters_org: {voice_bank_filters_org}")
    logger.info(f"VoiceBank: artist_profile_filters_org: {artist_profile_filters_org}")

    voice_bank_filters = { k: v for k, v in voice_bank_filters_org.items() if v }
    if language and "," in language:
        lang_list = language.split(",")
        voice_bank_filters['language'] = ['in', lang_list]

    artist_profile_filters = { k: v for k, v in artist_profile_filters_org.items() if v }
    logger.info(f"VoiceBank: Pre-processed filter value, which is removing empty fields")
    logger.info(f"VoiceBank: voice_bank_filters: {voice_bank_filters}")
    logger.info(f"VoiceBank: artist_profile_filters: {artist_profile_filters}")

    voice_list_results_all = frappe.get_list("Voice Upload", filters=voice_bank_filters,
                                    fields=["member_id", \
                                               "language", \
                                               "slang", \
                                               "voice", \
                                               "voice_image", \
                                               "timestamp", \
                                               "category"])
    
    if language and "," in language:
        # Create a dictionary to store data for each member_id
        member_data = defaultdict(list)

        # Group data by member_id
        for item in voice_list_results_all:
            member_data[item['member_id']].append(item)

        # Retain complete dict data for each member_id with different languages
        voice_list_results = []
        for member_id, data_list in member_data.items():
            languages = set()
            for item in data_list:
                languages.add(item['language'])
            if len(data_list) > 1 and len(languages) > 1:
                voice_list_results.extend(data_list)

        logger.info(f"VoiceBank: updated list : {voice_list_results}")
    else:
        voice_list_results = voice_list_results_all

    profile_list_results = frappe.get_list("Artist Profile", filters=artist_profile_filters,
                                   fields=["member_id", \
                                           "first_name", \
                                           "last_name", \
                                           "gender", \
                                           "date_of_birth", \
                                           "phone1", \
                                           "phone2", \
                                           "email_id", \
                                           "status", \
                                           "profile_image"])

    logger.info(f"VoiceBank: Search Results:")
    logger.info(f"VoiceBank: voice_list_results {voice_list_results}")
    #logger.info(f"VoiceBank: profile_list_results {profile_list_results}")

    results = []
    if not voice_list_results or not profile_list_results:
        logger.info(f"VoiceBank: Either Profile list or voice list search list are empty")
        results = []
    else:
        for profile in profile_list_results:
            for voice in voice_list_results:
                result = {}
                if profile['member_id'] == voice['member_id']:
                    result['member_id']   = profile['member_id']
                    result['first_name']  = profile['first_name']
                    result['last_name']   = profile['last_name']
                    result['age']         = "0"
                    result['gender']      = profile['gender']
                    result['language']    = voice['language']
                    result['slang']       = voice['slang']
                    result['voice_image'] = voice['voice_image']
                    result['voice']       = voice['voice']
                    result['category']    = voice['category']
                    results.append(result)

    return { "results" : results }
