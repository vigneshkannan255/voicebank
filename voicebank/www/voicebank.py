# about.py
import frappe

def get_context(context):
      context.data_list = frappe.db.sql(
        """
        SELECT first_name,last_name,age,gender,profile_image,voice,language,slang,category FROM `tabVoice Upload`
        """,as_dict=1,
      )
      return context
