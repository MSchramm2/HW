# -*- coding: utf-8 -*-
"""
Created on Wed May  4 00:21:55 2022

@author: Meg
"""

#%% imports

import pandas as pd
import irc_parse
import nltk
from nltk.corpus import words

#%% read in data

raw_log = []
with open('hackers.log', 'r', errors='ignore') as log_file:
    raw_log = log_file.readlines()

#%% create dataframe

hackers = pd.DataFrame(raw_log, columns=['original_data'])


#%% use the is_date_row function to
# check if a row is actually a date.

hackers['is_date_row'] = hackers['original_data'].apply(irc_parse.is_date_row)

#%%apply the is_messgae function 

hackers['is_message'] = hackers['original_data'].apply(irc_parse.is_message)

#%% save data to cleaner

hackers.to_csv('hackers_clean.csv')

#%% (1.1) Which users posted the most messages (2pts)?

most_users = {}
for row in hackers['original_data']:
    if irc_parse.is_message(row):
        username = irc_parse.get_user_name(row)
        if username in most_users.keys():
            most_users[username] = most_users.get(username) + 1
        else:
            most_users[username] = 1
max = 0
max_user = ''
for key in most_users.keys():
    if most_users.get(key) > max:
        max = most_users.get(key)
        max_user = key
        
print (max_user)

#%% (1.2) Which users logged in the greatest number of times? (2pts)
##print out all usernames to find the line that is causing issues

logged_users = {}
for row in hackers['original_data']:
    if irc_parse.get_join_quit_type(row) == 'join':
        username = irc_parse.get_join_quit_username(row) ##error
        print(username)
        if username in logged_users.keys():
            logged_users[username] = logged_users.get(username) + 1
        else:
            logged_users[username] = 1
        
max = 0
max_user = ''
for key in logged_users.keys():
    if logged_users.get(key) > max:
        max = logged_users.get(key)
        max_user = key
    
print (max_user)

#%% (1.3) Which users spent the most time in the chat? (3pts)



#%% (1.4) Who are the administrators (username begins with @) (1pt).
admins = []
for row in hackers['original_data']:
    if irc_parse.is_message(row):
        username = irc_parse.get_user_name(row)
        if irc_parse.get_user_prefix(username) == "@":
            if not(username in admins):
                logged_users.append(username)

print(admins) ##error

#%% (2.1) Count the total number of written messages (only those with actual text content) (1 pts).

len(hackers.loc[hackers['is_message']==True])
print(len(hackers.loc[hackers['is_message']==True]))

#%% (2.2) Find the most common words (only include message content) (2 pts)

words = {}

for row in hackers['original_data']:
    if irc_parse.is_message(row):
        message = irc_parse.get_chat_message(row).split()
        for word in message:
            if word in words.keys():
                words[word] = words.get(word) + 1
            else:
                words[word] = 1
                
max = 0
max_word = ''
for key in words.keys():
    if words.get(key) > max:
        max = words.get(key)
        max_word = key
        
print (max_word)
        

#%% (2.3) Find and rank (by count) words not in an English dictionary (2 pts). 
          #This is a simple method that can identify some names of malware tools.
nltk.download('words')
non_words = {}

for word in words.keys(): 
    if not(word in words.words()): 
        if word in non_words.keys():
            non_words[word] = non_words.get(word) + 1
        else:
            non_words[word] = 1

max = 0
max_word = ''
for key in non_words.keys():
    if non_words.get(key) > max:
        max = non_words.get(key)
        max_word = key
        
print (max_word)

#%% (2.4) How many distinct URLs were posted in the chat? (1 pt)
##works

urls_list = []

for row in hackers['original_data']:
    if irc_parse.is_message(row):
        urls = irc_parse.find_urls(irc_parse.get_chat_message(row))
        for url in urls:
            if not(url in urls_list):
                urls_list.append(url)
                
print(len(urls_list))

#%% (2.5) Which URLs were posted the most (top 5)? (1 pt)
##done
url_dict = {}

for row in hackers['original_data']:
    if irc_parse.is_message(row):
        urls = irc_parse.find_urls(irc_parse.get_chat_message(row))
        for url in urls:
            if url in url_dict.keys():
                url_dict[url] = url_dict.get(url) + 1
            else:
                url_dict[url] = 1

url_dict = {k: v for k, v in sorted(url_dict.items(), key=lambda item: item[1])}
url_list = list(url_dict)[0:5]
print(url_list)
#%% (2.6) Which domains (e.g. github.com/ or youtube.com) were shared the most.
##doesnt work
domains = {}

for url in urls_list:
    sub_domains = url.split('.')
    domain_name = sub_domains[0] + '.'# + sub_domains[1]
    if domain_name in domains:
        domains[domain_name] = domains.get(domain_name) + 1
    else:
        domains[domain_name] = 1

max_user = 0
max_domain = ''
for key in domains.keys():
    print(domains.get(key))
    if domains.get(key) > max_user:
        max_user = non_words.get(key)
        max_domain = key
        
print (max_domain)
#%% (2.7) Generate a list of sites on the Dark Web (sites ending in .onion) (1pt)
## doesnt work
dark_list = []

for url in urls_list:
    sub_domains = url.split(',')
    if 'onion' in sub_domains:
        dark_list.append(url)
        
print(dark_list)
#%% (3.1) Which hours of the day had the most messages (1 pt)?


#%% (3.2) Which days had the most messages (top 10 days) (2pts)?


#%% (3.3) Rank the days of the week by average message count