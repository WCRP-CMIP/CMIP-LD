import requests

def url_exists(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return None
    except requests.Timeout:
        return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    