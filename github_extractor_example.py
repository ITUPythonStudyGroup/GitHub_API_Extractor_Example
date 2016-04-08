## Import modules
import requests, json

## Define the basic terms
TOKEN = ''
SRC = 'https://api.github.com/search/repositories?q='
USR = 'https://api.github.com/users/'

## Welcome
print('Welcome to the GitHub Search API Extractor', '\n')

##########################################################
### Step 1. Define the search term for the GitHub API  ###
##########################################################

## Define the search terms
TERM = input('Please enter your search term. Use a plus sign to separate words. \n')

## Generate the Search API URL
URL = '%s%s' % (SRC, TERM)

## Determine the number of pages per 100 repos
response = requests.get(URL).json()
total = response['total_count']
print('Number of results for the search term:', total, '\n')
n = total // 100 + 2

#############################################################
### Step 2. Get the data and store it in your dictionary  ###
#############################################################

## Create an empty dictionary if there is no previous dictionary
try:
    repositories
except NameError:
    repositories = {}

## Print the number of results already in the dictionary
target = total + len(repositories)

## Call each pages with a 100 repos (search result page)
if total > 1000:
    print ('Warning: the Search API limit is 1000 results for authenticated users. '
                  'Try to be more specific.\n')
else:
    for x in range(1, n):
        par = {'page': x, 'per_page': 100}
        head = {'Authorization': 'token %s' % TOKEN}
        response = requests.get(URL, params=par, headers=head).json()
        for item in response['items']:
            repositories[item['id']] = {
                'name': item['name'],
                'language': item['language'],
                'username': item['owner']['login']
            }

##############################################
### Step 3. Look for data collection error ###
##############################################

## Check if you have all the new results in your dictionary
print('****************************************')
print('Results in dictionary:', len(repositories))
print('Target result:', target)
print('****************************************\n')
if len(repositories) != target:
    print('There might have been an error in getting the new results.')
else:
    print('Great, you have all the new results in your dictionary.')

#######################################
### Step 4. Collect additional data ###
#######################################

## Get extra information for each user
for repository in repositories:
    head = {'Authorization': 'token %s' % TOKEN}
    username = repositories[repository]['username']
    URL = '%s%s' % (USR, username)
    user = requests.get(URL, headers=head).json()
    repositories[repository]['repos'] = user['public_repos']

print('User information has been added to your dictionary. Thanks for using the GitHub API Extractor.')

'''
If you want to continue working with your data later or you need to load it to a program to analyze it,
use the code below.

## Export your data
with open('repository_example.json', 'w') as outfile:
    json.dump(repositories, outfile)

## This is how you load your data if you want to continue working with it
with open('repository_example.json') as infile:
    repositories = json.load(infile)

## This is how you can export the data from your dictionary to a CSV file
import csv
writer = csv.writer(open('repository_example.csv', 'w'))
for key, value in repositories.items():
   writer.writerow(value.values())
'''
