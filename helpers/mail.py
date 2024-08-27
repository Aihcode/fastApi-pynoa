import os
import resend

class Email:
    def __init__(self):
        self.api_key = os.environ["RESEND_API_KEY"]
        if self.api_key == "":
            raise Exception("RESEND_API_KEY is not set")
        print(self.api_key, "email system started")


    def send(self, from_param: str = "Acme <onboarding@resend.dev>", to_list: list = ["delivered@resend.dev"], subject: str = "hello world", html: str = "<strong>it works!</strong>"):
        print("send email", from_param, to_list, subject, html)
        resend.api_key = self.api_key
        params: resend.Emails.SendParams = {
            "from": from_param,
            "to": to_list,
            "subject": subject,
            "html": html,
        }
    
        email = resend.Emails.send(params)

        if email is not None:
            print(email)
        else:
            print("email not sent")
        return email