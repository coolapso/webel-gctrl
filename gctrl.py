import requests
import argparse
from bs4 import BeautifulSoup


base_url = 'https://webel-online.se'
login_url = f'{base_url}/lblogin.asp'
panel_url = f'{base_url}/bil/main.asp'
base_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': base_url,
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': f'{base_url}/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Priority': 'u=0, i'
}

login_data = {
    'zaa': 'login',
    'username': '',
    'password': '',
    'login': 'Login'
}

turn_on_data = { 
    'dirstartruntime': '60',
    'Directstart': 'Direct start your car heater location',
    '_confirmDirstart': 'OFF',
    '_lock': 'OFF'
}

turn_off_data = {
    'dirstartruntime': '30',
    'CancelDirectstart': 'Cancel+direct+start',
    '_confirmDirstart': 'OFF',
    '_lock': 'OFF',
}

def login(session: requests.Session, headers, data: dict) -> requests.Response:
    """Logs in and returns with a session and returns the response"""
    return session.post(login_url, headers=headers, data=data, allow_redirects=True)

def turn_on_power(session: requests.Session, data: dict) -> requests.Response:
    """Uses session created with login and sends a post request to turn on power"""
    return session.post(panel_url, data=data, allow_redirects=True)

def turn_off_power(session: requests.Session, data: dict) -> requests.Response:
    """Uses session created with login and sends a post request to turn off power"""
    return session.post(panel_url, data=data, allow_redirects=True)

def get_panel(session: requests.Session) -> requests.Response:
    """Uses Session created with login and sends a get request to get the web pahel html"""
    return session.get(panel_url, allow_redirects=True)

def is_power_disabled(html: str) -> bool:
    """Inspects the web panel html for the "cancel direct start" button and checks if it's disabled, disabled means the plug is off"""
    soup = BeautifulSoup(html, 'html.parser')
    input_element = soup.find('input', {'name': 'CancelDirectstart', 'data-langify': 'cancel-direct-start'})

    if input_element and input_element.has_attr('disabled'):
        return True

    return False


def main(): 
    parser = argparse.ArgumentParser(description="Control car heater.")
    parser.add_argument("action", choices=["on", "off", "status"], help="Specify 'on', 'off', or 'status'.")
    parser.add_argument("--runtime", type=int, help="Specify the runtime in minutes", default=30)
    parser.add_argument("--username", help="Specify the username")
    parser.add_argument("--password", help="Specify the password")
    
    args = parser.parse_args()
    login_data["username"]  = args.username
    login_data["password"] = args.password
    turn_on_data["dirstartruntime"] = args.runtime
    session = requests.Session()

    login(session, base_headers, login_data)
    loggedInHeaders = base_headers
    loggedInHeaders['Referer'] = panel_url

    if args.action == "on":
        turn_on_power(session, turn_on_data)
    elif args.action == "off":
        turn_off_power(session, turn_off_data)
    elif args.action == "status":
        response = get_panel(session)
        if response.status_code == 200:
            if is_power_disabled(response.text):
                print("Directstart is not active")
            else:
                print("Directstart is active")


if __name__ == '__main__':
    main()
