import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from app import check_food_availability

load_dotenv()
PASS = os.getenv("APP_PASS")

# hi

def send_email(subject, message, from_email, to_emails, password, from_name=None):
    try:
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(from_email, password)

        for to_email in to_emails:
            msg = MIMEMultipart()
            msg['From'] = f"{from_name} <{from_email}>" if from_name else from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            server.sendmail(msg['From'], msg['To'], msg.as_string())
            print("successfully sent email to %s:" % (msg['To']))

        server.quit()
    except Exception as e:
        print("failed to send mail to %s: %s" % (msg['To'], str(e)))


def notify(food):
    avail = check_food_availability(food)

    data = json.loads(avail)
    if ("error" in data):
        return ""

    data_iter = iter(data.items())
    next(data_iter)

    result = f"{food} is available at:\n"
    for location, times in data_iter:
        result += f"\t{location} during:\n" + \
            '\n'.join("\t- " + t for t in times) + "\n"
    return result + "\n"


if __name__ == "__main__":

    mail_dict = {
        "ranadkar@ucsc.edu": ["Dal Saag"],
        "arvora@ucsc.edu": ["Dal Saag"],
        "aadisharmahope@gmail.com": ["Dal Saag"],
        "aiyhuang@ucsc.edu": ["Dal Saag"],
        "jchow10@ucsc.edu": ["New England Clam Chowder"],
        "jmehta1@ucsc.edu": ["Dal Saag", "Potato Samosas"]
    }

    # mail_dict = {
    #     "ranadkar@ucsc.edu": ["Dal Saag"],
    # }

    # TODO: make it not repeatedly call check_food_availability
    for email, food_list in mail_dict.items():
        out = ""
        for food in food_list:
            out += notify(food)

        if len(out) > 0:
            print(out)
            send_email("Dining Hall Foods", out,
                       "ilovedaalsaag@gmail.com", [email], PASS, "Daal Saag")
        else:
            print(f"No food available for {email}")
