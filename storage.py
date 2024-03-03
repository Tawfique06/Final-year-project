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
        Storage._file_name = file_name
        self.__active = False
        if os.path.exists(Storage._file_name):
            Storage._data = json.load(open(Storage._file_name))
        else:
            Storage._data = {}

    @property
    def active(self):
        return self.__active


    def new_user(self, *args):
        """Add new user which is also the current user"""
        new = {}
        if args:
            id = str(uuid4())
            for i, val in enumerate(*args):
                if i == 0:
                    new['sname'] = val
                if i == 1:
                    new['fname']= val
                if i == 2:
                    new['email'] = val
                if i == 3:
                    new['pnumber'] = val
                if i == 4:
                    new['password'] = val
            new['id']= id
            Storage._data[id]= new
            Storage._current_user = new
            self.__active = True
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
            return {}
        self.__active = True
        return Storage._current_user

    @property
    def get_url(self):
        """get image url"""
        if self.__active == False:
            return None
        self.__active = True
        return Storage._current_user.get('image_url')
        

    def get_user(self, email, password):
        "Get a particular user and set it as current user"
        if not email or not password:
            return ('Your name or password is null')
        for val in Storage._data.values():
            if val.get('email') == email and val.get('password') == password:
                Storage._current_user = val
                self.__active = True
                return Storage._current_user
        return None

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
    
    def logout(self):
        """Logout current user"""
        self.__active = False
        Storage._current_user = {}




if __name__ ==  "__main__":
    test = Storage("tests/test.json")
    print(test.new_user(['mus', 'mus', 'mus@ageestimator', '+2348056xxxx', 'passkey']))
    print(test.new_user(['Hammed', 'Taofeeq', 'tk@ageestimator', '+2348056xxxx', 'passkey']))
    print(test.save())
    auth = test.get_user('tk@ageestimator', 'passkey')
    id = auth.get('id')
    print(id)
    test.add_image_url(id, f'{id}.png')
    print(test.current_user)
    test.save()
    