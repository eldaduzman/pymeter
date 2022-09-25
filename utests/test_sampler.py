"""unittest module"""
from unittest import TestCase, main
from pymeter.api.config import TestPlan, ThreadGroupSimple
from pymeter.api.samplers import HttpSampler


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
            str(type(http_sampler.java_wrapped_element)),
            "<class 'jnius.reflect.us.abstracta.jmeter.javadsl.http.DslHttpSampler'>",
        )


if __name__ == "__main__":
    main()
