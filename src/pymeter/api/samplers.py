"""this module defines all the test samplers,
which are the steps taken in a load test script"""
from pymeter.api import ThreadGroupChildElement


class BaseSampler(ThreadGroupChildElement):
    """base class for all samplers"""


class DummySampler(BaseSampler):
    """class for the dummy sampler objects"""

    def __init__(self, name: str, response_body: str, *children) -> None:
        self._dummy_sampler_instance = BaseSampler.jmeter_class.dummySampler(
            name, response_body
        )
        self._dummy_sampler_instance.children(
            *[c.java_wrapped_element for c in children]
        )
        super().__init__()


class HttpSampler(BaseSampler):
    """Http sampler sends http requests to a target server side"""

    def __init__(self, name: str, url: str, *children) -> None:
        self._http_sampler_instance = BaseSampler.jmeter_class.httpSampler(name, url)
        self._http_sampler_instance.children(
            *[c.java_wrapped_element for c in children]
        )
        super().__init__()
