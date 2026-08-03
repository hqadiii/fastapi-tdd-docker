from app.models.tortoise import TextSummary


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "url"],
                "msg": "Field required",
                "input": {},
            }
        ]
    }


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    test_app_with_db.portal.call(TextSummary.all().delete)
    response = test_app_with_db.get("/summaries/1/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1


def test_delete_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.delete(f"/summaries/{summary_id}/")
    assert response.status_code == 204


def test_delete_summary_incorrect_id(test_app_with_db):
    test_app_with_db.portal.call(TextSummary.all().delete)
    response = test_app_with_db.delete("/summaries/1/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]
    payload = {"url": "https://foo.bar", "summary": "updated!"}
    response = test_app_with_db.put(f"/summaries/{summary_id}/", json=payload)
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == payload["url"]
    assert response_dict["summary"] == payload["summary"]
    assert response_dict["created_at"]


def test_update_summary_incorrect_id(test_app_with_db):
    test_app_with_db.portal.call(TextSummary.all().delete)
    payload = {"url": "https://foo.bar", "summary": "updated!"}
    response = test_app_with_db.put("/summaries/1/", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary_invalid_json(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{summary_id}/", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": {},
                "loc": ["body", "summary"],
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


def test_update_summary_invalid_keys(test_app_with_db):
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.put(f"/summaries/{summary_id}/", json=payload)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {"url": "https://foo.bar"},
                "loc": ["body", "summary"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }
