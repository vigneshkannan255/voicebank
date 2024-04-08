import frappe
from frappe import _
from frappe.utils import sanitize_html
from datetime import datetime, timedelta
from string import Template 

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

    #
    # Update database with row
    #
    doc = frappe.get_doc({
    'doctype': 'Enquery Form',
    'name1': cust_name,
    'email_id': email_id,
    "phone_number": phone_number,
    "member_id_list": member_id_list
    })
    print (doc)
    doc.insert()

    #
    # Send email to customer
    # Here content generated based on template
    #

    mail_content_for_customer_1 = """
    Dear $cust_name,

    Thank you for reaching out. I'm glad to assist you with the contact details of the listed members. Please find the requested information below:

    """
    mail_content_for_customer_2 = """

    $num. $member_name
       - Email: $member_email_id
       - Phone: $member_phone_number
    """
    template_cust_2 = Template(mail_content_for_customer_2)

    mail_content_for_customer_3 = """

    If you require any further assistance or have additional questions, feel free to let me know.

    Best regards,
    [SICTADAU Admin]
    """

    mail_content_for_customer = ""
    mail_subject_for_customer = "Request for Contact Details of Listed Members"

    num = 1
    for member_id in member_id_list.split(","):

        print ("MEMEBR ID")
        print (member_id)
        artist_profile_filters = {
            "member_id": member_id
        }

        profile_list_results = frappe.get_list("Artist Profile", filters=artist_profile_filters,
                                   fields=["member_id", \
                                           "first_name", \
                                           "last_name", \
                                           "gender", \
                                           "date_of_birth", \
                                           "phone1", \
                                           "phone2", \
                                           "email", \
                                           "status", \
                                           "profile_image"])

        if profile_list_results:
            profile_list_result = profile_list_results[0]
            dict_cust_2 = { "num": str(num),
                            "member_name": "%s %s" %  (profile_list_result["first_name"], profile_list_result["last_name"]),
                            #"member_email_id": profile_list_result["email"],
                            "member_email_id": "xxxxx@yyy.com",
                            "member_phone_number": profile_list_result["phone1"]
                        }

            single_cust_details = template_cust_2.substitute(dict_cust_2)
            mail_content_for_customer = mail_content_for_customer + single_cust_details

            print ("mail_content_for_customer")
            print (mail_content_for_customer)

            num = num + 1


    frappe.sendmail(
            recipients = email_id,
            subject = mail_subject_for_customer,
            content = mail_content_for_customer,
            now = True
            )


    #
    # Send Email to admin
    #
    print ("member_id_list")
    print (member_id_list)
    if member_id_list:
        admin_email = "agevenkat@gmail.com"
        mail_template_for_admin = """

            Dear SICTADAU Admin,

            We're in need of the contact details of the listed members $member_id_list. Could you kindly provide us with their email addresses and phone numbers? Any additional information would be appreciated.
            Thank you for your assistance.

            Best regards,
            $cust_name
        """
        template_admin = Template(mail_template_for_admin)

        dict_admin_content = {
            "cust_name": cust_name,
            "member_id_list": member_id_list
        }
        mail_content_for_admin = template_admin.substitute(dict_admin_content)

        print (mail_content_for_admin)
        frappe.sendmail(
                recipients = admin_email,
                subject = mail_subject_for_customer,
                content = mail_content_for_admin,
                now = True
            )

    return { "results" : results }
