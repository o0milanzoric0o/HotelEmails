from bs4 import BeautifulSoup

CONTACT_LABELS = ["contact",
                  "kontakt",
                  "Kontakt",
                  "Contacts",
                  "Kontakts",
                  "Kontakti",
                  "About",
                  "Impressum",
                  "Anfragen",
                  "Buchen",
                  "Inquiry",
                  "Enquiry",
                  "kontaktua",
                  "кантакт",
                  "контакт",
                  "contacte",
                  "kokkupuude",
                  "yhteyshenkilö",
                  "contacto",
                  "επαφή",
                  "kapcsolattartó",
                  "samband",
                  "Teagmháil",
                  "contatto",
                  "kontaktas",
                  "kuntatt",
                  "contato"]


def find_contact_page(html):
    # find all links on the page
    # req = urllib.request.Request(link, None, headers);
    # html = urllib.request.urlopen(req);

    bs_obj = BeautifulSoup(html.text, "html.parser")
    links = bs_obj.findAll('a')
    base = bs_obj.find('base')
    base_url = None
    if base is not None:
        if base.has_attr('href'):
            base_url = base['href'].strip()
    url = None
    for cp_link in links:
        if len(cp_link.contents) == 0:
            continue
        href = None
        if cp_link.has_attr('href'):
            href = cp_link['href']
        if is_link_to_contact_page(cp_link):
            url = str(href).strip()
            break

    if "http" in str(url):
        return str(url)

    if "www" in str(url):
        return str(url)

    if base_url is not None:
        return base_url + str(url)
    else:
        return html.url + str(url)


def is_link_to_contact_page(link):
    ret = False
    for label in CONTACT_LABELS:
        if label.lower() in str(link).lower():
            ret = True
            break
    return ret
