#!/usr/bin/env python3
import requests
import json
import argparse
import calendar
import errno
import sys
import os
from datetime import datetime, timedelta

# Constants
API = 'https://slack.com/api'

# Settings
parser = argparse.ArgumentParser(description='Download/Delete files.')
parser.add_argument('token', help='API Token: see https://api.slack.com/web')
parser.add_argument('-o', '--out', default=".", help='Output folder')
parser.add_argument('--all', default=False, action='store_true', help='Download all of the organizations files?')
parser.add_argument('--download', default=False, action='store_true', help='Download files?')
parser.add_argument('--delete', default=False, action='store_true', help='Delete files?')
args = parser.parse_args()

if not (args.download or  args.delete):
    print("Must select at least one of --download or --delete")
    sys.exit(errno.EINVAL)

def download_file(url, out):
    try:
        os.stat(out)
    except:
        os.mkdir(out)

    local_filename = out + '/' + url.split('/')[-1]

    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename

def get_user_name(id):
    url = API+'/users.info'
    data = {'token': args.token, 'user': id }
    response = requests.post(url, data=data)
    return response.json()['user']['name']


def make_requester():
    list_url = API+'/files.list'

    if not args.all:
        auth_url = API+'/auth.test'
        data = {"token": args.token }
        response = requests.post(auth_url, data=data)
        user = response.json()["user"]
        user_id = response.json()["user_id"]

        def user_requester(page):
            print("Requesting files for %s (%s)" % (user, user_id))
            data = {'token':  args.token, 'user': user_id, 'page': page}
            response = requests.post(list_url, data=data)
            if response.status_code != requests.codes.ok:
                print('Error fetching file list')
                sys.exit(1)
            return response.json()

        return user_requester
    else:
        def all_requester(page):
            print('Requesting all files')
            data = {'token':  args.token, 'page': page}
            response = requests.post(list_url, data=data)
            if response.status_code != requests.codes.ok:
                print('Error fetching file list')
                sys.exit(1)
            return response.json()

        return all_requester


if __name__ == '__main__':
    page = 1
    users = dict()
    file_requester = make_requester()
    while True:
        json = file_requester(page)
        if not json['ok']:
            print('Error', json['error'])

        fileCount = len(json['files'])
        print('Found', fileCount, 'files')
        if fileCount == 0:
            break

        for f in json["files"]:
            user = users.get(f['user'], get_user_name(f['user']))

            if args.download:
                file_url = f["url_download"]
                print("Downloading file: '%s'" % file_url)
                download_file(file_url, args.out + '/' + user);

            if args.delete:
                print("Deleting file: '%s/%s'" % (user, f["name"]))
                data = { "token": args.token, "file": f["id"], "set_active": "true", "_attempts": "1"}
                timestamp = str(calendar.timegm(datetime.now().utctimetuple()))
                delete_url = API+'/files.delete?t='+timestamp
                requests.post(delete_url, data=data)

        page = page + 1
    print('Finished.')
