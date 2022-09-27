"""this module defines all the test samplers,
which are the steps taken in a load test script"""
import json
from typing import Dict, List, Union

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from pymeter.api import ThreadGroupChildElement, ContentType


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

    def post(self, body: Union[Dict, List, str], content_type: ContentType) -> Self:
        """create a post request sampler"""

        if isinstance(body, dict) or isinstance(body, list):
            body = json.dumps(body)
        elif not isinstance(body, str):
            raise TypeError(
                f"Invalid type, expected `list`, 'dict', or 'str'. got {type(body)}"
            )

        self._http_sampler_instance = self.java_wrapped_element.post(
            body, content_type.value
        )
        return self
