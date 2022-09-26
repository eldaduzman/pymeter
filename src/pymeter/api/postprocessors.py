"""this module defines all the test samplers,
which are the steps taken in a load test script"""
from pymeter.api import ThreadGroupChildElement


class BasePostProcessors(ThreadGroupChildElement):
    """base class for all post processors"""


class JsonExtractor(BasePostProcessors):
    """Http sampler sends http requests to a target server side"""

    def __init__(self, variable_name: str, jmes_path: str) -> None:
        self._json_extractor_instance = BasePostProcessors.jmeter_class.jsonExtractor(
            variable_name, jmes_path
        )

        super().__init__()
