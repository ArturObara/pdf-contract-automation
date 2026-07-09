import pdfplumber
import re

PATTERN_CONTRACT = re.compile(r"Numer umowy:[ \t]*(?P<contract_number>[\w/-]+)")
PATTERN_ADDRESS = re.compile(r"zam\. / siedziba przy ul\.[ \t]*(?P<street>[^\n]+)")
PATTERN_POSTAL = re.compile(r"kod pocztowy:[ \t]*(?P<postal_code>[\d-]+)")
PATTERN_CITY = re.compile(r"miejscowość:[ \t]*(?P<city>[^\n]+)")
PATTERN_PHONE = re.compile(r"Telefon:[ \t]*(?P<phone>[+\d\s]+)")
PATTERN_NAME = re.compile(r"Imię i nazwisko / Firma:[\s\n]*(?P<name>(?!zam\.)[^\n]+)")
PATTERN_PESEL = re.compile(r"PESEL/NIP:[\s\n]*(?P<pesel>\d{10,11})")
PATTERN_EMAIL = re.compile(r"Adres e-mail:[\s\n]*(?P<email>[\w\.-]+@[\w\.-]+\.\w+)")

def extract_contract_data(file_stream) -> dict:
    with pdfplumber.open(file_stream) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        match_contract_old = PATTERN_CONTRACT.search(text)
        match_name = PATTERN_NAME.search(text)
        match_address = PATTERN_ADDRESS.search(text)
        match_postal_code = PATTERN_POSTAL.search(text)
        match_city = PATTERN_CITY.search(text)
        match_pesel = PATTERN_PESEL.search(text)
        match_mobile_phone = PATTERN_PHONE.search(text)
        match_email = PATTERN_EMAIL.search(text)

    return {
        "name": match_name.group('name').strip() if match_name else "",
        "old_contract_number": match_contract_old.group('contract_number').strip() if match_contract_old else "",
        "pesel": match_pesel.group('pesel').strip() if match_pesel else "",
        "phone": match_mobile_phone.group('phone').strip() if match_mobile_phone else "",
        "email": match_email.group('email').strip() if match_email else None,
        "postal_code": match_postal_code.group('postal_code').strip() if match_postal_code else "",
        "city": match_city.group('city').strip() if match_city else "",

        "street": match_address.group('street').strip() if match_address else ""
    }