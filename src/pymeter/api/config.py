from jnius import JavaException

from pymeter.api import BaseJMeterClass


class BaseConfigElement(BaseJMeterClass):
    ...


class TestPlan(BaseConfigElement):
    def __init__(self, *children) -> None:
        self._test_plan_instance = BaseConfigElement.jmeter_class.testPlan()
        java_children = [c.java_wrapped_element for c in children]
        self._test_plan_instance.children(*java_children)
        super().__init__()

    def run(self):

        try:
            self._test_plan_instance.run()
        except JavaException as ja:
            print("\n\t at ".join(ja.stacktrace))
            raise (ja)


class ThreadGroup(BaseConfigElement):
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
        self._ramp_to_and_hold_instance.children(*[c.java_wrapped_element for c in children])
        super().__init__()
