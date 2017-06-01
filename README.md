# Booky

Python code to gather random book data by scraping Goodreads and prints it out in a copiable format (v1 and v2) or outputs it to a file in CSV format (v3 onward). Mainly for my own use, but I figured why not share it.

### Example

```
$ python3 -O Booky-v5.py -v3 --min-rating 500 /path/to/data.csv
```

Thanks to Code Review user MrGrj for the suggested code improvements (present in v2 onward) and to Code Review user alecxe for the suggested code improvements (present in v5).

## Booky-v3 changes

- Program now outputs to a file instead of printing
- Automatically creates file `data.csv` in working directory
- Outputs with CSV formatting (double quotes around title, comma separation, etc.)

### I recommend adding a header to the CSV in the form `Title,Pages,Rating`.

## Booky-v4 changes

- In `to_int(rating_count)` added if-else statement to check if rating count is already an integer
- Fixed issue caused by the removal of series identification where an extra space is left at the end of the title
- In `get_book_rating_count(soup)` added try-except block to catch if the rating count is missing
- **Added command line parsing**, here's the "*help*" print out:

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

- Added option to continually print total line count after appendage (always prints on the same line thanks to `sys.stdout.write("\033[F")`) - if `--verbosity` is 1 or 3
- Added option to print program run time (in real time) and total count of lines added - upon keyboard interrupt (manual exit) - if `--verbosity` is 2 or 3
- Added `FileNotFoundError` to main try-except block to catch if file doesn't exist
- Added `os.path.isfile(FILE_PATH)` to check if file is deleted while the program is running
- Now actually prints something if `ConnectionResetError` is caught

## Booky-v5 changes

- Changed single line commenting to use `#` instead of docstrings
- Removed random endline spaces, added spaces where they should go
- **Added code to maintain session for `URL`**
- **Changed parser from `html.parser` to `lxml` for faster parsing**
- **Added `SoupStrainer` to parse more efficiently**
- Changed comma to colon for `soup.find()` in `get_book_rating_count`
- Updated command line parsing help print out:

```
usage: Booky-v5.py [-h] [-v {0,1,2,3}] [-mr MIN_RATING] filepath

Gather random book data from Goodreads and append it to a file in CSV format, until the program is manually closed or until a connection issue. I recommend having the CSV header: Title,Pages,Rating.

positional arguments:
  filepath              output file, only supports FULL path (no tilde, etc.)

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
