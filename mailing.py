import smtplib

email_text = """  
To: %s  
Subject: %s
Content-type: text/html


<div style="font-family: Helvetica, Arial, sans-serif;padding:15px;padding-bottom:margin:0;">
	<center>
		<div style="max-width:400px;border: 1px solid rgba(100,100,100,0.7);border-radius:10px;padding:20px 35px 15px 35px;">
			
	        <h1 style="text-align:left;color:black;word-wrap:break-word;margin-bottom:30px;">Hey %s,</h1>

	        <p style="font-size:20px;margin:0;color:rgba(0,0,0,0.6);text-align:center;">
	          Welcome to the RIICC site!</p>
	        
	        <img alt="Club_logo" src="https://drive.google.com/uc?export=view&id=1zr8Vbnv7camsZNik_D_g3dh2WK2waobE" style="margin-top:25px;margin-bottom:10px;width:250px;">
	        

	        <p style="text-align:center;display:block;margin-bottom:35px;font-size:17px;color:rgba(0,0,0,0.6);">You're one step away from having your own account! Just click on the button below to confirm your email.</p>
	        
          	<a style="width:230px;margin-bottom:20px;display:block;background-color:#4285f4;padding:10px 0px 10px 0px;text-decoration: none;color:white;border-radius: 4px;font-size:18px;" href=%s>Confirm Email address</a>
	          
		</div>
	</center>
</div>


"""

def send_email(emaillist,username,link,message = email_text):
	assert isinstance(emaillist,str) or isinstance(emaillist,list), "Must be string or List"

	gmail_user = 'rafflesinfocommclub@gmail.com'  
	gmail_password = 'RafflesInstitutionIndianCulturalClub'
	sent_from = gmail_user
	to = ['']

	if isinstance(emaillist,list):
		to = emaillist
	else:
		to = [emaillist]


	subject = 'Confirm Your Email Address' 
	email_text = message % (", ".join(to), subject,username,link)

	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(sent_from, to, email_text)
		server.close()
		return True
	except:
		return False

if __name__ == "__main__":
	send_email("chennuode2012@gmail.com","Nuode","nuode.com")



