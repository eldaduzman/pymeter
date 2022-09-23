from typing import Optional
from jnius import autoclass, JavaException

from pymeter.api import BaseJMeterClass
from pymeter.api.timers import BaseTimer


class BaseSampler(BaseJMeterClass):
    ...


class HttpSampler(BaseSampler):
    def __init__(self, name:str, url:str, timer: Optional[BaseTimer] = None) -> None:
        self._http_sampler_instance = BaseSampler.jmeter_class.httpSampler(name, url)
        if timer:
            self._http_sampler_instance.children(timer.java_wrapped_element)
        super().__init__()