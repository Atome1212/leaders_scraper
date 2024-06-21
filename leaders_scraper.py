import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict

def get_first_paragraph(url: str, session: requests.Session) -> str:
    """
    Retrieves and cleans the first relevant (complete) paragraph from a given Wikipedia article.

    Parameters:
    first_name (str): The first name of the person.
    last_name (str): The last name of the person.
    url (str): The URL of the Wikipedia page.
    session (requests.Session): A requests.Session used to perform the HTTP request.

    Returns:
    str: The cleaned first relevant paragraph.
    """
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    infobox_table = soup.find('table', {'class': 'infobox'})

    paragraph = infobox_table.find_next_sibling('p') if infobox_table else ""
        
    if not paragraph:
        return "No paragraph found."
    
    clean_text = paragraph.get_text(separator=" ", strip=True)
    
    clean_text = re.sub(r'\[.*?\]', '', clean_text)
    clean_text = re.sub(r'\([^)]*\)', '', clean_text)
    clean_text = re.sub(r'/.*?/', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = clean_text.replace(' ,', ',').replace(' .', '.').strip()
    
    print("===========================")
    print("Cleaned paragraph:")
    print(clean_text)
    
    print(f'{url} done !')
    return clean_text.strip()

def get_cookies(root_url: str) -> requests.cookies.RequestsCookieJar:
    """
    Retrieves cookies necessary for subsequent requests.

    Parameters:
    root_url (str): The base URL for retrieving cookies.

    Returns:
    requests.cookies.RequestsCookieJar: The retrieved cookies.
    """
    cookie_url = f'{root_url}/cookie'
    cookie_req = requests.get(cookie_url)
    return cookie_req.cookies

def get_leaders() -> Dict[str, List[Dict]]:
    """
    Retrieves leaders for each country and their respective biographies from Wikipedia.

    Returns:
    Dict[str, List[Dict]]: A dictionary where keys are country names and values are lists of leaders with their biographies.
    """
    root_url = 'https://country-leaders.onrender.com'
    countries_url = f'{root_url}/countries'
    leaders_url = f'{root_url}/leaders'
    
    cookies = get_cookies(root_url)

    countries_req = requests.get(countries_url, cookies=cookies)
    countries = countries_req.json()

    leaders_per_country = {}
    with requests.Session() as session:
        for country in countries:
            while True:
                leaders_req = requests.get(leaders_url, cookies=cookies, params={'country': country})
                if leaders_req.status_code == 403:
                    cookies = get_cookies(root_url)
                else:
                    leaders = leaders_req.json()
                    break
            
            for leader in leaders:
                if 'wikipedia_url' in leader:
                    try:
                        leader['bio'] = get_first_paragraph(leader['wikipedia_url'], session)
                    except Exception as e:
                        print(f"Failed to fetch paragraph for {leader['wikipedia_url']}: {e}")
                        leader['bio'] = "Bio not available"

            leaders_per_country[country] = leaders
    return leaders_per_country

def save(leaders_per_country: Dict[str, List[Dict]]) -> None:
    """
    Saves the leaders per country data to a JSON file.

    Parameters:
    leaders_per_country (Dict[str, List[Dict]]): The dictionary containing leaders per country data.
    """
    with open('./Data/leaders.json', 'w', encoding='utf-8') as f:
        json.dump(leaders_per_country, f, ensure_ascii=False, indent=4)
    
def check(leaders_per_country: Dict[str, List[Dict]]) -> None:
    """
    Checks if the saved leaders per country data matches the original data.

    Parameters:
    leaders_per_country (Dict[str, List[Dict]]): The original dictionary containing leaders per country data.
    """
    with open('./Data/leaders.json', 'r', encoding='utf-8') as f:
        loaded_leaders = json.load(f)
    print("Data loaded successfully and matches the original leaders_per_country.") if loaded_leaders == leaders_per_country else print("Data loaded does not match the original leaders_per_country.")

def main() -> None:
    """
    Main function to execute the script: retrieves leaders, saves them, and checks the saved data.
    """
    leaders_per_country: Dict[str, List[Dict]] = get_leaders()
    save(leaders_per_country)
    check(leaders_per_country)

if __name__ == "__main__":
    main()
