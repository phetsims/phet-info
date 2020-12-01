#!/bin/bash

# update-repos-list.sh
#
#  This script creates a file in this directly called `.repos` that is
#  a newline separated list of all repos in the phetsims organization.

# temporarily store the old repos for troubleshooting if problems arise
mv .repos .repos.old

# binDir is the name of the current directory
binDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# this gets the credentials used for github api authentication
creds=`node ${binDir}/printGithubAuthorization.js`

# Get the collection of repos in json format
curl -is -u "$creds" https://api.github.com/orgs/phetsims/repos -o .response

# A regex to extract the page number from the api response
pageExtractor='s/.*page=\([0-9]\).*/\1/g'

# next
nextPage=`cat .response | grep Link: | awk '{print $2}' | sed ${pageExtractor}`
# last
lastPage=`cat .response | grep Link: | awk '{print $4}' | sed ${pageExtractor}`

# A regex to extract the name of the repository from the json objects
nameExtractor='s/"\([a-zA-Z0-9-]*\)",/\1/'
nameMatcher="^\ \ \ \ \"name\""

# Add repos to list for the current page
cat .response | grep "${nameMatcher}" | awk '{print $2}' | sed ${nameExtractor} >> .repos

# Continue fetching the list of repos until we've gotten all of them
for ((i=$nextPage;i<=$lastPage;i++))
do
    curl -is -u "$creds" https://api.github.com/orgs/phetsims/repos?page=${i} -o .response
    cat .response | grep "${nameMatcher}" | awk '{print $2}' | sed ${nameExtractor} >> .repos
done

# Put the repos in alphanumeric order
sort -f .repos -o .repos

# Cleanup temporary files
rm .response .repos.old

