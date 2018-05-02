import os
import csv
import smtplib
from email.mime.text import MIMEText


def load_email_credentials():
  """Load Amazon SES email credentials from a CSV file
  """
  cred = {}
  row_idx = 0

  dir_path = os.path.dirname(os.path.abspath(__file__))
  credential_file = os.path.join(dir_path, "email_credentials.csv")
  with open(credential_file) as csv_file:
    rdr = csv.reader(csv_file)
    for row in rdr:
        if row_idx == 1:
          cred["username"] = row[1]
          cred["password"] = row[2]
        row_idx += 1

  return cred

def send_self_email(subject, body, is_html=True):
  """Sends an email from me to me using Amazon SES
  """
  credentials = load_email_credentials()
  smtp_host = "email-smtp.eu-west-1.amazonaws.com"
  from_email = "jeremy.d.collins@gmail.com"

  msg = None
  if is_html:
    msg = MIMEText(body, "html", "utf-8")
  else:
    msg = MIMEText(body, "plain", "utf-8")
  msg["To"] = from_email
  msg["From"] = from_email
  msg["Subject"] = subject

  s = smtplib.SMTP_SSL(smtp_host, 465)
  s.set_debuglevel(1)
  s.login(credentials["username"], credentials["password"])
  s.sendmail(from_email, from_email, msg.as_string())

def self_email_test():
  html_body = """\
  <html>
    <head></head>
    <body>
      <p>This is a test message generated from a Python script and delivered via Amazon SES.</p>
    </body>
  </html>\r\n
  """
  send_self_email("Testing", html_body, True)

if __name__ == "__main__":
    self_email_test()


