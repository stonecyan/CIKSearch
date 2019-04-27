## To start the application:

Run `. venv/bin/activate` to start the virtual environment in Terminal

Then run the application using: `python CIKSearch.py <CIK#>`

Mandatory parameter is the CIK or ticker, optional parameters are document type and date. Document type default is 13F and default date is None. Enter `python CIKSearch.py -h` for more information.

## Example:
`python CIKSearch.py 0001179392 -t 13F -d 20170123`

The .tsv file is saved in the output folder under the name <CIK#>-<Date>.tsv

## Supported Formats
This program only handles 13F-HR reports with the XML format. Certain forms I found were not in this XML format, and require parsing situations. More research would be needed on all the different types of data formats we would be looking at, to write code that can handle all these situations. From my initial scan, it seems that the information always comes in an information table. We can search for the words "Information Table", and try to parse the necessary data from the table.


