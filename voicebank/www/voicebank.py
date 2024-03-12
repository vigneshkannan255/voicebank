import frappe
from frappe import _
from frappe.utils import sanitize_html

def get_context(context):
    context.no_cache = 1
    if frappe.form_dict.query and frappe.form_dict.category:
        query = sanitize_html(frappe.form_dict.get('query'))
        category = sanitize_html(frappe.form_dict.get('category'))
        #context.title = _("Search Results for")
        context.query = query
        #context.route = "/voicebank"
        context.results = search(query, category, frappe.form_dict.get('scope'))
        context.update(context.results)
    else:
        context.title = _("Search")

@frappe.whitelist(allow_guest=True)
def search(query, category, scope=None):
    if category == "language":
        results = frappe.get_all("Voice Upload", filters={"language": ["like", f"%{query}%"]},
                                   fields=["first_name", "last_name"])
    elif category == "gender":
        results = frappe.get_all("Voice Upload", filters={"gender": query},
                                   fields=["first_name", "last_name", "profile_image", "voice", "language", "slang"])
    else:
        results = []
    return results
