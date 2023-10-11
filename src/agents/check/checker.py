from uagents import Agent, Context, Protocol
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from uagents.setup import fund_agent_if_low
import csv 

logging.basicConfig(filename='currency_checker.log', level=logging.INFO)

smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'techfestraap@gmail.com'
sender_password = 'vxmm wojx idjm shuy'

checker = Agent(name="checker", seed="checker agent")

def create_email(to_email, body, subject):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = to_email
    message.attach(MIMEText(body, 'plain'))
    return message

def send_email(message):
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, message['To'], message.as_string())
            logging.info(f"Email sent to {message['To']}")
    except Exception as e:
        logging.error(f"Email sending error: {str(e)}")

fund_agent_if_low(checker.wallet.address())
checker_agent_protocol = Protocol("CheckerAgent")


@checker.on_interval(period=5)
async def check(ctx: Context):
    try:
        with open(r"C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\user_data.json", 'r') as f:
            data = json.load(f)

        for email in data:
            tracks_to_remove = []

            for track in data[email]:
                from_this_currency = data[email][track]["From_this_currency"]
                to_this_currency = data[email][track]["to_this_currency"]
                threshold1 = float(data[email][track]["Threshold1"])
                threshold2 = float(data[email][track]["Threshold2"])

                api_url = f'https://v6.exchangerate-api.com/v6/f4b4ef0a8c3dc88bf7db4859/latest/{from_this_currency}'
                response = requests.get(api_url)
                chart = response.json()

                rate = chart["conversion_rates"][to_this_currency]
                ctx.logger.info(f"Current Rate is {rate}")

                if rate < threshold1 or rate > threshold2:
                    message = create_email(
                        email,
                        f"{to_this_currency} rate is outside of thresholds. Current rate: 1 {from_this_currency} = {rate} {to_this_currency}",
                        "Threshold Alert"
                    )
                    send_email(message)
                    tracks_to_remove.append(track)

            for track_to_remove in tracks_to_remove:

                del data[email][track_to_remove]

        with open(r'C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\database.csv', 'w', newline='') as database_file:
            writer = csv.writer(database_file)
            for email in data:
                for track in data[email]:
                    from_currency = data[email][track]["From_this_currency"]
                    to_currency = data[email][track]["to_this_currency"]
                    threshold1 = data[email][track]["Threshold1"]
                    threshold2 = data[email][track]["Threshold2"]
                    writer.writerow([email, threshold1, threshold2, from_currency, to_currency])

        with open(r"C:\Users\pushp\Documents\pythonAI\currency_monitor-main\src\utils\user_data.json", 'w') as f:
            json.dump(data, f)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


checker.include(checker_agent_protocol)