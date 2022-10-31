"""unittest module"""
from unittest import TestCase, main
from pymeter.api import ContentType
from pymeter.api.config import TestPlan, ThreadGroupSimple
from pymeter.api.samplers import HttpSampler
from pymeter.api.timers import ConstantTimer


class TestSampler(TestCase):
    """Testing creation of a http sampler object"""

    def test_http_sampler(self):
        # TODO: implement a way to extract output
        """send request to postman echo"""
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1")
        tg1 = ThreadGroupSimple(1, 1, http_sampler)
        test_plan = TestPlan(tg1)
        test_plan.run()
        self.assertEqual(
            http_sampler.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.http.DslHttpSampler",
        )

    def test_http_sampler_with_valid_children(self):
        """send request to postman echo"""
        timer = ConstantTimer(1000)
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1", timer)
        self.assertEqual(
            http_sampler.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.http.DslHttpSampler",
        )

    def test_http_sampler_with_valid_children_out_of_constructor(self):
        """send request to postman echo"""
        timer = ConstantTimer(1000)
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1")
        http_sampler.children(timer)
        self.assertEqual(
            http_sampler.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.http.DslHttpSampler",
        )

    def test_post_http_sampler_dict_input(self):

        http_sampler = HttpSampler(
            "Echo",
            "https://jsonplaceholder.typicode.com/posts",
        ).post({"var1": 1}, ContentType.APPLICATION_JSON)
        self.assertEqual(
            http_sampler.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.http.DslHttpSampler",
        )

    def test_post_http_sampler_list_input(self):

        http_sampler = HttpSampler(
            "Echo",
            "https://jsonplaceholder.typicode.com/posts",
        ).post([1, 2, 3, 4], ContentType.APPLICATION_JSON)
        self.assertEqual(
            http_sampler.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.http.DslHttpSampler",
        )

    def test_post_http_sampler_str_input(self):

        http_sampler = HttpSampler(
            "Echo",
            "https://jsonplaceholder.typicode.com/posts",
        ).post('{"name": "John Doe"}', ContentType.APPLICATION_JSON)
        self.assertEqual(
            http_sampler.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.http.DslHttpSampler",
        )

    def test_post_http_sampler_int_input(self):

        with self.assertRaises(TypeError) as exp:
            http_sampler = HttpSampler(
                "Echo",
                "https://jsonplaceholder.typicode.com/posts",
            ).post(1, ContentType.APPLICATION_JSON)
            self.assertEqual(
                http_sampler.get_java_class_name(),
                "us.abstracta.jmeter.javadsl.http.DslHttpSampler",
            )
        self.assertEqual(
            str(exp.exception),
            "Invalid type, expected `list`, 'dict', or 'str'. got <class 'int'>",
        )

    def test_http_valid_header(self):

        http_sampler = HttpSampler(
            "Echo",
            "https://jsonplaceholder.typicode.com/posts",
        ).header("key1", "val1")
        self.assertEqual(
            http_sampler.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.http.DslBaseHttpSampler",
        )

    def test_http_2_headers(self):

        http_sampler = (
            HttpSampler(
                "Echo",
                "https://jsonplaceholder.typicode.com/posts",
            )
            .header("key1", "val1")
            .header("key2", "val2")
        )
        self.assertEqual(
            http_sampler.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.http.DslBaseHttpSampler",
        )

    def test_http_duplicated_header(self):

        http_sampler = (
            HttpSampler(
                "Echo",
                "https://jsonplaceholder.typicode.com/posts",
            )
            .header("key1", "val1")
            .header("key1", "val2")
        )
        self.assertEqual(
            http_sampler.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.http.DslBaseHttpSampler",
        )

    def test_http_invalid_header_key(self):

        with self.assertRaises(TypeError) as exp:
            http_sampler = HttpSampler(
                "Echo",
                "https://jsonplaceholder.typicode.com/posts",
            ).header(1, "aa")
            self.assertEqual(
                http_sampler.get_java_class_name(),
                "us.abstracta.jmeter.javadsl.http.DslBaseHttpSampler",
            )
        self.assertEqual(
            str(exp.exception),
            "key field must be a string",
        )

    def test_http_invalid_header_value(self):

        with self.assertRaises(TypeError) as exp:
            http_sampler = HttpSampler(
                "Echo",
                "https://jsonplaceholder.typicode.com/posts",
            ).header("key1", 1)
            self.assertEqual(
                http_sampler.get_java_class_name(),
                "us.abstracta.jmeter.javadsl.http.DslBaseHttpSampler",
            )
        self.assertEqual(
            str(exp.exception),
            "value field must be a string",
        )


if __name__ == "__main__":
    main()
