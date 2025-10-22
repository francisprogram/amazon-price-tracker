# amazon-price-tracker
A Python program that monitors prices of items on Amazon, stores price history in a local database and automatically sends an email alert if the price drops below full price or changes.  

# Features
The program: 

- Scrapes web page data from Amazon
- Sends email alert when prices drop
- Stores price history in database locally
- Records timestamp, listed price, full price and change in price between listed and full prices.

# How to use
To use this program:

1) Clone this repository

2) Install required libraries using: `pip install -r requirements.txt`

3) Set up an app password for python SMTP: https://myaccount.google.com/apppasswords

4) Open program, fill in details and run program (your email, email to send to, app password and full price)

# Tech Stack
- Python 3
- BeautifulSoup4
- Requests
- smtplib
- SQLite3
