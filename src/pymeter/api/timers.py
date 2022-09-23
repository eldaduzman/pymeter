from jnius import autoclass, JavaException

from pymeter.api import BaseJMeterClass


class BaseTimer(BaseJMeterClass):
    ...


class UniformRandomTimer(BaseTimer):
    def __init__(self, bottom_milliseconds: int, top_milliseconds: int) -> None:
        self._uniform_random_timer_instance = (
            UniformRandomTimer.jmeter_class.uniformRandomTimer(
                bottom_milliseconds, top_milliseconds
            )
        )
        super().__init__()
