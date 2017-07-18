# import required modules
from datetime import timedelta
from bs4 import BeautifulSoup
from google import search
from time import time, localtime, strftime
import xlsxwriter
import requests
import sys
import re

INPUT_FILE = "/Volumes/Dario Porsche LaCie/ALL/Dario's Mac/Documents/Dario MAC Manual Backup (07th May 2017)/Businesses/-Businesses/Actual/SeasonAbroad/Approaching Companies/Campaigns/PythonScript/Real Script for Winter Campaign/booking_example.txt";
# INPUT_FILE = "C:\\Users\\milan\\python\\input\\keywords_short.txt"
OUTPUT_FILE = "/Volumes/Dario Porsche LaCie/ALL/Dario's Mac/Documents/Dario MAC Manual Backup (07th May 2017)/Businesses/-Businesses/Actual/SeasonAbroad/Approaching Companies/Campaigns/PythonScript/Real Script for Winter Campaign/hotels.csv";
# OUTPUT_FILE = "C:\\Users\\milan\\python\\output\\hot.xlsx"

# put the list of keywords (separated by space) to help find hotel webiste.
ADDITIONAL_KEYWORDS_BEFORE = "Hotel"
ADDITIONAL_KEYWORDS_AFTER = "Bulgaria"


# TIME measuring defs
def secondsToStr(t):
    return str(timedelta(seconds=t))


def timeToStr(t):
    return strftime("%H:%M:%S", t)


line = "=" * 40


