import requests
# import urlparse

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
    
    
# def valid_url(url):
#     parsed_url = urlparse(url)
#     # Check if the URL has a valid scheme (e.g., 'http', 'https') and netloc (domain)
#     return parsed_url.scheme and parsed_url.netloc