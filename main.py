import requests
import json
import argparse
import datetime
from datetime import datetime, timedelta
import pause

GET_CURRENT_POLL = "https://api.bollsvenskan.jacobadlers.com/dota/signup"
BASE = "https://nextcloud.jacobadlers.com/index.php"
CHECK_USER_NAME = "/apps/polls/check/username"
TOKEN = "/csrftoken"
REGISTER = "/apps/polls/s/ayWuLpAQxt1LOVSW/register"

def job() -> bool:
    s = requests.session()

    CURRENT_POLL = json.loads(s.get(GET_CURRENT_POLL).text)['currentPollUrl'].split('/')[-1]

    REGISTER = f"/apps/polls/s/{CURRENT_POLL}/register"

    csrf_token = s.get(BASE + TOKEN)
    res = json.loads(csrf_token.text)

    HEADERS = {
        'origin': 'https://nextcloud.jacobadlers.com',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        'requesttoken': res['token']
    }

    check_name_payload = {
        'token': CURRENT_POLL,
        'userName': USERNAME
    }

    check_name_req = s.post(BASE + CHECK_USER_NAME, headers=HEADERS, data=check_name_payload)
    if not check_name_req.ok:
        print("Failed namecheck", check_name_req)
        return False

    register_payload = {
        'userName': USERNAME,
        "emailAddress": ""
    }

    register_req = s.post(BASE + REGISTER, headers=HEADERS, data=register_payload)
    if not register_req.ok:
        print("Failed register", register_req)
        return False

    res = json.loads(register_req.text)
    token = res['share']['token']
    print(token)

    VOTE = f"/apps/polls/s/{token}/vote"

    vote_payload = {
        "optionId": 471,
        "setTo": "yes"
    }

    vote_req = s.put(BASE + VOTE, headers=HEADERS, data=vote_payload)
    if not vote_req.ok:
        print("Failed register", vote_req)
        return False

    vote_payload = {
        "optionId": 472,
        "setTo": "yes"
    }

    vote_req = s.put(BASE + VOTE, headers=HEADERS, data=vote_payload)
    if not vote_req.ok:
        print("Failed register", vote_req)
        return False

    vote_payload = {
        "optionId": 473,
        "setTo": "yes"
    }

    vote_req = s.put(BASE + VOTE, headers=HEADERS, data=vote_payload)
    if not vote_req.ok:
        print("Failed register", vote_req)
        return False

    print("Succesfully signed up")
    return True

def sleepUntillWednesday() -> datetime:
    now = datetime.today()
    days = getDays(now.weekday())

    nextWed = now + timedelta(days=(days), hours=(24 - now.hour - 1 + 4), minutes=(60 - now.minute - 1 + 5),  seconds=(60 - now.second))
    
    print("Will sleep untill", nextWed, "which is:", nextWed - now)
    pause.until(nextWed)
    return nextWed

def getDays(day) -> int:
    if day == 0:
        return 1
    elif day == 1:
        return 0
    elif day == 2:
        return -1
    elif day == 3:
        return 5
    elif day == 4:
        return 4
    elif day == 5:
        return 3
    elif day == 6:
        return 2

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="username", required=True)
    args = parser.parse_args()

    USERNAME = args.name
    GAMES = args.games

    nextWed = sleepUntillWednesday()
    while(True):
        if not job():
            quit()
        nextWed += timedelta(days=(7))
        pause.until(nextWed)

