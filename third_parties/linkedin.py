from dotenv import load_dotenv
import requests
import os



load_dotenv()


def scrap_linkedin_profile(url:str,mock:bool = False):
    """ scrap info from linkedin profiles
    """
    print("call came here-------------------")
    if mock:
        url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
        response  = requests.get(
            url,
            timeout=10,
        )
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey" : os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl":url
        }

        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    # data = response.json().get("person")

    try:
        json_data = response.json()
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return {}

    data = json_data.get("person")

    # ✅ Fallback if data is None
    if not data:
        print(f"⚠️ No 'person' data found for URL: {url}")
        return {}

    print(data)
    
    data = {
         k : v for k, v in data.items()
         if v not in ([], "","",None) and k not in ["certifications"]
    }
    return data





if __name__=="__main__":
        print(
            scrap_linkedin_profile(url="https://www.linkedin.com/in/gajanan-shinde-64529221a/", mock=True)
        )

