
class NotificationDispatcher:
    
    def __init__(self):
        pass
        
    
    def dispatch(self,email,sms,message):
        if email:
            self.send_email(email)
        if sms:
            self.send_sms(sms)
    
    def send_email(self,email,message):
        print(message)
    
    def send_sms(self,sms,message):
        print(message)