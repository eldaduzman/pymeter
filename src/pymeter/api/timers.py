"""
Timers are used to pause the thread for a given amount of time.
The goal is to emulate either a user think time or any other time related aspect of the test script.

.. note::
    Timers apply to all samplers in their scope.

.. note::
    Note that timers are processed before each sampler in the scope in which they are found; if there are several timers in the same scope, all the timers will be processed before each sampler.
    Timers are only processed in conjunction with a sampler. A timer which is not in the same scope as a sampler will not be processed at all.

example - 1:
--------------
This uniform random timer is used for each HTTP request in this test script


      .. code-block:: python

            from pymeter.api.config import TestPlan, ThreadGroupSimple
            from pymeter.api.samplers import HttpSampler
            from pymeter.api.timers import UniformRandomTimer

            timer = UniformRandomTimer(2000, 5000)
            http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1", timer)
            thread_group = ThreadGroupSimple(1, 1, http_sampler)
            test_plan = TestPlan(thread_group)
            stats = test_plan.run()

example - 2:
--------------
This uniform random timer is used for the entire thread group


      .. code-block:: python

            from pymeter.api.config import TestPlan, ThreadGroupSimple
            from pymeter.api.samplers import HttpSampler
            from pymeter.api.timers import UniformRandomTimer

            timer = UniformRandomTimer(2000, 5000)
            http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1")
            thread_group = ThreadGroupSimple(1, 1, http_sampler, timer)
            test_plan = TestPlan(thread_group)
            stats = test_plan.run()
"""
from pymeter.api import ThreadGroupChildElement


class BaseTimer(ThreadGroupChildElement):
    "base class for all timers"


class UniformRandomTimer(BaseTimer):
    """
    Randomizes wait times with uniform distribution


    .. note::
        UniformRandomTimer minimum and maximum parameters differ from the ones used by JMeter Uniform Random Timer element,
        to make it simpler for users with no JMeter background.
    """

    def __init__(self, bottom_milliseconds: int, top_milliseconds: int) -> None:
        self._uniform_random_timer_instance = (
            UniformRandomTimer.jmeter_class.uniformRandomTimer(
                bottom_milliseconds, top_milliseconds
            )
        )
        super().__init__()
