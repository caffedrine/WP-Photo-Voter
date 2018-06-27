import string
import time
import datetime
import sys
import random

import requests
from requests import Session

from util import *

# GLOBALS
contest_id = "22"
vote_id = "207"
requestUrl = "https://www.freerider.ro/wp-admin/admin-ajax.php?vote_id={id}".format(id=vote_id)

# Proxy list file and array()
proxy_list = "proxy.txt"
proxy_array = []


# Function used to send vote
def try_vote(contest_id, vote_id, req_url, proxy):
    # Web requests session
    web_session = requests.Session()  # type: Session

    # Generate random uid
    uid=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

    # Send first request in order to get correct cookies
    # try:
    #     web_session.get("https://www.freerider.ro/concurs-foto/{id}".format(id=vote_id))
    # except:
    #     pass

    # Build request header
    request_header = {"User-Agent"      : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                      "Accept"          : "*/*",
                      "Accept-Language" : "en-GB,en;q=0.5",
                      "Accept-Encoding" : "gzip, deflate",
                      "Referer"         : req_url,
                      "Content-Type"    : "application/x-www-form-urlencoded; charset=UTF-8",
                      "X-Requested-With": "XMLHttpRequest",
                      "Cookie"          : "JCS_INENREF=; JCS_INENTIM=1530037773197; viewed_cookie_policy=yes; fv_uid={uid}; PHPSESSID=e456adf18a85d4436db4677171293e85; evercookie_cache={uid}; evercookie_etag={uid}".format(uid=uid),
                      "Connection"      : "Close"}

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
                    "ds"        : "MTg3OXgxMDU2"}

    # Proxy tuple
    curr_proxy_tuple = {"https": "socks4://" + proxy, "http": "socks4://" + proxy}

    # Store response
    function_resp = { "status" : False, "error_desc" : ""}

    # Try send HttpWebRequest
    try:
        response = web_session.post(url=req_url, data=post_content, headers=request_header, timeout=15, proxies=curr_proxy_tuple)
        function_resp['status'] = True;

        # Check response to know whether vote was counted or not
        vote_resp_code = find_between(str(response.content), '"res":', ',')

        # Response code 1 means the vote was successfully counter
        if vote_resp_code.__contains__("1") is False:
            function_resp['status'] = False;
            function_resp['error_desc'] = "Request succeed but somehow vote was not counted :( Are you trying to vote twice from the same IP?"

    except Exception as e:
        function_resp['error_desc'] = str(e.message)
        function_resp['status'] = False

    return function_resp


# Main function
def main():
    # Load socks4 proxy list
    with open(proxy_list) as proxies:
        for proxy in proxies:
            proxy_array.append(proxy.replace('\n', ''))

    # Loop through every proxy and try to vote
    successVotes = 0
    failVotes = 0
    for i in range(len(proxy_array)):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f')[:-3]
        sys.stdout.write("[{timestamp}] {index}. Voting from {proxy}...".format(timestamp=st, index=str(i+1), proxy=proxy_array[i]))
        vote_result = try_vote(contest_id, vote_id, requestUrl, proxy_array[i])
        if vote_result['status'] is True:
            successVotes += 1
            sys.stdout.write("SUCCESS\n")
        else:
            failVotes += 1
            sys.stdout.write("FAILED - {reason}\n".format(reason=vote_result['error_desc']))

    # Print final stats
    print("===== STATS =====")
    print("Total number of proxies: {proxies_number}".format( proxies_number=str(len(proxy_array))))
    print("Success votes: {success_votes}".format(success_votes=str(successVotes)))
    print("Failed votes: {failed_votes}".format(failed_votes=str(failVotes)))


# Entry point
if __name__ == "__main__":
    main()
