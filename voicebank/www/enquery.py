import frappe
from frappe import _
from frappe.utils import sanitize_html
from datetime import datetime, timedelta

def get_context(context):
    context.no_cache = 1
    if frappe.form_dict.member_id_list:
        name = sanitize_html(frappe.form_dict.get('name'))
        email_id = sanitize_html(frappe.form_dict.get('email_id'))
        phone_number = sanitize_html(frappe.form_dict.get('phone_number'))
        member_id_list = sanitize_html(frappe.form_dict.get('member_id_list'))
        context.results = search(name, email_id, phone_number, member_id_list)
        context.update(context.results)
    else:
        context.title = _("Search")

@frappe.whitelist(allow_guest=True)
def search(name, email_id, phone_number, member_id_list):

    emquery_filters_org = {
        "name": name,
        "email_id": email_id,
        "phone_number": phone_number,
        "member_id_list": member_id_list
    }

    
    results = {}
    print ("Original Value of filter")
    print ( "voice_bank_filters_org: ", emquery_filters_org)


    return { "results" : results }
