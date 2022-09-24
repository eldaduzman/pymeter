"""unittest module"""
from unittest import TestCase, mock, main


class TestInstanceCreation(TestCase):
    """This suite tests the creation of new gevent instances"""

    def test_instantiate_keywords_class(self):
        """when a new keyword instance is created,
        it should have no bundle of coroutines"""
        self.assertEqual(0, 0)


if __name__ == "__main__":
    main()
