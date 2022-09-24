"""this module defines all the test samplers,
which are the steps taken in a load test script"""
from pymeter.api import BaseJMeterClass


class BaseSampler(BaseJMeterClass):
    """base class for all samplers"""


class HttpSampler(BaseSampler):
    """Http sampler sends http requests to a target server side"""
    def __init__(self, name: str, url: str, *children) -> None:
        self._http_sampler_instance = BaseSampler.jmeter_class.httpSampler(name, url)
        self._http_sampler_instance.children(
            *[c.java_wrapped_element for c in children]
        )
        super().__init__()
