import re
import pdfplumber
from pypdf import PdfReader

ACROFORM_FIELD_MAP = {
    "name": "klient_nazwa",
    "old_contract_number": "numer_umowy",
    "pesel": "klient_identyfikator",
    "phone": "klient_telefon",
    "email": "klient_email",
    "postal_code": "klient_kod_pocztowy",
    "city": "klient_miejscowosc",
    "street": "klient_adres",
}

def _extract_from_acroform(file_stream) -> dict | None:
    file_stream.seek(0)
    try:
        reader = PdfReader(file_stream)
        fields = reader.get_fields()
    except Exception:
        return None

    if not fields:
        return None

    result = {}
    found_any_value = False

    for out_key, pdf_field_name in ACROFORM_FIELD_MAP.items():
        field = fields.get(pdf_field_name)
        value = (field.get("/V") or "").strip() if field else ""

        if value:
            found_any_value = True

        if out_key == "email":
            result[out_key] = value or None
        elif out_key == "pesel":
            result[out_key] = value.replace("-", "").strip() if value else ""
        else:
            result[out_key] = value

    return result if found_any_value else None


PATTERN_CONTRACT = re.compile(r"Numer umowy:[ \t]*(?P<contract_number>[\w./-]+)")
PATTERN_ADDRESS = re.compile(r"zam\.\s*/\s*siedziba\s*przy\s*ul\.[ \t]*(?P<street>[^\n]+)")
PATTERN_POSTAL = re.compile(r"kod pocztowy:[ \t]*(?P<postal_code>\d{2}-\d{3})")
PATTERN_CITY = re.compile(r"miejscowość:[ \t]*(?P<city>[^\n]+)")
PATTERN_PHONE = re.compile(r"Telefon:[ \t]*(?P<phone>[+\d][\d \t-]*)")
PATTERN_NAME = re.compile(r"Imię i nazwisko / Firma:[\s\n]*(?P<name>(?!zam\.)[^\n]+)")
PATTERN_PESEL = re.compile(r"PESEL\s*/\s*NIP:[ \t]*(?P<pesel>[\d-]{10,13})")
PATTERN_EMAIL = re.compile(r"Adres e-mail:[\s\n]*(?P<email>[\w.-]+@[\w.-]+\.\w+)")

def _extract_from_flat_text(text: str) -> dict:
    match_contract = PATTERN_CONTRACT.search(text)
    match_name = PATTERN_NAME.search(text)
    match_address = PATTERN_ADDRESS.search(text)
    match_postal_code = PATTERN_POSTAL.search(text)
    match_city = PATTERN_CITY.search(text)
    match_pesel = PATTERN_PESEL.search(text)
    match_phone = PATTERN_PHONE.search(text)
    match_email = PATTERN_EMAIL.search(text)

    return {
        "name": match_name.group("name").strip() if match_name else "",
        "old_contract_number": match_contract.group("contract_number").strip() if match_contract else "",
        "pesel": match_pesel.group("pesel").replace("-", "").strip() if match_pesel else "",
        "phone": match_phone.group("phone").strip() if match_phone else "",
        "email": match_email.group("email").strip() if match_email else None,
        "postal_code": match_postal_code.group("postal_code").strip() if match_postal_code else "",
        "city": match_city.group("city").strip() if match_city else "",
        "street": match_address.group("street").strip() if match_address else "",
    }

def extract_contract_data(file_stream) -> dict:
    acroform_data = _extract_from_acroform(file_stream)
    if acroform_data is not None:
        return acroform_data

    file_stream.seek(0)
    with pdfplumber.open(file_stream) as pdf:
        text = pdf.pages[0].extract_text() or ""

    return _extract_from_flat_text(text)