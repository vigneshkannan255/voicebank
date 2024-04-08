import frappe
from frappe import _
from frappe.utils import sanitize_html
from datetime import datetime, timedelta

def get_context(context):
    context.no_cache = 1
    if frappe.form_dict.member_id_list:
        cust_name = sanitize_html(frappe.form_dict.get('cust_name'))
        email_id = sanitize_html(frappe.form_dict.get('email_id'))
        phone_number = sanitize_html(frappe.form_dict.get('phone_number'))
        member_id_list = sanitize_html(frappe.form_dict.get('member_id_list'))
        context.results = search(cust_name, email_id, phone_number, member_id_list)
        context.update(context.results)
    else:
        context.title = _("Search")

@frappe.whitelist(allow_guest=True)
def search(cust_name, email_id, phone_number, member_id_list):

    emquery_filters_org = {
        "cust_name": cust_name,
        "email_id": email_id,
        "phone_number": phone_number,
        "member_id_list": member_id_list
    }

    
    results = {}
    print ("Original Value of filter")
    print ( "enquery_form_org: ", emquery_filters_org)

    voice_list_results = frappe.get_list("Enquery Form", fields=["name1"]) 
    print (voice_list_results)

    doc = frappe.get_doc({
    'doctype': 'Enquery Form',
    'name1': cust_name,
    'email_id': email_id,
    "phone_number": phone_number,
    "member_id_list": member_id_list
    })
    print (doc)
    doc.insert()
    frappe.sendmail(recipients = 'ethirajit@gmail.com',subject = 'test mail',content = 'test mail',now = True)
    return { "results" : results }
