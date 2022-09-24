"""configuration elements"""
from jnius import JavaException

from pymeter.api import BaseJMeterClass


class BaseConfigElement(BaseJMeterClass):
    """base class for all config elements"""


class TestPlan(BaseConfigElement):
    """wrapper for the test plan object"""

    def __init__(self, *children) -> None:
        self._test_plan_instance = BaseConfigElement.jmeter_class.testPlan()
        java_children = [c.java_wrapped_element for c in children]
        self._test_plan_instance.children(*java_children)
        super().__init__()

    def run(self):
        """execute the test plan"""
        try:
            return self._test_plan_instance.run()
        except JavaException as java_exception:
            print("\n\t at ".join(java_exception.stacktrace))
            raise java_exception


class ThreadGroup(BaseConfigElement):
    """A wrapper for the thread group"""

    def __init__(
        self,
        number_of_threads: int,
        rampup_time_seconds: float,
        holdup_time_seconds: float,
        *children
    ) -> None:
        self._thread_group_instance = BaseConfigElement.jmeter_class.threadGroup()
        self._ramp_to_and_hold_instance = self._thread_group_instance.rampToAndHold(
            number_of_threads,
            BaseConfigElement.java_duration.ofSeconds(rampup_time_seconds),
            BaseConfigElement.java_duration.ofSeconds(holdup_time_seconds),
        )
        self._ramp_to_and_hold_instance.children(
            *[c.java_wrapped_element for c in children]
        )
        super().__init__()
