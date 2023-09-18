# url: http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
import argparse
# other imports go here
import urllib.request
import datetime
import csv
import re


def find(regex, string):
    return re.search(regex, string, re.IGNORECASE)


class Record:
    def __init__(self, file, time, browser, response, size):
        self.file = file
        self.extension = "." + file.rsplit(".")[-1].lower()
        self.time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        self.browser = self.parseBrowser(browser)
        self.response = int(response)
        self.size = int(size)

    def parseBrowser(self, browser):
        if find("firefox", browser): return "Firefox"
        if find("msie", browser): return "Explorer"
        if find("chrome", browser): return "Chrome"
        if find("safari", browser): return "Safari"
        return "other"


def downloadData(url):
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


def parse_data(csvFile):
    records = []
    for columns in csv.reader(csvFile.strip().split('\n'), delimiter=','):
        records.append(Record(*columns))
    return records


def imageHits(records):
    counter = 0
    for record in records:
        if find(".jpg|.gif|.png|.jpeg", record.extension):
            counter += 1
    print(f"Image requests account for {(counter / len(records)) * 100:.1f}% of all requests.")


def browser(records):
    counter = {}
    for r in records:
        if r.browser not in counter:
            counter[r.browser] = 0
        counter[r.browser] += 1

    maximum = max(counter, key=counter.get)
    print(f"Most popular browser today is {maximum}.")


def hours(records):
    counter = {hour: 0 for hour in range(0, 24)}
    for r in records:
        counter[r.time.hour] += 1

    hits = ((hour, count) for hour, count in counter.items())
    hits_sorted = sorted(hits, key=lambda x: x[1], reverse=True)

    for hour, count in hits_sorted:
        print(f"Hour {hour:02d} has {count} hits.")

def main(url):
    print(f"Running main with URL = {url}...")
    try:
        csvData = downloadData(url)
    except:
        print("Error downloading data, exiting")
        return

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
