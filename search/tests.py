from mock import patch

from django.test import TestCase, Client

# Create your tests here.


class SearchTestCase(TestCase):

    @patch('urllib2.OpenerDirector')
    def test_wrong_format_api_response(self, mock_opener):
        mock_opener.return_value.open.return_value = """
        {"something": "wrong"}
        """

        c = Client()
        response = c.get('/search/', {'search_term': 'someterm'})

        self.assertTrue(response.context['error'])

    @patch('urllib2.OpenerDirector')
    def test_mangled_api_response(self, mock_opener):
        mock_opener.return_value.open.return_value = """
        "sometsdlkfjsdfkjlhing":sdfdsf: wrong"
        """

        c = Client()
        response = c.get('/search/', {'search_term': 'someterm'})

        self.assertTrue(response.context['error'])

    @patch('urllib2.OpenerDirector')
    def test_proper_api_response(self, mock_opener):
        mock_opener.return_value.open.return_value = """
        {
        "search":
            {
                "results":
                [
                    {
                        "title": "Andrew Product",
                        "price": {"listPriceText": "500 GBP"},
                        "averageRatingText": "5.00"
                    }
                ]
            }
        }
        """

        c = Client()
        response = c.get('/search/', {'search_term': 'andrew'})

        self.assertFalse(response.context['error'])
        self.assertEqual(
            response.context['items'][0]['title'], "Andrew Product")
        self.assertEqual(
            response.context['items'][0]['price']['listPriceText'], "500 GBP")
        self.assertEqual(
            response.context['items'][0]['averageRatingText'], "5.00")

    @patch('urllib2.OpenerDirector')
    def test_no_results_api_response(self, mock_opener):
        mock_opener.return_value.open.return_value = """
        {
        "search":
            {
                "results":
                []
            }
        }
        """

        c = Client()
        response = c.get('/search/', {'search_term': 'andrew'})

        self.assertFalse(response.context['error'])
        self.assertEqual(response.context['items'], [])