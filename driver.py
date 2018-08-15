import sys
import os
import re
import subprocess

def currentDefaultRedirectPage(redirect_php):
    indexRequire = len(redirect_php)-2
    #print(indexRequire)
    stringToSplit = redirect_php[indexRequire]
    #print(stringToSplit)
    defaultRedirect = ""
    for i in range (9, len(stringToSplit)-4):
        defaultRedirect = defaultRedirect+stringToSplit[i]  
    #print(defaultRedirect)
    return defaultRedirect

def parseRedirect_php():
    redirect_php = [];
    with open('./tmp/redirect.php.temp') as fin:
        for line in fin:
            redirect_php.append(line)
    return redirect_php

def parseHosts():
    hosts = [];
    hosts.append([])
    hosts.append([])
    #print(hosts)
    with open('./tmp/hosts.temp') as fin:
        for line in fin:
            fields = line.split()
            hosts[0].append(fields[0])
            hosts[1].append(fields[1])
            pointsToIp = fields[0]
            url = fields[1]
            #print(url+" points to ip address: "+pointsToIp)
    #print(hosts)
    return hosts


def viewRedirects(currentRedirects):
    print "\n---Current DNS Redirects---\n"
    col1= currentRedirects[0]
    col2= currentRedirects[1]
    for c1, c2 in zip(col1, col2):
            print "%-11s <--- %s" % (c1, c2)
    print "\n\n"
    return

def mainMenu():
    print "Please Select An option from the menu:"
    print "     1) Add New DNS Redirect"
    #print "     2) Remove a Redirect(s)"
    print "     2) View Current DNS Redirect(s)"
    #print "     4) Edit A DNS Redirect"
    #print "     5) Change Default Redirect"
    #print "     6) View Modifications"
    print "     3) Save Changes"
    print "     4) Quit DNS"
    return raw_input();

def addRedirect(defaultRedirectPage, defaultHosts):
    print "\n---Adding New DNS Redirect---\n"
    print("**Note** Leaving options 2 and 3 blank below will default to 172.16.42.1 and the Default Redirect Page specified in Main Menu Option 5.  Press <Enter> when prompted for default behavior\n")
    urlEntered = False
    newURL = ""
    while(urlEntered == False):
        newURL = raw_input("1) Please enter the url of the (http) site you would like to redirect: ")
        if(newURL == ""):
            print("\n Please enter a valid url\n")
        else:
            urlEntered = True
    newIPRedirect = raw_input("\n2) Please enter the ip address you would like this site to redirect to: ")
    newRedirectToPage = ""
    newRedirectPage_php = []
    if (newIPRedirect == ""):
        newIPRedirect = "172.16.42.1"
    if (newIPRedirect == "172.16.42.1"):
        foundFile = False 
        while(foundFile == False):
            newRedirectToPage = raw_input("\nPlease enter the .html page in the Pineapple's /www folder you would like this site to load: ")  
            if((os.path.isfile("/www/"+newRedirectToPage)) or (newRedirectToPage == "")):
                foundFile = True 
            else:
                print("Couldn't find "+newRedirectToPage+" in /www/")
                print("Please enter a valid .html file in /www/\n")
        #build redirect.php if entered non-default behavior
        if(newRedirectToPage != ""):
            phpRedirect = "if ($ref == \""+newURL+"\")  { header('Location: "+newRedirectToPage+"'); }\n"
            for i in range(0, len(defaultRedirectPage)):
                if(i == len(defaultRedirectPage)-2):
                    newRedirectPage_php.append(phpRedirect)
                    newRedirectPage_php.append(defaultRedirectPage[i])
                else: 
                    newRedirectPage_php.append(defaultRedirectPage[i])

        f=open("./tmp/redirect.php.temp", "w+")
        for i in range(0, len(newRedirectPage_php)):
            f.write(newRedirectPage_php[i])
        f.close()
        #print("\n\nOld redirect.php page: \n")
        #print(defaultRedirectPage)
        #print("\n\nNew redirect.php page: \n")
        #print(newRedirectPage_php) 
      
    f_hosts=open("./tmp/hosts.temp", "a")
    newEntry=newIPRedirect+"\t"+newURL+"\n"
    f_hosts.write(newEntry)
    f_hosts.close()
    return

def viewModifications():
    print("---View Modifications---")

def saveChanges():
    print("You have sucessfully saved your changes")

def main():
	#subprocess.call("./scripts/getRedirectFiles.sh", shell=True)
	print "\nWelcome to Shan's DNS Spoof Module for the Pineapple Tetra.\n\n"
	currentHosts = parseHosts();
	redirectPHP = parseRedirect_php();
	defaultRedirectPage = currentDefaultRedirectPage(redirectPHP);


	mmOption = mainMenu();
	while(True):
		if mmOption == "1":
            		addRedirect(redirectPHP, currentHosts)
			currentHosts=parseHosts()
			redirectPHP=parseRedirect_php()
			mmOption = mainMenu();
		elif mmOption == "2":
            		viewRedirects(currentHosts)
            		mmOption = mainMenu();
		elif mmOption == "3":
			#subprocess.call("./scripts/save.sh", shell=True)
            		saveChanges()
		elif mmOption == "4":
            		print "\n\nThanks for using my DNS Spoof Module for the Pineapple Tetra.\n\n"
            		sys.exit(0)
		else:
            		print "\nPlease enter a valid menu option...\n\n"
            		mmOption = mainMenu();

if __name__ == "__main__": main()
