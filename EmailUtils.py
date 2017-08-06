import re


def extract_emails(html):
    if html is None:
        return []

    emails = []

    doc = bytes(str(html.text), 'utf-8').decode('unicode_escape')

    reg = r'<?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not is_fake_email(match):
            emails.append(str(match))

    reg = r'<?([a-zA-Z0-9_.+-]+\(a\)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not is_fake_email(match):
            emails.append(str(match).replace("(a)", "@"))

    reg = r'<?([a-zA-Z0-9_.+-]+\(@\)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not is_fake_email(match):
            emails.append(str(match).replace("(@)", "@"))

    reg = r'<?([a-zA-Z0-9_.+-]+\[@\][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not is_fake_email(match):
            emails.append(str(match).replace("[@]", "@"))

    reg = r'<?([a-zA-Z0-9_.+-]+\[at\][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not is_fake_email(match):
            emails.append(str(match).replace("[at]", "@"))

    reg = r'<?([a-zA-Z0-9_.+-]+\(at\)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not is_fake_email(match):
            emails.append(str(match).replace("(at)", "@"))

    reg = r'<?([a-zA-Z0-9_.+-]+\[AT\][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not is_fake_email(match):
            emails.append(str(match).replace("[AT]", "@"))

    reg = r'<?([a-zA-Z0-9_.+-]+\(AT\)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?'
    for match in re.findall(reg, doc):
        if str(match) not in emails and not is_fake_email(match):
            emails.append(str(match).replace("(AT)", "@"))

    return emails


def is_fake_email(email):
    return str(email).endswith(".png") \
           or str(email).endswith(".jpg") \
           or str(email).endswith(".jpeg")
