import os
import time
from datetime import datetime
from typing import List, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

USER_NAME = os.getenv("USER_NAME")
BASE_URI = os.getenv("BASE_URI")
API_TOKEN = os.getenv("API_TOKEN")
TITLE_TEMPLATE = os.getenv("TITLE_TEMPLATE")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL"))


def jellyfin(path, method='get', **kwargs):
    return getattr(requests, method)(
        f'{BASE_URI}/{path}',
        headers={'X-MediaBrowser-Token': API_TOKEN},
        **kwargs
    )


users = jellyfin('Users').json()  # type: List[dict]
users_name_mapping = {user.get('Name'): user for user in users}  # type: Dict[str, dict]
user_id = users_name_mapping.get(USER_NAME).get('Id')


def scan(FOLDER_ID=None, callback=None, parent_item=None):
    resp = jellyfin(f'Users/{user_id}/Items', params=dict(
        Fields='Path', ParentId=FOLDER_ID
    )).json()  # type: dict
    items = resp.get('Items')
    for index, item in enumerate(sorted(items, key=lambda x: x.get('Path')), start=1):
        item: dict
        if item.get('IsFolder'):
            if item.get('Type') == 'ManualPlaylistsFolder':
                continue
            print(datetime.now(), '- scanning:', item.get('Name'))
            scan(item.get('Id'), callback, parent_item=item)
        else:
            item = jellyfin(f'Users/{user_id}/Items/{item.get("Id")}').json()  # type: dict
            if callback:
                callback(item, parent_item, item_index=index)


def retitle(item: dict, parent_item: dict, item_index: int):
    parent_id = parent_item.get('Id')
    parent_name = parent_item.get('Name')

    item_id = item.get('Id')
    item_name = item.get('Name')
    item_path = item.get('Path')
    item_filename = os.path.basename(item_path)  # type: str
    [item_filename, item_ext] = os.path.splitext(item_filename)
    item_filename_without_ext = item_filename.removesuffix(item_ext)

    if not TITLE_TEMPLATE:
        fix_name = item_filename_without_ext
    else:
        fix_name = TITLE_TEMPLATE % locals()

    if item_name != fix_name:
        item.update(Name=fix_name)
        jellyfin(f'Items/{item_id}', json=item, method='post')
        print(datetime.now(), '- changed:', f'{item_name} -> {fix_name}')


try:
    while True:
        scan(callback=retitle)
        time.sleep(SCAN_INTERVAL)
except KeyboardInterrupt:
    pass
