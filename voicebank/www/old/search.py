# about.py
import frappe
from frappe import _

jenvs = {
    "methods":["search:voicebank.www.jinja.search"],
}

@frappe.whitelist(allow_guest=True)
def search(query,category):
    query = frappe.form_dict.get('query')
    category = frappe.form_dict.get('category')
    if category == "language":
#        results.data_list = frappe.db.sql("""SELECT first_name,last_name,age,gender,profile_image,voice,language,slang,category FROM `tabVoice Upload` WHERE language = `Tamil` """,as_dict=1,)
        results = frappe.get_list("Voice Upload", filters={"language": ["like", f"%{query}%"]}, fields=["first_name","last_name","profile_image","voice","language","slang"])
    elif category == "gender":
        results = frappe.get_list("Voice Upload", filters={"gender": query}, fields=["first_name","last_name","profile_image","voice","language","slang"])
    return frappe.render_template("voicebank/www/search.html",{"results" : results})
#    return json.dump(results)
#    frappe.msgprint(results)
#    return results

#def get_context(context):
#    return context
