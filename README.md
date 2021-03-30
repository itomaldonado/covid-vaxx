# Covid Vaxx Appointment Status

Checks for vaccine appointments slots in CVS across the US.

## Pre-Reqs:

* Python 3.7+

## Installation:

Just run `pip install -r requirements.txt`. If using virtual environments,
make sure activate them first!

## Usage:
```
➜  python get-availability.py --help
Usage: get-availability.py [OPTIONS] STATE

Options:
  -c, --city TEXT  City Name.
  --help           Show this message and exit.

```

* `STATE`: two-letter code representing state
* `--city` / `-c`: optional, the name of the town or city to check. If not provided,
it'll check all cities in that state.
