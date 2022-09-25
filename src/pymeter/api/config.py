"""configuration elements"""
from jnius import JavaException

from pymeter.api import TestPlanChildElement, ThreadGroupChildElement


class BaseConfigElement(TestPlanChildElement):
    """base class for all config elements"""


class TestPlan(BaseConfigElement):
    """wrapper for the test plan object"""

    class TestPlanStats(BaseConfigElement):
        """test stats"""

        def __init__(self, java_instance) -> None:
            self._test_plan_stats_instance = java_instance
            super().__init__()

        @property
        def sample_time_mean_milliseconds(self):
            """returns the mean of sample times in milliseconds"""
            return self.java_wrapped_element.overallStats.sampleTime().mean().toMillis()

        @property
        def sample_time_min_milliseconds(self):
            """returns the min of sample times in milliseconds"""
            return self.java_wrapped_element.overallStats.sampleTime().min().toMillis()

        @property
        def sample_time_median_milliseconds(self):
            """returns the median of sample times in milliseconds"""
            return (
                self.java_wrapped_element.overallStats.sampleTime().median().toMillis()
            )

        @property
        def sample_time_90_percentile_milliseconds(self):
            """returns the 90th percentile of sample times in milliseconds"""
            return (
                self.java_wrapped_element.overallStats.sampleTime().perc90().toMillis()
            )

        @property
        def sample_time_95_percentile_milliseconds(self):
            """returns the 95th percentile of sample times in milliseconds"""
            return (
                self.java_wrapped_element.overallStats.sampleTime().perc95().toMillis()
            )

        @property
        def sample_time_99_percentile_milliseconds(self):
            """returns the 99th percentile of sample times in milliseconds"""
            return (
                self.java_wrapped_element.overallStats.sampleTime().perc99().toMillis()
            )

        @property
        def sample_time_max_milliseconds(self):
            """returns the max of sample times in milliseconds"""
            return self.java_wrapped_element.overallStats.sampleTime().max().toMillis()

        @property
        def duration(self):
            """returns the max of sample times in milliseconds"""
            return self.java_wrapped_element.duration().toMillis()

    def __init__(self, *children: TestPlanChildElement) -> None:
        if not all(isinstance(c, TestPlanChildElement) for c in children):
            raise TypeError("only takes children of type `TestPlanChildElement`")
        self._test_plan_instance = BaseConfigElement.jmeter_class.testPlan()
        if children:
            self._test_plan_instance.children(
                *[c.java_wrapped_element for c in children]
            )
        super().__init__()

    def run(self):
        """execute the test plan"""
        try:
            return TestPlan.TestPlanStats(self._test_plan_instance.run())
        except JavaException as java_exception:
            print("\n\t at ".join(java_exception.stacktrace))
            raise java_exception


class BaseThreadGroup(BaseConfigElement):
    """base class for all thread groups"""

    def __init__(self, *children: ThreadGroupChildElement) -> None:
        if not all(isinstance(c, ThreadGroupChildElement) for c in children):
            raise TypeError("only takes children of type `ThreadGroupChildElement`")
        super().__init__()


class ThreadGroupSimple(BaseThreadGroup):
    """Thread group defined by number of threads and number of iterations"""

    def __init__(
        self,
        number_of_threads: int,
        iterations: int,
        *children: ThreadGroupChildElement,
        name: str = "Thread Group"
    ) -> None:
        super().__init__(*children)
        self._thread_group_simple_instance = BaseConfigElement.jmeter_class.threadGroup(
            name, number_of_threads, iterations
        )
        if children:
            self._thread_group_simple_instance.children(
                *[c.java_wrapped_element for c in children]
            )


class ThreadGroupWithRampUpAndHold(BaseThreadGroup):
    """A wrapper for the thread group"""

    def __init__(
        self,
        number_of_threads: int,
        rampup_time_seconds: float,
        holdup_time_seconds: float,
        *children,
        name: str = "Thread Group"
    ) -> None:
        super().__init__(*children)
        self._thread_group_with_ramp_up_and_hold_instance = (
            BaseConfigElement.jmeter_class.threadGroup(name)
        )
        self._ramp_to_and_hold_instance = (
            self._thread_group_with_ramp_up_and_hold_instance.rampToAndHold(
                number_of_threads,
                BaseConfigElement.java_duration.ofSeconds(rampup_time_seconds),
                BaseConfigElement.java_duration.ofSeconds(holdup_time_seconds),
            )
        )
        if children:
            self._ramp_to_and_hold_instance.children(
                *[c.java_wrapped_element for c in children]
            )
