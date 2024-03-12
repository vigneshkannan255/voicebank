# about.py
import frappe
from frappe import _
import sys
import markupsafe
from frappe.utils import sanitize_html

def get_context(context):
    context.no_cache = 1
    if frappe.form_dict.query and frappe.form_dict.category:
        query = str(markupsafe.escape(sanitize_html(frappe.form_dict.query)))
        category = str(markupsafe.escape(sanitize_html(frappe.form_dict.category)))
        context.title = _("Search Results for")
        context.query = query
        context.route = "/search"
        context.update(search(query,category,frappe.utils.sanitize_html(frappe.form_dict.scope)))
    else:
        context.title = _("Search")
      #query = search()
      #context.update(query, frappe.utils.sanitize_html(frappe.form_dict.scope))
      #return context


@frappe.whitelist(allow_guest=True)
def search(query,category,scope: dict | None = None):
    query = frappe.form_dict.get('query')
    category = frappe.form_dict.get('category')
    if category == "language":
        results = frappe.get_list("Voice Upload", filters={"language": ["like", f"%{query}%"]}, fields=["first_name","last_name","profile_image","voice","language","slang"])
    elif category == "gender":
        results = frappe.get_list("Voice Upload", filters={"gender": query}, fields=["first_name","last_name","profile_image","voice","language","slang"])
    #elif as_html:
    #return frappe.render_template("voicebank/templates/includes/search_result.html", out)
    #return out
    return results
