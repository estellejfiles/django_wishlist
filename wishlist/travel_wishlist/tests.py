from django.test import TestCase
from django.urls import reverse

from .models import Place

# Create your tests here.

# home page test
class TestHomePage(TestCase):
    # test that home page displays empty list when no places have been added
    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')

# wishlist test
class TestWishlist(TestCase):
    fixtures = ['test_places']
    # assert that correct wishlist places are being shown using data from fixtures
    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

# visited page test if no places have been visited
class TestVisitedPage(TestCase):
    # test that visited page shows message when no places have been visited
    def test_visited_page_shows_empty_list_message_for_empty_database(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet')

# correct visited list test
class VisitedList(TestCase):
    fixtures = ['test_places']
    # test that correct visited places are being shown using data from fixtures
    def test_visited_list_shows_visited_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'New York')
        self.assertNotContains(response, 'Tokyo')

# adding new place test
class TestNewPlace(TestCase):
    # test that new unvisited place can be added to wishlist
    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        response_places = response.context['places']
        # assert only one place is added in list
        self.assertEqual(1, len(response_places))
        # dictionary index 0 from rendered template is tokyo
        tokyo_from_response = response_places[0]
        # retrieve tokyo from database
        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)
        # assert that tokyo from database is same as tokyo from rendered template
        self.assertEqual(tokyo_from_database, tokyo_from_response)

# visit request test
class TestVisitPlace(TestCase):
    fixtures = ['test_places']
    # test that place can be marked as visited
    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, ))
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)

    # test place that does not exist
    def test_non_existent_place(self):
        visit_nonexistent_place_url = reverse('place_was_visited', args=(123456, ))
        response = self.client.post(visit_nonexistent_place_url, follow=True)
        self.assertEqual(404, response.status_code)