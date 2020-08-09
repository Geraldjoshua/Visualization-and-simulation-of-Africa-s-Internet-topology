#!/bin/bash
#((RANDOM%10))
while read line; do whois -h whois.ripe.net -T route $line -i origin | egrep "route: " |awk 'NR==1{$1=$1;print}'; done < AsnAfrica.txt > ipnetwork.txt