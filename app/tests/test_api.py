def test_root_endpoint(test_db):
    response = test_db.get("/")
    assert response.status_code == 200


def test_generate_happy_path(test_db):
    client_data = {
        "name": "Jan Kowalski",
        "old_contract_number": "S/1",
        "pesel": "85031212345",
        "phone": "+48111222333",
        "postal_code": "04-350",
        "city": "Warszawa",
        "street": "Nowy Świat 1"
    }
    test_db.post("/contracts/", json=client_data)
    response = test_db.post("/contracts/generate-upsell", json={"old_contract_number": "S/1"})
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"


def test_generate_upsell_returns_404(test_db):
    response = test_db.post("/contracts/generate-upsell", json={"old_contract_number": "DOES_NOT_EXIST"})
    assert response.status_code == 404


def test_upload_endpoint_rejects_non_pdf(test_db):
    response = test_db.post(
        "/contracts/upload",
        files={"file": ("test.txt", b"not a pdf", "text/plain")},
    )
    assert response.status_code == 400


def test_upload_real_pdf_integration(test_db):
    pdf_path = "app/tests/fixtures/test_contract.pdf"
    
    with open(pdf_path, "rb") as f:
        response = test_db.post(
            "/contracts/upload",
            files={"file": ("test_contract.pdf", f, "application/pdf")},
        )
        
    assert response.status_code == 200
    
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "pesel" in data