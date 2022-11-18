# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 17:32:19 2022

@author: Bhuvaneswari
"""

import smtplib 
import ssl
try: 
    #Create your SMTP session 
    print(ssl.OPENSSL_VERSION)
    smtp = smtplib.SMTP_SSL("smtp.mail.yahoo.com",587) 

   #Use TLS to add security 
    #smtp.starttls() 

    #User Authentication 
    smtp.login("nikhisri@yahoo.com","fdhgp")

    #Defining The Message 
    message = "Stock below 4 needs to be reordered" 

    #Sending the Email
    smtp.sendmail("nikhisri@yahoo.com", "nikhisrinivas261@gmail.com",message) 

    #Terminating the session 
    smtp.quit() 
    print ("Email sent successfully!") 

except Exception as ex: 
    print("Something went wrong....",ex)