# About
This script is a hack for naukri.com apis https://www.naukri.com/. It updates the userprofile ('resume headline') at a random interval of 2 to 12 minutes 

# How it helps
Updating the naukri.com's profile continously moves it to the top, which means more recruiters will be able to see your profile and contacts you.

# How to use
Python 3.6 has to installed.

You have 4 options to input username and password
You can select either one:

1. Hardcode your username and password on the top of the script:
    ```
     hard_user_name= 'your_username'
     hard_pass_word= 'your_password'
     ```
     
2. Or make a text file `'user_data.txt'` in the same directory and add your username and password in that.
3. Or run the script and input username and password on the prompt.
4. Or you can pass the argument like : 
    ```
    python naukri.py your_username your_password
    ```
Suggestions: Most preferable way must have to be adding 'user_data.txt' file and storing your username and password over there. And then simply run : 
    ```
    python naukri.py
    ```
    
Voila your are done. Until the script is running and connected to internet it will update your profile.

Make sure you're connected to internet and run the script :


```
python naukri.py
```
