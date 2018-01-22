import re
import time
from datetime import datetime
import os
import random
import sys
try:
    import requests
except ModuleNotFoundError:
    print('Trying to install requests module\n')
    os.system('pip3 install requests')
finally:
    import requests

#Hardcode the username and password here:
hard_user_name = ''
hard_pass_word = ''

class Naukri:
    validated = False
    def __init__(self):
        """ Initialize

        Initializes the class.
        """
        self.base_url = 'https://www.nma.mobi'
        self.header = {'Content-Type': 'application/json; charset=utf-8',
                       'clientId': 'ndr01d',
                       'deviceId': self.gen_random_id(),
                       'AppVersion': '71',
                       'Accept': 'application/json',
                       'Accept - Encoding': 'gzip',
                       'Accept - Charset': 'UTF - 8'
                       }
        self.session = self.get_session()

    def get_session(self):
        """ Session

        Create a session for GET or POST.
        """
        session = requests.Session()
        return session

    def gen_random_id(self):
        return ''.join(random.choice('0123456789abcdef') for _ in range(16))

    def post_login(self, userName, passWord):
        """ Post Login Call

        Sign in to the server
        """
        url =  self.base_url + '/login/v2/login'
        json_data = {"USERNAME":userName,"ISLOGINBYEMAIL":"1","PASSWORD":passWord}

        login_response = self.session.post(url, json=json_data, headers=self.header)

        return login_response

    def get_dashboard(self):
        """ Get Dashboard

        Get the user details
        """
        url = self.base_url + '/mnj/v3/dashBoard?properties=profile(isPushdownAvailable)'

        dash_response = self.session.get(url, headers=self.header)
        self.profile_id = dash_response.json().get('dashBoard').get('profileId')

    def get_profile(self):
        """ Get Profile

        Get the user Profile
        """
        url = self.base_url + '/mnj/v2/user/profiles?&expand_level=2&active=1'

        profile_response = self.session.get(url, headers=self.header)
        return profile_response

    def update_profile(self, json_data):
        """ Update Profile

        Updates the user Profile
        """
        url = self.base_url + '/mnj/v1/user/profiles/' + self.profile_id + '/'

        self.session.post(url, json=json_data, headers=self.header)

    def valLogin(self, userName, passWord):
        """Validates Login Session

        Validates that login was successful
        """
        print('Validating your Credentials.........\n')
        print('Entered Username : ' + userName)
        print('Entered Password : {0}*****{1}'.format(passWord[:2], passWord[len(passWord)-2:]))
        login_response = self.post_login(userName, passWord)
        if login_response.json().get('error'):
            print(', '.join(list(self.find('message',login_response.json()))))
            self.validated = False
            return False

        else:
            self.validated = True
            self.header['Authorization'] = 'NAUKRIAUTH id=' + login_response.json().get('id')
            print('You are Successfully Logged in')
            self.get_dashboard()
            return True

    def find(self, key, dictionary):
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in self.find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in self.find(key, d):
                        yield result

####################################################################################################################################


def input_user_data():
    users_name = ''
    while(True):
        if not clean_username(users_name):
            users_name = input('\nEnter your registered email of naukri.com:\n')
        else:
            user_password = clean_password(input('Enter the Password\n'))
            if user_password:
                break

        print('--'*40)

    return users_name, user_password


def nested_dict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            nested_dict(v)
        else:
            print("{0} : {1}".format(k, v))


def clean_username(username):
    if username:
        validation = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")
        if validation.match(username.strip()):
            return username.strip()

        else:
            print('Invalid Username')
            print("Must contains valid email id like : your_email@domain.extention\n")
            print('--' * 40)


def clean_password(password):
    if password:
        return password.strip()
    else:
        print('Password cannot be blank')


def clean_data(username, password):
    return clean_username(username), clean_password(password)


def file_exists():
    try:
        with open('user_data.txt', 'r') as data:
            print('Found user_data.txt file')
            username, password = data.readlines()
            return username, password

    except FileNotFoundError:
        pass

    except ValueError:
        print('File does not have valid data')
        print('First line must contain username and second line password like:')
        print('''
        your_email@domain.extention
        your_password
        ''')

def user_data():
    #hardcode your username and password
    username = hard_user_name
    password = hard_pass_word

    #Or your can make a file name user_data.txt and add username and password in it.
    #Username must be email id
    #And it should come at first line
    #and password on the second line
    if os.path.isfile('user_data.txt'):
        try:
            username, password = file_exists()
        except TypeError:
            pass

    if clean_username(username) and clean_password(password):
        return clean_username(username), clean_password(password)


def main():
    naukri = Naukri()

    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            print('Password cannot be blank\n')
            user_info = sys.argv[1], input('Enter the password\n')
        else:
            user_info = sys.argv[1], sys.argv[2]
    else:
        user_info = user_data()

    if not user_info or not naukri.valLogin(*user_info):
        while True:
            user_info = input_user_data()
            if naukri.valLogin(*user_info):
                break

    #Validates and update the data.
    if naukri.validated:

        pro_dic = naukri.get_profile().json()
        find_value = list(naukri.find('resumeHeadline',pro_dic))[0]
        while True:
            print('updating...')
            naukri.update_profile({'resumeHeadline': find_value})
            print('updated at '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            time.sleep(random.randint(120,750))


if __name__ == '__main__':
    main()
