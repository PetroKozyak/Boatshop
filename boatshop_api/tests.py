from django.urls import reverse
from unittest_data_provider import data_provider
from boatshop_api.test.base_test_case import BaseTestCase


class BoatCreateAPIViewTestCase(BaseTestCase):
    url = reverse("boats-list")

    createBoat = lambda: (
        (BaseTestCase.USER_ID_1, 'Victoria', 400, 201,),
        (BaseTestCase.USER_ID_4_NOT_EXIST, 'Test', 200, 401,),
        (BaseTestCase.USER_ID_2, None, 200, 400,),
        (BaseTestCase.USER_ID_3, "Boat", None, 400,),
        (BaseTestCase.USER_ID_1, None, None, 400,),
    )

    @data_provider(createBoat)
    def test_create_boat(self, user_id, boat_name, boat_price, response_code):
        self.before_test(user_id)
        data = {"boat": boat_name,
                "price": boat_price
                }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response_code, response.status_code)

    getBoats = lambda: (
        (BaseTestCase.USER_ID_1, 3, 200,),
        (BaseTestCase.USER_ID_4_NOT_EXIST, 0, 401,),
        (BaseTestCase.USER_ID_2, 3, 200,),
    )

    @data_provider(getBoats)
    def test_list_boats(self, user_id, items_count, response_code):
        self.before_test(user_id)
        response = self.client.get(self.url)
        self.assertEqual(response_code, response.status_code)
        if response_code == 200:
            self.assertEqual(len(response.json()), items_count)


class BoatDetailAPIViewTestCase(BaseTestCase):
    boat_detail = lambda: (
        (BaseTestCase.BOAT_ID_1, BaseTestCase.USER_ID_2, "Manda", 403),
        (BaseTestCase.BOAT_ID_2, BaseTestCase.USER_ID_2, "Manda", 200),
        (BaseTestCase.BOAT_ID_3, BaseTestCase.USER_ID_2, "Manda", 403),
    )

    @data_provider(boat_detail)
    def test_boat_object(self, boat_id, user_id, boat_name, response_code):
        self.before_test(user_id)
        self.url = reverse("boats-detail", kwargs={"pk": boat_id})

        response = self.client.put(self.url, {"boat": boat_name})
        self.assertEqual(response.status_code, response_code)

    boat_delete = lambda: (
        (BaseTestCase.BOAT_ID_1, BaseTestCase.USER_ID_2, 403),
        (BaseTestCase.BOAT_ID_2, BaseTestCase.USER_ID_2, 204),
        (BaseTestCase.BOAT_ID_3, BaseTestCase.USER_ID_2, 403),
    )

    @data_provider(boat_delete)
    def test_boat_delete(self, boat_id, user_id, response_code):
        self.before_test(user_id)
        response = self.client.delete(reverse("boats-detail", kwargs={'pk': boat_id}), format='json')
        self.assertEqual(response_code, response.status_code)


class OrderCreateAPIViewTestCase(BaseTestCase):
    url = reverse("orders-list")

    getListOrder = lambda: (
        (BaseTestCase.USER_ID_1, 3, 200,),
        (BaseTestCase.USER_ID_2, 3, 200,),
        (BaseTestCase.USER_ID_4_NOT_EXIST, 0, 401,),
        (BaseTestCase.USER_ID_3, 2, 200,),
    )

    @data_provider(getListOrder)
    def test_list_order(self, user_id, items_count, response_code):
        self.before_test(user_id)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response_code, response.status_code)
        if response_code == 200:
            self.assertEqual(len(response.json()), items_count)

    createOrder = lambda: (
        (BaseTestCase.USER_ID_1, BaseTestCase.BOAT_ID_1, 400,),
        (BaseTestCase.USER_ID_1, BaseTestCase.BOAT_ID_2, 201,),
        (BaseTestCase.USER_ID_2, BaseTestCase.BOAT_ID_4_NOT_EXIST, 400,),
        (BaseTestCase.USER_ID_2, BaseTestCase.BOAT_ID_2, 400,),
        (BaseTestCase.USER_ID_4_NOT_EXIST, BaseTestCase.BOAT_ID_2, 401,),
    )

    @data_provider(createOrder)
    def test_create_order(self, user_id, boat_id, response_code):
        self.before_test(user_id)
        response = self.client.post(self.url, {"boat": boat_id}, format='json')
        self.assertEqual(response_code, response.status_code)
        if response_code == 201:
            self.assertEqual(set(response.json().keys()), self.ORDER_KEYS)

    orders_detail = lambda: (
        (BaseTestCase.ORDER_ID_1, BaseTestCase.USER_ID_2, 204),
        (BaseTestCase.ORDER_ID_2, BaseTestCase.USER_ID_2, 404),
        (BaseTestCase.ORDER_ID_3, BaseTestCase.USER_ID_3, 204),
        (BaseTestCase.ORDER_ID_4, BaseTestCase.USER_ID_1, 204),
    )

    @data_provider(orders_detail)
    def test_order_delete(self, order_id, user_id, response_code):
        self.before_test(user_id)
        response = self.client.delete(reverse("orders-detail", kwargs={'pk': order_id}), format='json')
        self.assertEqual(response_code, response.status_code)
