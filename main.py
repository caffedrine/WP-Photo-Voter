import string
import time
import datetime
import sys
import random
import concurrent.futures

import requests
from requests import Session

from util import *

# GLOBALS
contest_id = "22"
vote_id = "209"
request_url = "https://www.freerider.ro/wp-admin/admin-ajax.php?vote_id={id}".format(id=vote_id)

# Proxy list file and array()
proxy_list = "proxy.txt"
proxy_array = []


# Function used to send vote
def try_vote(contest_id, vote_id, req_url, attempts=2, proxy=None):
    # Web requests session
    web_session = requests.Session()  # type: Session

    # Generate random uid
    uid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

    # Build request header
    request_header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                      "Accept": "*/*",
                      "Accept-Language": "en-GB,en;q=0.5",
                      "Accept-Encoding": "gzip, deflate",
                      "Referer": req_url,
                      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "X-Requested-With": "XMLHttpRequest",
                      "Cookie": "JCS_INENREF=; JCS_INENTIM=1530037773197; viewed_cookie_policy=yes; fv_uid={uid}; PHPSESSID=e456adf18a85d4436db4677171293e85; evercookie_cache={uid}; evercookie_etag={uid}".format(
                          uid=uid),
                      "Connection": "Close"}

    # Build POST request
    post_content = {"action": "vote",
                    "contest_id": contest_id,
                    "vote_id": vote_id,
                    "post_id": "131331",
                    "rr": "-",
                    "uid": uid,
                    "pp": "2260506713",
                    "fuckcache": "705RsINb",
                    "some_str": "099109b4a7",
                    "ds": "MTg3OXgxMDU2"}

    # Store response
    function_resp = {"status": False, "error_desc": ""}

    for i in range(attempts):
        # Proxy tuple
        curr_proxy_tuple = None
        proxy_type = get_proxy_type(proxy, 3)
        if proxy_type is not 'DEAD':
            curr_proxy_tuple = {"https": "{proxy_type}://{ip_port}".format(proxy_type=proxy_type.lower(), ip_port=proxy),
                                "http": "{proxy_type}://{ip_port}".format(proxy_type=proxy_type.lower(), ip_port=proxy)}
        else:
            function_resp['error_desc'] = "Dead proxy"
            continue

        # # Send first request in order to get correct cookies
        # try:
        #     web_session.get("https://www.freerider.ro/concurs-foto/{id}".format(id=vote_id))
        # except:
        #     pass

        # Try send HttpWebRequest
        try:
            response = web_session.post(url=req_url, data=post_content, headers=request_header, timeout=15, proxies=curr_proxy_tuple)
            function_resp['status'] = True

            # Check response to know whether vote was counted or not
            vote_resp_code = find_between(str(response.content), '"res":', ',')

            # Response code 1 means the vote was successfully counter
            if vote_resp_code.__contains__("1") is False and vote_resp_code.__contains__("3") is False:
                function_resp['status'] = False
                function_resp['error_desc'] = "Request succeed but somehow vote was not counted :( Are you trying to vote twice from the same IP?"
                continue

        except Exception as e:
            function_resp['error_desc'] = str(e.message)
            function_resp['status'] = False

    return function_resp


# Main function
def main():
    # Load proxy list
    with open(proxy_list) as proxies:
        for proxy in proxies:
            proxy_array.append(proxy.replace('\n', ''))

    # # Check socks
    # index = 1
    # valid_proxies = 0
    # invalid_proxies = 0
    # with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    #     future_socks = {executor.submit(get_proxy_type, socks, 3): socks for socks in proxy_array}
    #
    #     # Wait for threads to finish
    #     for future in concurrent.futures.as_completed(future_socks):
    #         socks = future_socks[future]
    #         result = future.result()
    #         if result is 'DEAD':
    #             invalid_proxies += 1
    #         else:
    #             invalid_proxies += 1
    #         print("{index}. {proxy} -> {type}".format(index=str(index), proxy=socks, type=result))
    #         index += 1
    # ### Print Stats ###
    # print("===== STATS =====")
    # print("Total number of proxies: {proxies_number}".format(proxies_number=str(len(proxy_array))))
    # print("Success votes: {success_votes}".format(success_votes=str(valid_proxies)))
    # print("Failed votes: {failed_votes}".format(failed_votes=str(invalid_proxies)))

    # Loop through every proxy and try to vote
    success_votes = 0
    fail_votes = 0
    index = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        work_requests = {executor.submit(try_vote, contest_id=contest_id, vote_id=vote_id, req_url=request_url, attempts=3, proxy=socks): socks for socks in proxy_array}
        # Wait for threads to finish
        for future in concurrent.futures.as_completed(work_requests):
            socks = work_requests[future]
            result = future.result()

            st = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f')[:-3]
            sys.stdout.write("[{timestamp}] {index}. {proxy} -> ".format(timestamp=st, index=str(index + 1), proxy=socks))
            if result['status'] is True:
                success_votes += 1
                sys.stdout.write("SUCCESS\n")
            else:
                fail_votes += 1
                sys.stdout.write("FAILED - {reason}\n".format(reason=result['error_desc']))
            index += 1

    # Print final stats
    print("===== STATS =====")
    print("Total number of proxies: {proxies_number}".format(proxies_number=str(len(proxy_array))))
    print("Success votes: {success_votes}".format(success_votes=str(success_votes)))
    print("Failed votes: {failed_votes}".format(failed_votes=str(fail_votes)))


# Entry point
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print e.message + "\nProgram will exit now..."
