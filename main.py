import urllib.request
import json
import os
import time
import unicodedata

# https://qiita.com/delicious-locomoco/items/1adfe3ede4247b72759d


def left(digit, msg):
    for c in msg:
        if unicodedata.east_asian_width(c) in ('F', 'W', 'A'):
            digit -= 2
        else:
            digit -= 1
    return msg + ' '*digit


user_id = os.environ["USER"]
since = None

while True:
    try:
        req = urllib.request.Request(
            f"http://api.twitcasting.tv/api/commentlist?type=json&user={user_id}&since={since}")
        with urllib.request.urlopen(req) as res:
            comments = json.loads(res.read())
            if len(comments) != 0:
                since = comments[0]['commentid']
            comments.reverse()
            for comment in comments:
                print(
                    f"{left(30,comment['userstatus']['name'])}@{left(20,comment['userstatus']['userid'])} {comment['message']}")
    except:
        print("エラー")

    time.sleep(3)
