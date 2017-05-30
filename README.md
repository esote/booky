# Booky

Python code to gather random book data from Goodreads and print it out in a copy-pastable manner such that it can be copied into an excel or Google sheets document. Mainly for my own use, but I figured why not share it.

## Booky-v3

*Very* simple CSV data file appendage to negate the need for copy-pasting. It should automatically create a CSV file called `data.csv` and start appending from there. I recommend adding a header to the CSV in the form `Title,Pages,Rating`.

## Booky-v4

Command line options and new stuff
```
$ python3 Booky-v4.py -h
usage: Booky-v4.py [-h] [-v {0,1,2,3}] [-mr MIN_RATING] filename

Gather random book data from Goodreads and append it to a file in CSV format, until the program is manually closed or until a connection issue.		

example command: Booky-v4.py -v3 -mr /path/to/file.csv

positional arguments:
  filename              output file, only supports FULL path (no tilde, etc.)

optional arguments:
  -h, --help            show this help message and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        specify verbosity level, default = 2		
                        0 = no output		
                        1 = continually print line count after appending to file
                        2 = after keyboard interrupt, print count of lines added since program start and program run time		
                        3 = both verbosity options 1 and 2
  -mr MIN_RATING, --min-rating MIN_RATING
                        specify the minimum accepted rating, default = 30
```

### Example:
```
$python3 -OO Booky-v4.py -v3 -mr 100 /path/to/data.csv
```
```
$python3 Booky-v4.py -verbosity 0 --min-rating 1 /path/to/other/data.csv
```
