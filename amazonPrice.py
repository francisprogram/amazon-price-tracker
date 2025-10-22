import requests # import requests to recieve data from Amazon
from bs4 import BeautifulSoup # import BeautifulSoup to parse HTML Web data from Amazon requests
import smtplib # import smtplib to send email using SMTP
import sqlite3 as sq
import time
import math

senderEmail = "[your email]" # Email to send from
recEmail = "[target email]" # Email to send to, can be same as senderEmail
appPass = "[app password]" # Your app password
fullPrice = 663 #Usual full price of item (laptop in this case)

def checkPrice(): #procedure to request and format price data and compare to full price of laptop

    #Setting up connection with database
    connection = sq.connect("priceData.db")
    
    #Instantiating cursor object to be able to modify and interact with database
    cursor = connection.cursor()

    #Creating "Data" table if it does not already exist in database
    cursor.execute("CREATE TABLE IF NOT EXISTS Data (ID text primary key not null, newprice VARCHAR(4) not null, fullprice VARCHAR(4) not null, change VARCHAR(4) not null)")


    # Storing URL to request web data from
    URL = "https://www.amazon.co.uk/Lenovo-ThinkPad-Ryzen-Windows-Laptop/dp/B0DPGG498M/ref=sr_1_7?dib=eyJ2IjoiMSJ9.ArGdZH0anE9cDfVse3UTOYnkB2rCQvrlk47H2N0S6UEdkdzIwQSyaxz-YSZW9CtlIC6uf1_I5CMPcBUfnGrLxzcRS2TYqNtvOC6CjWPcDMZxRa2JpHqYMNmacbE_C-96Pr21Td-g5IWvNJCOzUzWBA04a5wJ-45QUuGzmSUCFXivB8ScM0KOezkaY5iwjDE_Le8V6WLchVZ13xOlRzUPmePrhJF6nW5SRC55zsQuJdo.gILNiWXVgCufpyGVlLxTXRbx9PsvXZk_NHJq8DjXte8&dib_tag=se&keywords=Thinkpad&qid=1760987537&sr=8-7"

    # Storing header data to be used to identify this system to the Amazon server
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"}

    #Requesting web data from Amazon
    pageData = requests.get(URL, headers = headers)

    #Parsing recieved data using bs4 HTML parser (as opposed to XML parser)
    soup = BeautifulSoup(pageData.content, "html.parser")

    #Finding current listed price inside parsed Amazon data including sign and decimals and formatting price
    price = soup.find(attrs = {"aok-offscreen"}).get_text().strip() 

    ## For multiple urls, request, parse and find multiple times, changing URL variable each time. ##
    
    #Removing pound sign and rounding listed price to the nearest integer
    convertedPrice = int(round(float(price[1:])))
    print(convertedPrice)

    #Calculating change separately to be able to add a + sign if positive (optional)
    change = "+"+str(round(fullPrice - float(price[1:]), 2)) if round(fullPrice - float(price[1:]), 2) > 0 else round(fullPrice - float(price[1:]), 2)

    #Creating new record noting the time of the check, the price listed, full price and difference in prices
    cursor.execute("INSERT INTO Data VALUES(?,?,?,?)",(round(time.time()), price[1:], fullPrice, change))

    #Committing changes to database
    connection.commit()
    
    print("committed")
    #Sending email if listed price is smaller than full price
    if convertedPrice < fullPrice:
        sendGmail()

def sendGmail():

    #Setting up client server to connect to gmail from and send data from
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    #Logging into gmail server to authenticate
    server.login(senderEmail, appPass)

    #Subject of email
    subject = "Price change"

    #Email body
    body = "Price change on Lenovo Thinkpad, fallen below 663 or changed and is still below 663.\n\nLink to it: https://www.amazon.co.uk/Lenovo-ThinkPad-Ryzen-Windows-Laptop/dp/B0DPGG498M/ref=sr_1_7?dib=eyJ2IjoiMSJ9.ArGdZH0anE9cDfVse3UTOYnkB2rCQvrlk47H2N0S6UEdkdzIwQSyaxz-YSZW9CtlIC6uf1_I5CMPcBUfnGrLxzcRS2TYqNtvOC6CjWPcDMZxRa2JpHqYMNmacbE_C-96Pr21Td-g5IWvNJCOzUzWBA04a5wJ-45QUuGzmSUCFXivB8ScM0KOezkaY5iwjDE_Le8V6WLchVZ13xOlRzUPmePrhJF6nW5SRC55zsQuJdo.gILNiWXVgCufpyGVlLxTXRbx9PsvXZk_NHJq8DjXte8&dib_tag=se&keywords=Thinkpad&qid=1760987537&sr=8-7"

    #Combining subject and body into single message
    msg = f"Subject: {subject}\n\n{body}"

    #Sending email to own email
    server.sendmail(senderEmail, recEmail, msg)
    print("sent")

    #Ending session
    server.quit()
    
checkPrice()



