"""
By default, JMeter marks any HTTP request with a fail response code (4xx or 5xx) as failed,
which allows you to easily identify when some request unexpectedly fails.

But in many cases, this is not enough or desirable,
and you need to check for the response body (or some other field) to contain (or not) a certain string.

This is usually accomplished in JMeter with the usage of Response Assertions,
which provides an easy and fast way to verify that you get the proper response for each step of the test plan,
marking the request as a failure when the specified condition is not met.

example - 1:
--------------
In this example we assert that the response contains the text "var"


      .. code-block:: python

            from pymeter.api.config import TestPlan, ThreadGroupSimple
            from pymeter.api.samplers import HttpSampler
            from pymeter.api.timers import ConstantTimer
            from pymeter.api.assertions import ResponseAssertion

            timer = ConstantTimer(2000)
            ra = ResponseAssertion().contains_substrings("var")
            http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1", timer, ra)
            thread_group = ThreadGroupSimple(1, 1)
            thread_group.children(http_sampler)
            test_plan = TestPlan(thread_group)
            stats = test_plan.run()

"""


from pymeter.api import ChildrenAreNotAllowed, ThreadGroupChildElement


class BaseAssertion(ThreadGroupChildElement):
    """base class for all assertions"""

    def children(self, *children):
        raise ChildrenAreNotAllowed("Cant append children to assertion")


class ResponseAssertion(BaseAssertion):
    """Assertion of the response element"""
    def __init__(self) -> None:
        self._response_assertion_instance = (
            ResponseAssertion.jmeter_class.responseAssertion()
        )

        super().__init__()

    def contains_substrings(self, *strings_to_look):
        """assert that the response contains string the given strings"""
        self._response_assertion_instance = (
            self._response_assertion_instance.containsSubstrings(*strings_to_look)
        )
        return self
