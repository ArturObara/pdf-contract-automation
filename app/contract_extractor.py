import pdfplumber
import re

def extract_contract_data(file_stream) -> dict:
    with pdfplumber.open(file_stream) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        match_contract_old = re.search(r"Numer umowy:[\s\n]*(?P<contract_number>[\w/-]+)", text)
        match_name = re.search(r"Imię i nazwisko / Firma:\s*(?P<name>[^\n]+)", text)
        match_address = re.search(r"zam\. / siedziba przy ul\.\s*(?P<street>[^\n]+)", text)
        match_postal_code = re.search(r"kod pocztowy:[\s\n]*(?P<postal_code>[\d-]+)", text)
        match_city = re.search(r"miejscowość:[\s\n]*(?P<city>[^\n]+)", text)
        match_mobile_phone = re.search(r"Telefon:\s*(?P<phone>[+\d\s]+)", text)
        match_email = re.search(r"Adres e-mail:[\s\n]*(?P<email>\S+)", text)

    return {
        "name": match_name.group('name').strip() if match_name else None,
        "old_contract_number": match_contract_old.group('contract_number').strip() if match_contract_old else None,
        "phone": match_mobile_phone.group('phone').strip() if match_mobile_phone else None,
        "email": match_email.group('email').strip() if match_email else None,
        "postal_code": match_postal_code.group('postal_code').strip() if match_postal_code else None,
        "city": match_city.group('city').strip() if match_city else None,
        "street": match_address.group('street').strip() if match_address else None
    }