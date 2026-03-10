def test_analyze_resume_flow(client, auth_headers, sample_docx_bytes):
    files = {
        "file": (
            "resume.docx",
            sample_docx_bytes,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    upload_response = client.post("/api/resume/upload", headers=auth_headers, files=files)
    resume_id = upload_response.json()["id"]

    analyze_payload = {
        "resume_id": resume_id,
        "job_title": "Backend Engineer",
        "job_description": "We need a Python engineer with FastAPI, Docker, SQL, and PostgreSQL experience.",
    }
    analyze_response = client.post("/api/analyze", headers=auth_headers, json=analyze_payload)

    assert analyze_response.status_code == 200
    analyze_body = analyze_response.json()
    assert 0 <= analyze_body["match_percentage"] <= 100
    assert 0 <= analyze_body["resume_score"] <= 100
    assert isinstance(analyze_body["missing_skills"], list)

    result_response = client.get(f"/api/results/{analyze_body['id']}", headers=auth_headers)

    assert result_response.status_code == 200
    result_body = result_response.json()
    assert result_body["id"] == analyze_body["id"]