def log(s, elapsed=None):
    print(line)
    print(timeToStr(localtime()), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()


def endlog():
    end = time()
    elapsed = end - start
    log("End Program", secondsToStr(elapsed))


def elapsedFrom(stamp):
    end = time()
    elapsed = end - stamp
    log("Elapsed time: ", secondsToStr(elapsed))


def now():
    return secondsToStr(time())


# END TIME measuring defs

def findContactPage(link):
    # find all links on the page
    # req = urllib.request.Request(link, None, headers);
    # html = urllib.request.urlopen(req);

    html = generalSession.get(link)

    bsObj = BeautifulSoup(html.text, "html.parser")
    links = bsObj.findAll('a')
    base = bsObj.find('base')
    baseUrl = None
    if base is not None:
        if base.has_attr('href'):
            baseUrl = base['href'].strip()
    url = None
    for link in links:
        # print(link);
        if len(link.contents) == 0:
            continue
        content = str(link.contents[0]).strip()
        # print(content);
        if content is not None:
            content = content.strip()
        href = None
        if link.has_attr('href'):
            href = link['href']
        title = None
        if link.has_attr('title'):
            title = link['title']
        # print(str(content) + ">" + str(href) + ">" + str(title));
        if "contact" in str(link):
            url = str(href).strip()
            break
        if "Contact" in str(link):
            url = str(href).strip()
            break
        if "kontakt" in str(link):
            url = str(href).strip()
            break
        if "Kontakt" in str(link):
            url = str(href).strip()
            break

    if "http" in str(url):
        return str(url)

    if "www" in str(url):
        return str(url)

    if not baseUrl is None:
        return (baseUrl + str(url))
    else:
        return (html.url + str(url))

        # return None


def getEmails(link):
    if link is None:
        return []

    emails = []

    # req = urllib.request.Request(link, None, headers);
    # html = urllib.request.urlopen(req);

    html = generalSession.get(link)
    doc = bytes(str(html.text), 'utf-8').decode('unicode_escape')

    reg = r'<?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not isFakeEmail(match):
            emails.append(str(match))

    reg = r'<?([a-zA-Z0-9_.+-]+\(a\)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not isFakeEmail(match):
            emails.append(str(match).replace("(a)", "@"))

    reg = r'<?([a-zA-Z0-9_.+-]+\[at\][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not isFakeEmail(match):
            emails.append(str(match).replace("[at]", "@"))

    reg = r'<?([a-zA-Z0-9_.+-]+\[AT\][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not isFakeEmail(match):
            emails.append(str(match).replace("[AT]", "@"))

    return emails


def isFakeEmail(email):
    return str(email).endswith(".png") \
           or str(email).endswith(".jpg") \
           or str(email).endswith(".jpeg")


def fetchHotels(link):
    # maxPages = 10;
    namesFound = 0
    page = 1
    list = []
    global xls_row
    global xls_fail_row

    # Get hotels in our City reusing booking.com session

    html = bookingSession.get(link)
    # req = urllib.request.Request(link, None, headers);
    # html = urllib.request.urlopen(req);
    while True:
        stamp = time()
        print("Page: " + str(page))
        # Prepare result for processing
        bsObj = BeautifulSoup(html.text, "html.parser")

        # Find elements containing hotel names
        hotelNameElements = bsObj.findAll('span', attrs={'class': re.compile('\w\w-hotel__name')})

        if (hotelNameElements.count == 0):
            break

        # hotelDetailElements = bsObj.findAll('a', attrs = {'class' : 'hotel_name_link url'});

        # Extract names from name elements
        for nameElement in hotelNameElements:
            # print(nameElement.contents[0].strip(), "");
            name = nameElement.contents[0].strip()
            namesFound += 1
            # Try to find a web page
            # Make a google search
            hotelLink = 'NOT FOUND'
            rank = 0
            try:
                searchResult = search(ADDITIONAL_KEYWORDS_BEFORE + " " + name + " " + ADDITIONAL_KEYWORDS_AFTER, stop=10)
            except:
                print("Error: ", sys.exc_info()[0])
                print("While googling for: " + str(hotelLink))
                continue
            for url in searchResult:
                rank += 1
                if "booking.com" in url:
                    continue
                if "facebook.com" in url:
                    continue
                if "tripadvisor." in url:
                    continue
                if "chamonix.net" in url:
                    continue
                if "ultimate-ski.com" in url:
                    continue
                if "agoda.com" in url:
                    continue
                if "bedandbreakfast.eu" in url:
                    continue
                if "goibibo.com" in url:
                    continue
                if "makemytrip.com" in url:
                    continue
                if "travelguru.com" in url:
                    continue
                if "cleartrip.com" in url:
                    continue
                if "yatra.com" in url:
                    continue
                if "odalys-vacances.com" in url:
                    continue
                if "odalys-vacation-rental.com" in url:
                    continue
                if "www.hotels.com" in url:
                    continue
                if "www.expedia.com" in url:
                    continue
                if "mountvacation.co.uk" in url:
                    continue

                hotelLink = url
                break

            emails = []
            errorMsg = ['NOT FOUND']
            errorOccured = False
            try:
                emails = getEmails(hotelLink)
            except:
                print("Error: ", sys.exc_info()[0])
                print("While getting emails from: " + str(hotelLink))
                errorMsg.append("Get emails from main page: " + str(sys.exc_info()[0]))
                errorOccured = True

            contactPage = None

            if len(emails) == 0 and not errorOccured:
                try:
                    contactPage = findContactPage(hotelLink)
                except:
                    print("Error: ", sys.exc_info()[0])
                    print("While getting contact page from: " + str(hotelLink))
                    errorMsg.append("Get contact page: " + str(sys.exc_info()[0]))
                    errorOccured = True

            if not contactPage is None and len(emails) == 0 and not errorOccured:
                try:
                    emails = getEmails(contactPage)
                except:
                    print("Error: ", sys.exc_info()[0])
                    print("While getting emails from: " + str(contactPage))
                    errorMsg.append("Get emails from contact page: " + str(sys.exc_info()[0]))

            if len(emails) == 0:
                emails = errorMsg
                worksheet_failed.write(xls_fail_row, 0, name.strip())
                worksheet_failed.write(xls_fail_row, 1, hotelLink.strip())
                worksheet_failed.write(xls_fail_row, 2, ", ".join(emails))
                worksheet_failed.write(xls_fail_row, 3, str(rank).strip())
                xls_fail_row = xls_fail_row + 1
                continue

            list += [[name, hotelLink, str(emails), str(rank)]]

            print(str(hotelLink) + " : " + str(emails))

            try:
                # writer.writerow({'HOTEL NAME': name.strip(), 'LINK': hotelLink.strip(),
                #                  'EMAILS': ",".join(str(emails).strip()),
                #                  'RANK': str(rank).strip()})
                worksheet.write(xls_row, 0, name.strip())
                worksheet.write(xls_row, 1, hotelLink.strip())
                worksheet.write(xls_row, 2, ", ".join(emails))
                worksheet.write(xls_row, 3, str(rank).strip())
                xls_row = xls_row + 1

            except:
                print("Error: ", sys.exc_info()[0])
                print(name)

        log("[" + str(page) + "]" + " Page processing time", time() - stamp)

        page = page + 1

        if page == 3:
            break

        # Find the base link for "next" page results
        element = bsObj.find('link', attrs={'rel': 'next'})

        if element:
            baseLinkForNext = element['href']
        else:
            break

        # print(list);
        # break;
        # req = urllib.request.Request(baseLinkForNext, None, headers);
        # html = urllib.request.urlopen(req);

        html = bookingSession.get(baseLinkForNext)

    # Return the number of hotel names found
    return list


start = time()

# Open keywords file
f = open(INPUT_FILE, "r")

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
header = {'User-Agent': user_agent}
headers = requests.utils.default_headers()
headers.update(header)

# Initialize sessions
bookingSession = requests.Session()
bookingSession.headers.update(headers)
generalSession = requests.Session()
generalSession.headers.update(headers)

# # Loop through keywords and query booking.com
# with open(OUTPUT_FILE, "w", newline="") as csvfile:
#     fieldnames = ['HOTEL NAME', 'LINK', 'EMAILS', 'RANK']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     writer.writeheader()
#
#
# # close excel file
# csvfile.close()

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(OUTPUT_FILE)
worksheet = workbook.add_worksheet()
worksheet_failed = workbook.add_worksheet()
xls_row = 0
xls_fail_row = 0

linkNo = 0
for link in f:
    linkNo += 1
    print("Processing link no. " + str(linkNo) + ".")
    stamp = time()
    # print(link.strip());
    hotelList = fetchHotels(link.strip())
# close the file
f.close()
# close workbook
workbook.close()
endlog()
