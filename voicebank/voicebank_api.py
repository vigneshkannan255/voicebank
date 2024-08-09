import frappe
from frappe import _
from datetime import datetime, timedelta

@frappe.whitelist(allow_guest=True)
def voice_data(language=None, gender=None, slang=None, age=None):
    try:
        if not language and not gender and not slang and not age:
            return []

        query = """
        SELECT 
            `tabVoice Upload`.member_id, first_name, last_name, gender, category, language, artist_image, slang, voice
        FROM 
            `tabVoice Upload`
        JOIN 
            `tabArtist Profile` 
        ON 
            `tabVoice Upload`.member_id = `tabArtist Profile`.member_id
        WHERE 
            1=1
        """
        query_params = []

        if language:
            languages = language.split(',')
            query += " AND language IN ({})".format(','.join(['%s'] * len(languages)))
            query_params.extend(languages)

        if gender:
            genders = gender.split(',')
            query += " AND gender IN ({})".format(','.join(['%s'] * len(genders)))
            query_params.extend(genders)

        if slang:
            slangs = slang.split(',')
            query += " AND slang IN ({})".format(','.join(['%s'] * len(slangs)))
            query_params.extend(slangs)

        if age:
            age_list1 = age.split(",")
            age_list2 = age_list1[0].split("-")[0]  
            age_list3 = age_list1[-1].split("-")[1]  

            min_age = int(age_list2)
            max_age = int(age_list3)

            min_date = convert_age_to_dob(min_age)
            max_date = convert_age_to_dob(max_age)

            query += " AND date_of_birth BETWEEN %s AND %s"
            query_params.extend([max_date, min_date])
 
        voice_data = frappe.db.sql(query, query_params, as_dict=True)
        return voice_data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error fetching voice data"))
        frappe.throw(_("Error fetching voice data"))

def convert_age_to_dob(age):
    current_date = datetime.now()
    dob = current_date - timedelta(days=365.25 * age)
    return dob.date()
