
import config
import requests

def addSubscription(user_details, ad_categories):
    try:
        url = config.adServiceUrl+'/subscribe'
        payload = {
            "user-details": user_details,
            "ad-categories": ad_categories
        }
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            return "Successfully inserted"

    except Exception as e:
        print("Failed to add sunscription", e)