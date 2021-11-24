from django.test import TestCase, Client, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token

from .models import Article
from .views import ArticleListView


class ArticlesTestCase(TestCase):
    def setUp(self) -> None:
        user_model = get_user_model()
        self.user = user_model.objects.create(city='Here', password='123_dfg456')

    def test_page(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_page_exist_user(self):
        rf = RequestFactory()
        request = rf.get('')
        request.user = self.user
        response = ArticleListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
