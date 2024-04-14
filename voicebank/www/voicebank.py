import frappe
from frappe import _
from frappe.utils import sanitize_html
from datetime import datetime, timedelta

def search_users_by_age(age):
    # default min and max age
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
    #print ("dob.date():", dob.date())
    return dob.date()

def get_context(context):
    context.no_cache = 1
    if frappe.form_dict.language or frappe.form_dict.gender or frappe.form_dict.age or frappe.form_dict.slang:
        language = sanitize_html(frappe.form_dict.get('language'))
        gender = sanitize_html(frappe.form_dict.get('gender'))
        age = sanitize_html(frappe.form_dict.get('age'))
        slang = sanitize_html(frappe.form_dict.get('slang'))
        #context.title = _("Search Results for")
        #context.query = query
        #context.route = "/voicebank"
        context.results = search(language, gender, slang, age, frappe.form_dict.get('scope'))
        context.update(context.results)
    else:
        context.title = _("Search")

@frappe.whitelist(allow_guest=True)
def search(language, gender, slang, age, scope=None):

    date_range = search_users_by_age(age)
    #print ( "date_range:", date_range )

    voice_bank_filters_org = {
        "language": language,
        "slang": slang
    }

    artist_profile_filters_org = {
        "gender": gender,
        "date_of_birth": date_range
    }

    #print ("Original Value from Search filter")
    #print ( "voice_bank_filters_org: ", voice_bank_filters_org)
    #print ( "artist_profile_filters_org: ",  artist_profile_filters_org)

    voice_bank_filters = { k: v for k, v in voice_bank_filters_org.items() if v }
    artist_profile_filters = { k: v for k, v in artist_profile_filters_org.items() if v }
    #print ("Pre-processed filter value, which is removing empty fields")
    #print ( "voice_bank_filters: ", voice_bank_filters)
    #print ( "artist_profile_filters: ", artist_profile_filters)

    voice_list_results = frappe.get_list("Voice Upload", filters=voice_bank_filters,
                                       fields=["member_id", \
                                               "language", \
                                               "slang", \
                                               "voice", \
                                               "voice_image", \
                                               "timestamp", \
                                               "category"])
    
    profile_list_results = frappe.get_list("Artist Profile", filters=artist_profile_filters,
                                   fields=["member_id", \
                                           "first_name", \
                                           "last_name", \
                                           "gender", \
                                           "date_of_birth", \
                                           "phone1", \
                                           "phone2", \
                                           "email", \
                                           "status", \
                                           "profile_image"])

    #print ("Search Results:")
    #print ("voice_list_results", voice_list_results)
    #print ("profile_list_results", profile_list_results)

    results = []
    if not voice_list_results or not profile_list_results:
        #print ("Eaither Profile list or voice list search list are empty")
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
