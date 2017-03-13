from davoduTSA import settings

class Django_Secrets:
    def __init__(self):
        self.key = settings.SECRET_KEY


class Oauth_Secrets:
    def __init__(self):
    	self.access_token = ""
    	self.access_token_secret = ""
    	self.consumer_key = ""
    	self.consumer_secret = ""
        