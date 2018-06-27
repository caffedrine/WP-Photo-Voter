import struct
import socket
import requests


def print_request(req):
    print('HTTP/1.1 {method} {url}\n{headers}\n\n{body}'.format(
        method=req.method,
        url=req.url,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        body=req.body,
    ))


def print_response(res):
    print('HTTP/1.1 {status_code}\n{headers}\n\n{body}\n\n{cookies}'.format(
        status_code=res.status_code,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
        body=res.content,
        cookies='\n'.join('{}: {}'.format(k, v) for k, v in res.cookies.items()),
    ))


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_proxy_type(proxy, attempts = 1):
    # Possible types returned: SOCKS4, SOCKS5, HTTP, HTTPS, DEAD
    ip = proxy.split(':')[0]
    port = proxy.split(':')[1]

    test_url = "http://checkip.dyndns.com"
    keyword = ip

    timeout = 15
    err_description = ""

    for i in range(attempts):
        # SOCKS5
        try:
            proxy_tuple = {"https": "{proxy_type}://{ip_port}".format(proxy_type="socks5", ip_port=proxy),
                           "http": "{proxy_type}://{ip_port}".format(proxy_type="socks5", ip_port=proxy)}
            response = requests.get(test_url, proxies=proxy_tuple, timeout=timeout)
            if response.content.__contains__(keyword):
                return "SOCKS5"
        except Exception as e:
            err_description = e.message

        # SOCKS4
        try:
            proxy_tuple = {"https": "{proxy_type}://{ip_port}".format(proxy_type="socks4", ip_port=proxy),
                           "http": "{proxy_type}://{ip_port}".format(proxy_type="socks4", ip_port=proxy)}
            response = requests.get(test_url, proxies=proxy_tuple, timeout=timeout)
            if response.content.__contains__(keyword):
                return "SOCKS4"
        except Exception as e:
            err_description = e.message

        # HTTP proxy
        try:
            proxy_tuple = {"https": "{proxy_type}://{ip_port}".format(proxy_type="http", ip_port=proxy),
                           "http": "{proxy_type}://{ip_port}".format(proxy_type="http", ip_port=proxy)}
            response = requests.get(test_url, proxies=proxy_tuple, timeout=timeout)
            if response.content.__contains__(keyword):
                return "HTTP"
        except Exception as e:
            err_description = e.message

        # HTTPS proxy
        try:
            proxy_tuple = {"https": "{proxy_type}://{ip_port}".format(proxy_type="https", ip_port=proxy),
                           "http": "{proxy_type}://{ip_port}".format(proxy_type="https", ip_port=proxy)}
            response = requests.get(test_url, proxies=proxy_tuple, timeout=timeout)
            if response.content.__contains__(keyword):
                return "HTTPS"
        except Exception as e:
            err_description = e.message

    return "DEAD"
