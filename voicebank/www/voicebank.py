import frappe
from frappe import _
from frappe.utils import sanitize_html

def get_context(context):
    context.no_cache = 1
    if frappe.form_dict.language and frappe.form_dict.gender:
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
    filters = {
    "language": language,
    "gender": gender,
    "age":['<', max_age]
    }
    results = frappe.get_list("Voice Upload", filters=filters,
                                   fields=["first_name","last_name","profile_image", "voice", "language", "slang","gender","category"])
    return {"results" : results}
