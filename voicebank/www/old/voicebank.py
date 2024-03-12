# about.py
import frappe
from frappe import _
import sys
#from .jinja import search

def get_context(context):
      context.data_list = frappe.db.sql(
        """
        SELECT first_name,last_name,age,gender,profile_image,voice,language,slang,category FROM `tabVoice Upload`
        """,as_dict=1,
      )
      #query = search()
      #context.update(query, frappe.utils.sanitize_html(frappe.form_dict.scope))
      return context


@frappe.whitelist(allow_guest=True)
def search(query,category):
    out = frappe._dict()
    query = frappe.form_dict.get('query')
    category = frappe.form_dict.get('category')
    if category == "language":
        results = frappe.get_list("Voice Upload", filters={"language": ["like", f"%{query}%"]}, fields=["first_name","last_name","profile_image","voice","language","slang"])
    elif category == "gender":
        results = frappe.get_list("Voice Upload", filters={"gender": query}, fields=["first_name","last_name","profile_image","voice","language","slang"])
    #elif as_html:
    #return frappe.render_template("voicebank/templates/includes/search_result.html", out)
    #return out
    out.results = results
    return "results"
