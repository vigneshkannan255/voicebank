
# about.py
import markupsafe
from frappe.core.utils import html2text
from frappe.utils import sanitize_html
from frappe.utils.global_search import web_search
import frappe
from frappe import _

jenvs = {
    "methods":["search:voicebank.www.jinja.search"],
}

def get_context(context):
    context.no_cache = 1
    if frappe.form_dict.query and frappe.form_dict.category:
        query = str(markupsafe.escape(sanitize_html(frappe.form_dict.query)))
        category = str(markupsafe.escape(sanitize_html(frappe.form_dict.category)))
        context.route = "/searchvoice"
        context.title = _("SearchVoice results")
        context.query = query
        context.category = category
        out = search(query,category)
        #return out
	#context.update(out)
        #print(context)
        #context.update(frappe.utils.sanitize_html(frappe.form_dict.scope))
    else:
        context.title = _("SearchVoice")


@frappe.whitelist(allow_guest=True)
def search(query : str, scope: str | None = None, as_html: bool = False):
    out = frappe._dict()
    query = frappe.form_dict.get('query')
    category = frappe.form_dict.get('category')
    if category == "language":
        results = frappe.get_list("Voice Upload", filters={"language": ["like", f"%{query}%"]}, fields=["first_name","last_name","profile_image","voice","language","slang"])
    elif category == "gender":
        results = frappe.get_list("Voice Upload", filters={"gender": query}, fields=["first_name","last_name","profile_image","voice","language","slang"])
    out.results = results
    #elif as_html:
    return frappe.render_template("voicebank/templates/includes/search_result.html", out)
    #return out
