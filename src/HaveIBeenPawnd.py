import ConfigParser,os,csv
from validate_email import validate_email

from selenium import webdriver
import time
import pandas as pd
import sys

class HIBPawned(object):
    """ 
    This is a class for validating if EMail ID(s) are pawned.
    Website to be used is https://haveibeenpwned.com/
    Author: Pawankumar Dubey
    """
    
    def __init__(self, configFile):
        """ 
        The constructor for HIBPawned class. 
        Basic purpose of ini files are to minimize harcoding and mainain static data.
        
        Parameters: 
           Configuration Ini (String): File to hold all information about runtime data requirements. 
        """
        print('#'*80)
        print("Initialization HIBPawned ", configFile)
        self.driver = webdriver.Chrome()
        configFilePath = os.path.join(os.getcwd(),configFile)
        self.configParser = ConfigParser.RawConfigParser()
        self.configParser.read(configFilePath)
        self.passed = self.configParser.get('commons', 'pass')
        self.failed = self.configParser.get('commons', 'fail')
        self.csvpath = self.configParser.get('commons', 'csvpath')
        self.driver.get(self.configParser.get('website', 'link'))
        self.title = self.configParser.get('website', 'title')
        self.sleep = int(self.configParser.get('commons', 'sleep'))
        self.emails_lst = []
        self.df = pd.read_csv(self.csvpath)
        with open(self.csvpath,'rt')as f:
            data = csv.reader(f)
            for x,email in enumerate(data):
                if x > 0:
                    self.emails_lst.append(email)
        
        self.account = self.configParser.get('website', 'input_txt')
        self.submit_btn = self.configParser.get('website', 'submit_btn')
        self.pwnCount = self.configParser.get('website', 'pwnCount')
        self.expect_Ret = self.configParser.get('website', 'ret_val')
        
        self.pwned_not_found = self.configParser.get('website', 'pwned_not_found')
        self.pwned_not_found_txt = self.configParser.get('website', 'pwned_not_found_txt')
        self.pwned_found = self.configParser.get('website', 'pwned_found')
        self.pwned_found_txt = self.configParser.get('website', 'pwned_found_txt')
        
    def validate_all_pawns(self):
        """ 
        The function Loops over EMail list and calls validate_single_pawn with single EMail ID's
        Updates Panda Dataframe against matchin Email ID and move Data frame to CSV file.
        """
        
        print('\n'*1)
        print('#'*80)
        print("InIt validate_all_pawns Method")
        print(self.driver.title)
        assert self.title in self.driver.title
        print(self.df)        
        for idx,email in enumerate(self.emails_lst):
            ret = self.validate_single_pawn(email[0])
            if type(ret) == tuple and len(ret) == 3:
                status=ret[1]
                detail=ret[2]
                #print("tuples -- > ",status,detail)
                self.df.loc[self.df["Email_ID"]==email[0], "IS_PAWN"] = status
                self.df.loc[self.df["Email_ID"]==email[0], "Detail"] = detail
            else:
                print("Unknown Data ", ret)
        self.df.to_csv(self.csvpath, index=False)
        self.driver.close()
    
    def validate_single_pawn(self,email):
        """ 
        Method is independent to run email ids on HaveIbeenPawned.com and return its data back as Tuple
  
        Parameters: 
            email (String): EMail Id to be looked up for pawn. 
          
        Returns: 
            Tuple: A Tuple with EMail ID, Status and Description. 
        """
        if validate_email(email):
            print('\n'*1)
            print('#'*80)
            print("Email Id is Valid --> ", email)
            self.driver.find_element_by_id(self.account).clear()
            elem = self.driver.find_element_by_id(self.account)
            elem.send_keys(email)
            time.sleep(self.sleep)
            elem = self.driver.find_element_by_id(self.submit_btn)
            elem.click()
            time.sleep(self.sleep)         
            '''
            Here; 
            if self.driver.find_element_by_xpath(self.pwned_found).is_displayed()
            searches for //h2[contains(text(),'pwned!')] --> We get this with chrome chropath
            If this is found that means Account has been compromised
            Below : self.driver.find_element_by_xpath(self.pwned_found_txt).text uses
            //p[@id='pwnCount'] to get text for reference
            failed data variable has static data as Oops; Email is pawned
            '''       
            if self.driver.find_element_by_xpath(self.pwned_found).is_displayed() == True:
                print(self.failed) 
                print(self.driver.find_element_by_xpath(self.pwned_found_txt).text)
                return (email,self.failed,str(self.driver.find_element_by_xpath(self.pwned_found_txt).text))
            
            '''
            Here; 
            self.driver.find_element_by_xpath(self.pwned_not_found).is_displayed()
            searches for //h2[contains(text(),'no pwnage found!')] --> We get this with chrome chropath
            If this is found that means Account has not been compromised
            Below : self.driver.find_element_by_xpath(self.pwned_not_found_txt).text uses
            //p[contains(text(),'No')] to get text for reference
            passed data variable has static data as Great; Email is not pawned
            ''' 
            if self.driver.find_element_by_xpath(self.pwned_not_found).is_displayed() == True:
                print(self.passed) 
                print(self.driver.find_element_by_xpath(self.pwned_not_found_txt).text)
                return (email,self.passed,str(self.driver.find_element_by_xpath(self.pwned_not_found_txt).text))
        else:
            print('#'*80)
            print("EMail Id is not valid ", email)
            return "Not a Valid Email_ID"
            
if __name__== "__main__":
    """ 
    Main Entry point for the execution
    """
    print('#'*80)
    print(sys.argv)
    print(len(sys.argv))
    
    if len(sys.argv) == 2:
        print('#'*80)
        print(str(sys.argv[1]))
        conf_ini = str(sys.argv[1])
        HIBPawned(conf_ini).validate_all_pawns()
    elif len(sys.argv) == 3:
        print('='*80)
        print(str(sys.argv[1]) , str(sys.argv[2]))
        conf_ini = str(sys.argv[1])
        email_id = str(sys.argv[2])
        HIBPawned(conf_ini).validate_single_pawn(email_id)
    else:
        print("Acceptable Arguments are only 1. Configuration(InI file) and/or 2. EMail ID ", len(sys.argv))