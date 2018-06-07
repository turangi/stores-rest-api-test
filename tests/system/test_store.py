import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test')

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'items': []},
                                     json.loads(resp.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                resp = client.post('/store/test')

                self.assertEqual(resp.status_code, 400)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.delete('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'},
                                     json.loads(resp.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/store/test')

                self.assertEqual(resp.status_code, 200)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/store/no_such_store')

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(resp.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()

                resp = client.get('/store/test')  # returns json of the store, which includes items
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'test', 'items': [{'name': 'test_item', 'price': 19.99}]},
                                     json.loads(resp.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.get('/stores')
                self.assertDictEqual({'stores': [{'name': 'test', 'items': []}]},
                                     json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()  # adding some actual items to the store

                resp = client.get('/stores')
                self.assertDictEqual({'stores': [{'name': 'test', 'items': [{'name': 'test_item', 'price': 19.99}]}]},
                                     json.loads(resp.data))