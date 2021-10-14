from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_storeadmin_verification_email(id,name,password,receiver):
    # Creating message subject and sender
    subject = 'Localshop Store Admin Verification'
    sender = 'localshop.com'

    #passing in the context vairables
    text_content = render_to_string('email/storeadmin_verification.txt',{"id":id,"name": name, "password":password})
    html_content = render_to_string('email/storeadmin_verification.html',{"id":id,"name": name,  "password":password})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()
    
def clerk_registration_email(id,name,password,receiver):
    # Creating message subject and sender
    subject = 'Localshop Clerk Registration'
    sender = 'localshop.com'

    #passing in the context vairables
    text_content = render_to_string('email/clerk_registration.txt',{"id":id,"name": name, "password":password})
    html_content = render_to_string('email/clerk_registration.html',{"id":id,"name": name,  "password":password})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()