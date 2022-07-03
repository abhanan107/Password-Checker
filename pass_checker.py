import requests
import hashlib
import sys


def get_api_response(qry_pass):
    url = 'https://api.pwnedpasswords.com/range/' + qry_pass
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error while fetching api data : response code {res.status_code}')
    return res


def get_pass_count(hashes, hash_check):
    hashes_list = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes_list:
        if h == hash_check:
            return count
    return 0


def pawned_api_check(passwd):
    hash_pass = hashlib.sha1(passwd.encode('UTF-8')).hexdigest().upper()
    pass_p1, pass_p2 = hash_pass[:5], hash_pass[5:]
    res = get_api_response(pass_p1)
    return get_pass_count(res, pass_p2)


def main_func(argv):
    for passwd in argv:
        count = int(pawned_api_check(passwd))
        if count > 0:
            print(f'This Password : {passwd} has been pawned {count} times')
        else:
            print(f'This Password : {passwd} is not pawned good to go')


if __name__ == '__main__':
    inputs = sys.argv[1:]
    main_func(inputs)
