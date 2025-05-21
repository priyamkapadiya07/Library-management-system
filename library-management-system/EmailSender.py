import yagmail

class EmailSender:
    def __init__(self):
        self.sender_email = "priyampatel968@gmail.com"
        # self.receiver_email = input("Enter receiver email : ")
        self.subject = "Book Report"
        self.body = "Please find the attached Book report PDF."
        self.attachment_file = "book_report.pdf"

    def send_email(self):
        try:
            yag = yagmail.SMTP(self.sender_email, "nxrx ergs eegb bpkx")
            yag.send(
                to=input("Enter receiver email : "),
                subject=self.subject,
                contents=self.body,
                attachments=self.attachment_file
            )
            print("📧 Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

# https://myaccount.google.com/u/1/apppasswords - for make app password