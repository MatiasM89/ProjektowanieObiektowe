import unittest
import urllib.request
import urllib.error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
import time

# These tests are based on my Kotlin tests for the same API from Zadanie 6 for E-biznes
# Tests are simply rewritten in Python instead of Kotlin

class ProductApiTests(unittest.TestCase):
    BASE_URL = "http://localhost:8080"

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        req = urllib.request.Request(f"{self.BASE_URL}/reset", method="POST")
        urllib.request.urlopen(req).close()

    def tearDown(self):
        self.driver.quit()

    def get_response_body(self, url):
        self.driver.get(url)
        return self.driver.find_element(By.TAG_NAME, "body").text

    def make_delete_request(self, url):
        req = urllib.request.Request(url, method="DELETE")
        try:
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()
                response_body = response.read().decode()
                return status_code, response_body
        except urllib.error.HTTPError as e:
            status_code = e.code
            response_body = e.read().decode()
            return status_code, response_body

    def json_contains_product(self, json_str, product_name):
        pattern = f'"content"\\s*:\\s*"{product_name}"'
        return bool(re.search(pattern, json_str))

    def test_get_products_returns_all_products(self):
        response = self.get_response_body(f"{self.BASE_URL}/products")
        self.assertTrue(self.json_contains_product(response, "Phone"))
        self.assertTrue(self.json_contains_product(response, "Charger"))
        self.assertTrue(self.json_contains_product(response, "Pen"))

    def test_get_products_returns_three_products(self):
        response = self.get_response_body(f"{self.BASE_URL}/products")
        products = json.loads(response)
        self.assertEqual(len(products), 3)

    def test_get_product_by_id_1_returns_phone(self):
        response = self.get_response_body(f"{self.BASE_URL}/products/1")
        self.assertTrue(self.json_contains_product(response, "Phone"))

    def test_get_product_by_id_2_returns_charger(self):
        response = self.get_response_body(f"{self.BASE_URL}/products/2")
        self.assertTrue(self.json_contains_product(response, "Charger"))

    def test_get_product_by_id_3_returns_pen(self):
        response = self.get_response_body(f"{self.BASE_URL}/products/3")
        self.assertTrue(self.json_contains_product(response, "Pen"))

    def test_get_product_by_invalid_id_returns_404(self):
        response = self.get_response_body(f"{self.BASE_URL}/products/999")
        self.assertTrue("404" in response or "Not Found" in response)

    def test_get_product_by_negative_id_returns_404(self):
        response = self.get_response_body(f"{self.BASE_URL}/products/-1")
        self.assertTrue("404" in response or "Not Found" in response)

    def test_get_product_by_zero_id_returns_404(self):
        response = self.get_response_body(f"{self.BASE_URL}/products/0")
        self.assertTrue("404" in response or "Not Found" in response)

    def test_get_product_by_non_numeric_id_returns_400(self):
        response = self.get_response_body(f"{self.BASE_URL}/products/abc")
        self.assertTrue("400" in response or "Bad Request" in response)

    def test_delete_product_by_id_1_removes_product(self):
        self.make_delete_request(f"{self.BASE_URL}/products/delete/1")
        response = self.get_response_body(f"{self.BASE_URL}/products")
        self.assertFalse(self.json_contains_product(response, "Phone"))

    def test_delete_product_by_id_2_removes_product(self):
        self.make_delete_request(f"{self.BASE_URL}/products/delete/2")
        response = self.get_response_body(f"{self.BASE_URL}/products")
        self.assertFalse(self.json_contains_product(response, "Charger"))

    def test_delete_product_by_id_3_removes_product(self):
        self.make_delete_request(f"{self.BASE_URL}/products/delete/3")
        response = self.get_response_body(f"{self.BASE_URL}/products")
        self.assertFalse(self.json_contains_product(response, "Pen"))

    def test_delete_product_by_invalid_id_returns_404(self):
        status_code, response_body = self.make_delete_request(f"{self.BASE_URL}/products/delete/999")
        self.assertEqual(status_code, 404)
        self.assertTrue("Not Found" in response_body)

    def test_delete_product_by_negative_id_returns_404(self):
        status_code, response_body = self.make_delete_request(f"{self.BASE_URL}/products/delete/-1")
        self.assertEqual(status_code, 404)
        self.assertTrue("Not Found" in response_body)

    def test_delete_product_by_zero_id_returns_404(self):
        status_code, response_body = self.make_delete_request(f"{self.BASE_URL}/products/delete/0")
        self.assertEqual(status_code, 404)
        self.assertTrue("Not Found" in response_body)

    def test_delete_product_by_non_numeric_id_returns_400(self):
        status_code, response_body = self.make_delete_request(f"{self.BASE_URL}/products/delete/abc")
        self.assertEqual(status_code, 400)
        self.assertTrue("Bad Request" in response_body)

    def test_get_products_after_deleting_id_1_returns_two_products(self):
        self.make_delete_request(f"{self.BASE_URL}/products/delete/1")
        response = self.get_response_body(f"{self.BASE_URL}/products")
        products = json.loads(response)
        self.assertEqual(len(products), 2)

    def test_delete_product_twice_returns_404_on_second_attempt(self):
        self.make_delete_request(f"{self.BASE_URL}/products/delete/1")
        status_code, _ = self.make_delete_request(f"{self.BASE_URL}/products/delete/1")
        self.assertEqual(status_code, 404)

    def test_get_product_after_deletion_returns_404(self):
        self.make_delete_request(f"{self.BASE_URL}/products/delete/1")
        response = self.get_response_body(f"{self.BASE_URL}/products/1")
        self.assertTrue("404" in response or "Not Found" in response)

    def test_get_products_returns_empty_list_after_deleting_all_products(self):
        self.make_delete_request(f"{self.BASE_URL}/products/delete/1")
        self.make_delete_request(f"{self.BASE_URL}/products/delete/2")
        self.make_delete_request(f"{self.BASE_URL}/products/delete/3")
        response = self.get_response_body(f"{self.BASE_URL}/products")
        self.assertEqual(response.strip(), "[]")

    def test_get_products_with_invalid_query_params(self):
        response = self.get_response_body(f"{self.BASE_URL}/products?invalid=xyz")
        products = json.loads(response)
        self.assertEqual(len(products), 3)

    def test_delete_malformed_url_returns_404(self):
        status_code, response_body = self.make_delete_request(f"{self.BASE_URL}/products/delete/")
        self.assertEqual(status_code, 404)
        self.assertTrue("Not Found" in response_body)

    def test_empty_list_strict_check(self):
        self.make_delete_request(f"{self.BASE_URL}/products/delete/1")
        self.make_delete_request(f"{self.BASE_URL}/products/delete/2")
        self.make_delete_request(f"{self.BASE_URL}/products/delete/3")
        response = self.get_response_body(f"{self.BASE_URL}/products")
        products = json.loads(response)
        self.assertEqual(products, [])

    def test_reset_response_status(self):
        req = urllib.request.Request(f"{self.BASE_URL}/reset", method="POST")
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.getcode(), 200)

    def test_get_products_response_time(self):
        start_time = time.time()
        self.get_response_body(f"{self.BASE_URL}/products")
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 1.0)

    def test_get_product_by_id_response_time(self):
        start_time = time.time()
        self.get_response_body(f"{self.BASE_URL}/products/1")
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 1.0)

    def test_delete_product_response_time(self):
        start_time = time.time()
        self.make_delete_request(f"{self.BASE_URL}/products/delete/1")
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 1.0)

    def test_reset_response_time(self):
        start_time = time.time()
        req = urllib.request.Request(f"{self.BASE_URL}/reset", method="POST")
        urllib.request.urlopen(req).close()
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 1.0)

    def test_get_products_json_structure(self):
        response = self.get_response_body(f"{self.BASE_URL}/products")
        products = json.loads(response)
        self.assertTrue(all("id" in p and "content" in p for p in products))

    def test_multiple_reset_calls(self):
        for _ in range(3):
            req = urllib.request.Request(f"{self.BASE_URL}/reset", method="POST")
            urllib.request.urlopen(req).close()
        response = self.get_response_body(f"{self.BASE_URL}/products")
        products = json.loads(response)
        self.assertEqual(len(products), 3)

if __name__ == "__main__":
    unittest.main(verbosity=2)