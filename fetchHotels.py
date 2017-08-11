# import required modules
from bs4 import BeautifulSoup
from google import search
from time import time
import xlsxwriter
import requests
import sys
import re

import ExclusionList
import Logging
import EmailUtils
import ContactPageUtils

INPUT_FILE = "/Users/DarioZoric-S/Documents/DZ TEMP/2) Sept. 2017 (Ski Resorts)/Austria - can/Austria copy 1.1.txt"
# INPUT_FILE = "C:\\Users\\milan\\python\\input\\keywords_short.txt"
OUTPUT_FILE = "/Users/DarioZoric-S/Documents/DZ TEMP/2) Sept. 2017 (Ski Resorts)/Austria - can/austria_winter_1.1.xlsx"
# OUTPUT_FILE = "C:\\Users\\milan\\python\\output\\hot.xlsx"

# put the list of keywords (separated by space) to help find hotel webiste.
ADDITIONAL_KEYWORDS_BEFORE = "Hotel"
ADDITIONAL_KEYWORDS_AFTER = "Austria"


def fetch_hotels(hotels_link):
    # maxPages = 10;
    names_found = 0
    page = 1
    list = []
    global xls_row
    global xls_fail_row

    # Get hotels in our City reusing booking.com session

    html = bookingSession.get(hotels_link)
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
            names_found += 1
            # Try to find a web page
            # Make a google search
            hotel_link = 'NOT FOUND'
            rank = 0
            try:
                searchResult = search(ADDITIONAL_KEYWORDS_BEFORE + " " + name + " " + ADDITIONAL_KEYWORDS_AFTER,
                                      stop=20)
            except:
                print("Error: ", sys.exc_info()[0])
                print("While googling for: " + str(hotel_link))
                continue
            for url in searchResult:
                rank += 1
                if ExclusionList.is_excluded(url):
                    continue

                hotel_link = url
                break

            emails = []
            error_msg = ['NOT FOUND']
            error_occurred = False
            try:
                html = generalSession.get(hotel_link)
                emails = EmailUtils.extract_emails(html)
            except:
                print("Error: ", sys.exc_info()[0])
                print("While getting emails from: " + str(hotel_link))
                error_msg.append("Get emails from main page: " + str(sys.exc_info()[0]))
                error_occurred = True

            contact_page = None

            if len(emails) == 0 and not error_occurred:
                try:
                    html = generalSession.get(hotel_link)
                    contact_page = ContactPageUtils.find_contact_page(html)
                except:
                    print("Error: ", sys.exc_info()[0])
                    print("While getting contact page from: " + str(hotel_link))
                    error_msg.append("Get contact page: " + str(sys.exc_info()[0]))
                    error_occurred = True

            if not contact_page is None and len(emails) == 0 and not error_occurred:
                try:
                    html = generalSession.get(contact_page)
                    emails = EmailUtils.extract_emails(html)
                except:
                    print("Error: ", sys.exc_info()[0])
                    print("While getting emails from: " + str(contact_page))
                    error_msg.append("Get emails from contact page: " + str(sys.exc_info()[0]))

            if len(emails) == 0:
                emails = error_msg
                worksheet_failed.write(xls_fail_row, 0, name.strip())
                worksheet_failed.write(xls_fail_row, 1, hotel_link.strip())
                worksheet_failed.write(xls_fail_row, 2, ", ".join(emails))
                worksheet_failed.write(xls_fail_row, 3, str(rank).strip())
                xls_fail_row = xls_fail_row + 1
                continue

            list += [[name, hotel_link, str(emails), str(rank)]]

            print(str(hotel_link) + " : " + str(emails))

            try:
                # writer.writerow({'HOTEL NAME': name.strip(), 'LINK': hotelLink.strip(),
                #                  'EMAILS': ",".join(str(emails).strip()),
                #                  'RANK': str(rank).strip()})
                worksheet.write(xls_row, 0, name.strip())
                worksheet.write(xls_row, 1, hotel_link.strip())
                worksheet.write(xls_row, 2, ", ".join(emails))
                worksheet.write(xls_row, 3, str(rank).strip())
                xls_row = xls_row + 1

            except:
                print("Error: ", sys.exc_info()[0])
                print(name)

        Logging.log("[" + str(page) + "]" + " Page processing time", time() - stamp)

        page = page + 1
        # THESE TWO LINES BELOW ARE JUST FOR TEST, UNHASHTAG BELOW TWO TO RUN TEST
        #if page == 3:
        #    break

        # Find the base link for "next" page results
        element = bsObj.find('link', attrs={'rel': 'next'})

        if element:
            base_link_for_next = element['href']
        else:
            break

        # print(list);
        # break;
        # req = urllib.request.Request(baseLinkForNext, None, headers);
        # html = urllib.request.urlopen(req);

        html = bookingSession.get(base_link_for_next)

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
    hotelList = fetch_hotels(link.strip())
# close the file
f.close()
# close workbook
workbook.close()
Logging.end_log(start)
