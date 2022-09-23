from typing import Optional

from pymeter.api import BaseJMeterClass


class BaseSampler(BaseJMeterClass):
    ...


class HttpSampler(BaseSampler):
    def __init__(self, name: str, url: str, *children) -> None:
        self._http_sampler_instance = BaseSampler.jmeter_class.httpSampler(name, url)
        self._http_sampler_instance.children(
            *[c.java_wrapped_element for c in children]
        )
        super().__init__()
