# HaveIBeenpwned_Python
General POC to check about if EMail is pawned.

# Requirements
Python 2.7.xx

Google Chrome and it's matching chromedriver.exe inside C:\Python27; folder

pip install -r HaveIBeenpwned_Python/requirements.txt

# How to run
1. Open emaildata.csv under src folder and fill in all the email ID's that needs to be validated in first column accordingly.

2. Open command prompt from same src folder and run "python HaveIBeenPawnd.py conf.ini" 

3. After Execution ends then simply launch emaildata.csv and verify respective outputs.

(OR)

If simply single EMail needs to be checked then

Go to src folder and open command prompt and run

"python HaveIBeenPawnd.py conf.ini someothersemailid@emailtest.com"

This will simply print result on console if email is pawned or not.

(OR)

HaveIBeenpwned_Python can also be imported as library and use validate_single_pawn with email as parameter. 

Project can further be modified upto implementation using headless-chrome as well.
