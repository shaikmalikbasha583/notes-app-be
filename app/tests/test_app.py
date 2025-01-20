# import unittest

# from fastapi.testclient import TestClient

# from app.main import app


# class TestMainApp(unittest.TestCase):
#     def setUp(self):
#         # print("I am in setUp")
#         self.client = TestClient(app)
#         app.dependency_overrides = {}

#     # def test_read_items(self):
#     #     response = self.client.get("/items/")
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIsInstance(response.json(), list)
#     #     self.assertEqual(len(response.json()), 2)

#     async def test_get_all_notes(self):
#         print("Running test_get_all_notes test case")
#         response = self.client.get("/api/v1/notes/")
#         print("Response: ", response.json())
#         assert response.status_code == 200
#         assert response.json()["success"] is True
#         assert response.json()["message"] == "List of notes"
#         assert response.json()["ui_message"] == "List of notes from the database"
#         assert len(response.json()["notes"]) >= 0

#     # def test_read_item(self):
#     #     response = self.client.get("/items/1")
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIsInstance(response.json(), dict)
#     #     self.assertEqual(response.json()["name"], "Item 1")

#     # def test_read_item_invalid_id(self):
#     #     response = self.client.get("/items/abc")
#     #     self.assertEqual(response.status_code, 422)


# if __name__ == "__main__":
#     unittest.main()
