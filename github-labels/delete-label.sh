#!/bin/bash

read -p "Github Username: " username
read -sp "Github Password: " password

echo ''

creds=${username}:${password}

if [[ $1 = '' ]]
then
echo "Usage: $0 label-name"
exit 1
else
label=$1
echo "$label"
fi

for repo in `cat phetsims-repos`
do
    url=https://api.github.com/repos/phetsims/${repo}/labels/${label}
    echo $url
    curl -isH 'User-Agent: "phet"' -u "$creds" -d "$label" -X "DELETE" $url | head -1
done

