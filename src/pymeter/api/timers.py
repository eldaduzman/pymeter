"""timers are used to control the time flow of our load test"""
from pymeter.api import BaseJMeterClass


class BaseTimer(BaseJMeterClass):
    "base class for all timers"


class UniformRandomTimer(BaseTimer):
    """Randomizes wait times with uniform distribution"""
    def __init__(self, bottom_milliseconds: int, top_milliseconds: int) -> None:
        self._uniform_random_timer_instance = (
            UniformRandomTimer.jmeter_class.uniformRandomTimer(
                bottom_milliseconds, top_milliseconds
            )
        )
        super().__init__()
