#!/usr/bin/python3
"""Store user information in a json file"""
import os
import json
from uuid import uuid4

class Storage:
    """The storage class"""

    _file_name = 'storage.json'
    _data = {}
    _current_user = {}

    def __init__(self, file_name='storage.json'):
        """The initializaton"""
        if file_name:
             Storage._file_name = file_name
        if os.path.exists(Storage._file_name):
            Storage._data = json.load(open(Storage._file_name))
        else:
            Storage._data = {}

    def new_user(self, *args):
        """Add new user which is also the current user"""
        new = {}
        if args:
            id = str(uuid4())
            for i, val in enumerate(*args):
                if i == 0:
                    new['sname'] = val
                if i == 1:
                    new['fname ']= val
                if i == 2:
                    new['email'] = val
                if i == 3:
                    new['pnumber'] = val
                if i == 4:
                    new['password'] = val
            new['id']= id
            Storage._data[id]= new
            Storage._current_user = new
            return Storage._current_user

    def save(self):
        """save the updated record in the file"""
        with open(Storage._file_name, 'w') as data:
            json.dump(Storage._data, data)
        return (Storage._data)

    @property
    def current_user(self):
        """Get current user"""
        if len(Storage._current_user.keys()) == 0:
            return None
        return Storage._current_user

    def get_user(self, email, password):
        "Get a particular user and set it as current user"
        if not email or not password:
            return ('Your name or password is null')
        for val in Storage._data.values():
            if val.get('email') == email and val.get('password') == password:
                Storage._current_user = val
                return Storage._current_user
        return ('No such user')

    def add_image_url(self, idx, url):
        """add the image url of the user"""
        if not idx or not url:
            return "the id or url is null"
        if idx in Storage._data.keys():
            Storage._current_user['image_url'] = url
            Storage._data[idx] = Storage._current_user
            return Storage._current_user
        else:
            return "No such user"


if __name__ ==  "__main__":
    test = Storage("test.json")
    print(test.new_user(['mus', 'mus', 'mus@ageestimator', '+2348056xxxx', 'passkey']))
    print(test.new_user(['Hammed', 'Taofeeq', 'tk@ageestimator', '+2348056xxxx', 'passkey']))
    print(test.save())
    auth = test.get_user('tk@ageestimator', 'passkey')
    id = auth.get('id')
    print(id)
    test.add_image_url(id, f'{id}.png')
    print(test.current_user)
    test.save()
    