import requests
from config import Config


class FacebookGroups:
    fb_access_key = Config.FACEBOOK_API_ACCESS_TOKEN
    user_id = 'john.d.case'
    group_id = 'socialisteconomics'
    url = f"https://graph.facebook.com/{group_id}/feed?limit=5&amp;access_token={Config.FACEBOOK_API_ACCESS_TOKEN}"

    @staticmethod
    def get_fb_groups():

            url = f"https://graph.facebook.com/{FacebookGroups.user_id}/groups"
            return requests.get(url)


