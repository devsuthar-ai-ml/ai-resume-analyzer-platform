def test_resume_upload_and_history(client, auth_headers, sample_docx_bytes):
    files = {
        "file": (
            "resume.docx",
            sample_docx_bytes,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    upload_response = client.post("/api/resume/upload", headers=auth_headers, files=files)

    assert upload_response.status_code == 200
    upload_body = upload_response.json()
    assert upload_body["original_filename"] == "resume.docx"

    history_response = client.get("/api/resume/history", headers=auth_headers)

    assert history_response.status_code == 200
    items = history_response.json()["items"]
    assert len(items) == 1
    assert items[0]["original_filename"] == "resume.docx"


def test_resume_upload_rejects_invalid_extension(client, auth_headers):
    files = {"file": ("resume.txt", b"not-valid", "text/plain")}
    response = client.post("/api/resume/upload", headers=auth_headers, files=files)
    assert response.status_code == 400
