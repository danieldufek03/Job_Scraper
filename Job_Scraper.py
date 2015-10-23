'''
Created on Apr 30, 2015

@author: Daniel
This is my very first python program.
'''
#! python3
# request.py - Opens several Craigslist jobs and returns the ones that pay over a threshhold

import requests, sys, webbrowser, bs4
import re, os

minPay = 10 #minumum pay rate you would like returned
maxPay = 70 #establish a maximum to weed out the fake jobs claiming to pay 5grand a week etc...
print('Searching Part Time Jobs...') # display text while downloading the Craigslist page
craigslist = requests.get('http://norfolk.craigslist.org/search/jjj?is_parttime=1') #pulls a page from the web and stores it in res
craigslist.raise_for_status() #checks to make sure site was accessed successfully


clSoup = bs4.BeautifulSoup(craigslist.text) #assigns the html to a beautifulsoup object
outputFile = open('craigslist.txt', 'w')


linkElems = clSoup.select('.pl a') #selects the pl <a> tags associated with the pl class

#print(len(linkElems), 'Jobs')

#print(str(linkElems[0]) + '\n')

for i in range(50):
    #webbrowser.open('http://norfolk.craigslist.org/' + linkElems[i].get('href'))
    jobs = requests.get('http://norfolk.craigslist.org/' + linkElems[i].get('href')) #go into all the links extracted
    jobs.raise_for_status()
    jobSoup = bs4.BeautifulSoup(jobs.text)
    title = jobSoup.select('.postingtitletext') #extracts the titles from the class postingtitletext
    pay = jobSoup.select('.bigattr b') #extracts the pay portion of page
    paystring = pay[0].text #converts the soup to an array of strings
    payint = re.findall(r'\b\d+\b',paystring) #parses the string to only contain #s  #RegEx??
    payint = [int(i) for i in payint] #converts from strings to ints  
    #prints the payrate for each job 
    #filters the jobs by their payrate
    if any(x > minPay for x in payint) and all(x < maxPay for x in payint): #trying to sort by payrate .. not working
        #try catch because the unicode error breaks the program
        try:
            print(title[0].text)
            outputFile.write(title[0].text + '\n')
        except UnicodeError:
            print("Could not output unicode error")
            outputFile.write("Could not output unicode error")
        print(paystring)
        outputFile.write(paystring + '\n')
        #prints the url of each job
        print('http://norfolk.craigslist.org/' + linkElems[i].get('href') +'\n')
        outputFile.write('http://norfolk.craigslist.org/' + linkElems[i].get('href') +'\n\n')
        webbrowser.open('http://norfolk.craigslist.org/' + linkElems[i].get('href')) #opens all of the jobs in the browser
