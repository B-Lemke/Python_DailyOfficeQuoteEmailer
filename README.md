# DailyOfficeQuoteEmailer
This python script sends a random quote from the office to emails of your choice.

______________

## Text Files
You will need to make a login.txt and emails.txt file in the same directory as the TheOfficeWebMailer.py project using the following formats


#### login.txt
The following is the format that should be used for the login.txt file:
>{"username": "emailUserNameGoesHere", "pass": "emailPasswordGoesHere"}

Ensure that you replace the email username and password with the correct login information for the email you wish to send the quote from




#### emails.txt
The following is the format that should be used for the emails.txt file:
>{"Emails": ["email1@gmail.com","email2@gmail.com"]}

The emails in this list will each recieve a copy of the randomly selected quote. You may add or delete as many members to this list as you wish.
