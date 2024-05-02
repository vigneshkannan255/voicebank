import frappe
from frappe import _
from frappe.utils import sanitize_html
from datetime import datetime, timedelta
from string import Template 
import time
import csv
import os

frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("voice_bank", allow_site=True, file_count=50)

def get_context(context):
    context.no_cache = 1
    if frappe.form_dict.member_id_list:
        cust_name = sanitize_html(frappe.form_dict.get('cust_name'))
        email_id = sanitize_html(frappe.form_dict.get('email_id'))
        phone_number = sanitize_html(frappe.form_dict.get('phone_number'))
        member_id_list = sanitize_html(frappe.form_dict.get('artist_member_id_list'))
        context.results = search(cust_name, email_id, phone_number, member_id_list)
        context.update(context.results)
    else:
        context.title = _("Search")

def update_artist_profile():
    
    www_path = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(www_path, 'test_1234.csv')

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            logger.info(f"Enquery: {row}")
            # format = DD-MM-YYYY
            dob = row["date_of_birth"].split("-")
            datetime_object = datetime(int(dob[2]), int(dob[1]), int(dob[0]))
            artist = frappe.get_doc({
                "doctype": "Artist Profile",
                "member_id": row["member_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "gender": row["gender"],
                "date_of_birth": datetime_object.strftime('%Y-%m-%d'),
                "phone1": row["phone1"],
                "phone2": row["phone2"],
                "email_id": row["email"],
                "status": row["status"],
                "profile_image": row["profile_image"],
            })

            artist.insert()
            logger.info(f"Enquery: {artist}")
            time.sleep(1)

@frappe.whitelist(allow_guest=True)
def search(cust_name, email_id, phone_number, member_id_list):

    emquery_filters_org = {
        "cust_name": cust_name,
        "email_id": email_id,
        "phone_number": phone_number,
        "member_id_list": member_id_list
    }

    
    results = {}
    logger.info(f"Enquery: Original Value of filter")
    logger.info(f"Enquery: enquery_form_org: {emquery_filters_org}")

    voice_list_results = frappe.get_list("Enquery Form", fields=["name1"]) 
    logger.info(f"Enquery: {voice_list_results}")

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
    logger.info(f"Enquery: {doc}")
    doc.insert()
    time.sleep(1)

    #update_artist_profile()

    #
    # Send email to Admin
    # Here content generated based on template
    #

    mail_template_for_admin = """

        Dear SICTADAU Admin,<br>

        We're in need of the contact details of the listed members $member_id_list.<br>
        Could you kindly provide us with their email addresses and phone numbers?<br>
        Any additional information would be appreciated.<br>
        Thank you for your assistance.<br>

        Best regards, <br>
        Name: $cust_name <br>
        Email ID: $email_id <by>
        Phone: $phone <br>
        """
    template_admin = Template(mail_template_for_admin)

    dict_admin_content = {
            "cust_name": cust_name,
            "email_id": email_id,
            "phone": phone_number,
            "member_id_list": member_id_list
        }
    mail_content_for_admin = template_admin.substitute(dict_admin_content)

    mail_content_for_admin_1 = """
    Note: This message has to be farwared to requester<br>
    =========================<br>
    Dear $cust_name,<br> 

        &nbsp;&nbsp;&nbsp;&nbsp;Thank you for reaching out. I'm glad to assist you with the contact details of the listed members. Please find the requested information below:<br>

    """
    template_admin_1 = Template(mail_content_for_admin_1)
    dict_admin_content_1 = {
            "cust_name": cust_name
        }
    mail_content_for_admin_1 = template_admin_1.substitute(dict_admin_content_1)
   
    mail_content_for_admin_2 = """
    <br>
    $num. $member_name<br> 
       &nbsp;&nbsp;- Email: $member_email_id<br> 
       &nbsp;&nbsp;- Phone: $member_phone_number<br>
    """
    template_admin_2 = Template(mail_content_for_admin_2)

    mail_content_for_admin_3 = """
    <br>
    If you require any further assistance or have additional questions, feel free to let me know.<br> 

    Best regards,<br> 
    [SICTADAU Admin]<br>
    =========================<br>
    """

    num = 1
    mail_content_for_admin_2 = ""
    for member_id in member_id_list.split(","):

        logger.info(f"Enquery: MEMEBR ID: {member_id}")
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
                                           "email_id", \
                                           "status", \
                                           "profile_image"])

        if profile_list_results:
            profile_list_result = profile_list_results[0]
            dict_cust_2 = { "num": str(num),
                            "member_name": "%s %s" %  (profile_list_result["first_name"], profile_list_result["last_name"]),
                            "member_email_id": profile_list_result["email_id"],
                            #"member_email_id": "xxxxx@yyy.com",
                            "member_phone_number": profile_list_result["phone1"]
                        }

            single_cust_details = template_admin_2.substitute(dict_cust_2)
            mail_content_for_admin_2 = mail_content_for_admin_2 + single_cust_details

            num = num + 1

    #
    # Send Email to admin
    #
    logger.info(f"Enquery: member_id_list: {member_id_list}")

    mail_content_for_admin = mail_content_for_admin + mail_content_for_admin_1 + mail_content_for_admin_2 + mail_content_for_admin_3
    logger.info(f"Enquery: mail_content_for_admin: {mail_content_for_admin}")
    mail_subject_for_customer = "Request for Contact Details of Listed Members"

    if member_id_list:
        #Send mail to Admin
        admin_email = "agevenkat@gmail.com"
        frappe.sendmail(
            recipients = admin_email,
            subject = mail_subject_for_customer,
            content = mail_content_for_admin,
            now = True
            )

        #
        # Send mail to customer
        #
        mail_template_for_customer = """

            Dear $cust_name,<br> 

            Thank you for reaching out SICTADAU, We will send you the requested voice artist profile as soon as possible.<br>

            Best regards,<br>
            [SICTADAU Admin]<br>
        """
        template_cust = Template(mail_template_for_customer)

        dict_cust_content = {
            "cust_name": cust_name
        }
        mail_content_for_cust = template_cust.substitute(dict_cust_content)

        logger.info(f"Enquery: mail_content_for_cust: {mail_content_for_cust}")
        frappe.sendmail(
                recipients = email_id,
                subject = mail_subject_for_customer,
                content = mail_content_for_cust,
                now = True
            )

    return { "results" : results }
