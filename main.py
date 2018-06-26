import requests
from requests import Session

from util import *

# GLOBALS
contest_id = "25"
vote_id = "206"
requestUrl = "https://www.freerider.ro/wp-admin/admin-ajax.php?vote_id=%s" % vote_id

# Proxy list file and array()
proxy_list = "proxy.txt"
proxy_array = []


# Function used to send vote
def try_vote(contest_id, vote_id, req_url, proxy):
    # Web requests session
    web_session = requests.Session()  # type: Session

    # Generate random uid or grab it from last session
    uid = "iTLZzpup"

    # Build request header
    request_header = {"User-Agent"      : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                      "Accept"          : "*/*",
                      "Accept-Language" : "en-GB,en;q=0.5",
                      "Accept-Encoding" : "gzip, deflate",
                      "Referer"         : req_url,
                      "Content-Type"    : "application/x-www-form-urlencoded; charset=UTF-8",
                      "X-Requested-With": "XMLHttpRequest",
                      "Cookie"          : "JCS_INENREF=; JCS_INENTIM=1530037773197; viewed_cookie_policy=yes; fv_uid={uid}; PHPSESSID=e456adf18a85d4436db4677171293e85; evercookie_cache={uid}; evercookie_etag={uid}".format(uid=uid),
                      "Connection"      : "Close"
    }

    # Build second POST request
    post_content = {"action"    : "vote",
                    "contest_id": contest_id,
                    "vote_id"   : vote_id,
                    "post_id"   : "131331",
                    "rr"        : "-",
                    "uid"       : uid,
                    "pp"        : "2260506713",
                    "fuckcache" : "705RsINb",
                    "some_str"  : "099109b4a7",
                    "ds"        : "MTg3OXgxMDU2"
                    }

    #try:
    curr_proxy_tuple = {"https" : "socks5://" + proxy, "http" : "socks5://" + proxy}
    response = web_session.post(url=req_url, data=post_content, headers=request_header, timeout=10, proxies=curr_proxy_tuple)
    #except:
        #response = None

    if response is None or response.status_code != 200:
        return False
    else:
        return True


# Main function
def main():
    # Load proxy list
    with open(proxy_list) as proxies:
        for proxy in proxies:
            proxy_array.append(proxy.replace('\n', ''))

    for proxy in proxy_array:
        try_vote(contest_id, vote_id, requestUrl, proxy)


if __name__ == "__main__":
    main()
