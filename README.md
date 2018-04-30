# Google Calendar Undo Import without dependency on google client library

Accidently imported an .ics into the wrong calendar?

No panic, this tool allow you to undo with a few steps.

## Getting started
1. In google calendar: export your 'contaminated' calendar to a contaminated.ics file
2. From this website: download and extract the main.py file to the same folder
3. Open your terminal window, type the following command:
```sh
python main.py contaminated.ics > cleaned.ics
```
Note: the above command is to remove the events imported on the same day as when your run it. If you are undo importing a few days later, then modify the main.py file by providing the importDate.

4. In google canlender: deleted or unsubcribe you contaminated calendar, then import the cleaned.ics


## See also:
    https://github.com/brianc118/Google-Calendar-Undo-Import

