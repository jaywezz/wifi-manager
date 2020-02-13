# wifi-manager
Desktop application to manage a home wifi

Simple desktop application in python programming language that will listen
an incoming SMS via GSM modem, from the contact set in the settings.
It should read through the SMS looking for the amount set in the
settings page. If the amount is true then the app should look for the
group that matches the amount received.

The app should also read through the received SMS looking for any
phone number stated included in the SMS. It should reply an SMS to the
number found, containing password and username in the group which
the received amount belongs.

Every group in the groups page, contains a list of dynamic username and
password. Every username and password s only be used once and
when used the status becomes “used”. Incase the group is exhausted
the app should not send SMS to the contact found and status in the
received becomes “No action”. When more items are added in that
group, and an “no action” item is selected in the received table, and
action button is pressed the status should change to “Acted” and is
passed to the sent page.

Still under development
