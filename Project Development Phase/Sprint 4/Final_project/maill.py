import smtplib 
import ssl
server = smtplib.SMTP_SSL('smtp.mail.yahoo.com',port=465)
server.login("nikhisri@yahoo.com","Nk100262")
server.sendmail("nikhisri@yahoo.com", "nikhisrinivas261@gmail.com", "reorder")
server.quit()