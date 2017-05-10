#!/bin/bash

# Create Log Files first

if [ ! -f /home/vkurakundi/login.txt ]
then
        echo "Log file created"
        touch /home/vkurakundi/login.txt
fi

if [ ! -f /home/vkurakundi/logout.txt ]
then
        echo "Log file created"
        touch /home/vkurakundi/logout.txt
fi

userin="$(who | grep mlevi | awk '{ print $1 }')"

# Compare it with the user and then send email

if [ "$userin" = 'mlevi' ]
then
        emailsent="$(cat /home/vkurakundi/login.txt)"

        if [ "$emailsent" != 'Yes' ]
        then
                echo "Matt has just logged into devxyz machine" | mail -s "Intruder Alert" yourname@email.com
                echo "Yes" > /home/vkurakundi/login.txt
                echo "No" > /home/vkurakundi/logout.txt
        fi

else
        emailsent2="$(cat /home/vkurakundi/logout.txt)"

        if [ "$emailsent2" != 'Yes' ]
        then
                msg="$(last mlevi | head -n 1)"
                echo "Matt logged out from devxyz, here is the detail: $msg" | mail -s "Day Saved! Intruder is gone!" yourname@email.com
                echo "Yes" > /home/vkurakundi/logout.txt
                echo "No" > /home/vkurakundi/login.txt
        fi

fi
