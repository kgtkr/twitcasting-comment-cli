import urllib.request
import json
import os
import time
import unicodedata
import webbrowser
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import threading

HOST = "localhost"
PORT = 5418
CLIENT_ID = "3069403147.33fc408fd750791a4cfeb1028f772ad3e20ecacc0a1c6bcb113fcf6343c9a79b"

user_id = os.environ["USER"]


# https://qiita.com/delicious-locomoco/items/1adfe3ede4247b72759d


def left(digit, msg):
    for c in msg:
        if unicodedata.east_asian_width(c) in ('F', 'W', 'A'):
            digit -= 2
        else:
            digit -= 1
    return msg + ' '*digit


def api(token, path):
    req = urllib.request.Request("https://apiv2.twitcasting.tv"+path)
    req.add_header("Accept", "application/json")
    req.add_header("X-Api-Version", "2.0")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read())


def runApp(token):
    since = None

    while True:
        try:
            comments = api(
                token, f"/movies/{api(token, f'/users/{user_id}/current_live')['movie']['id']}/comments?limit=50"+(f"&slice_id={since}" if since != None else ""))["comments"]
            if len(comments) != 0:
                since = comments[0]['id']
            comments.reverse()
            for comment in comments:
                print(
                    f"{left(30,comment['from_user']['name'])}@{left(20,comment['from_user']['screen_id'])} {comment['message']}")
        except Exception as e:
            print("エラー")
            print(e)

        time.sleep(3)


class MyHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/":
            body = b"<script>location.href='?'+location.hash.substr(1);</script>"
            token = None
        else:
            body = b"<script>location.href='about:blank';</script>"
            token = urllib.parse.parse_qs(
                urlparse(self.path).query)["access_token"][0]
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)
        if token != None:
            runApp(token)


webbrowser.open(
    f"https://apiv2.twitcasting.tv/oauth2/authorize?client_id={CLIENT_ID}&response_type=token")

httpd = HTTPServer(
    (HOST, PORT), MyHandler)
httpd.serve_forever()
