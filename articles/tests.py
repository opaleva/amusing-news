from django.test import TestCase, Client


class ArticlesTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_page(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

