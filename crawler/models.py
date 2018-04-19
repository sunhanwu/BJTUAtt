

class UserModel:
    def __init__(self, name, username, url, profile, uid=None, fb_id=None, friend_num=0):
        self.uid = uid
        self.name = name
        self.username = username
        self.fb_id = fb_id
        self.url = url
        self.profile = profile
        self.friend_num = friend_num


class RelationshipModel:
    def __init__(self, uid1, uid2):
        self.uid1 = uid1
        self.uid2 = uid2
