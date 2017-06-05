# Kellogg Faculty Info Scraper

## Prerequisites

The scraping script is built on Python 2.7 and the libraries requests, beautifulsoup, and lxml. To get started, created a Python virtualenv, activate it, and install the requirements:

```bash
virtualenv -p python2 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running

Run this scraper with:

```bash
python scrape_faculty.py
```

This will create a sub-folder within `html` with today's date (in `YYYYMMDD` format), where it will save the HTML files for each of the faculty profile pages.

It will also then extract information from each of these pages, and creates the following files:

* [faculty.json](faculty.json) - This is *everything* scraped from the site, including faculty that are missing information (like names) in their pages.
* [faculty.csv](faculty.csv) - This is the same as `faculty.json` only in CSV format.
* [faculty_with_names_and_faces.json](faculty_with_names_and_faces.json) - This is a subset of the `faculty.json` data, only those faculty with names recorded. Yes this is a thing.
* [faculty_with_names.json](faculty_with_names.json) - This is a subset of `faculty_with_names_and_faces.json` without image links, which could be used for a faster page (not having to load all the images).

These files are deposited in the local directory here. To use with the faculty directory web app, these files should be copied to the parent folder.

## Credit

Written by Nicholas Bennett, [nicholas.bennett@kellogg.northwestern.edu](mailto:nicholas.bennett@kellogg.northwestern.edu), while working in KIS Operations Support to ease with putting names to faces of faculty, and to more easily look up their information.
