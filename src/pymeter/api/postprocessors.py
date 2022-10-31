"""
Post processors are attached to samplers and are executed after the parent sampler gets executed.
The most common use case for a post-processor is to add value on the response coming from the sampler.

example - 1:
--------------
*Correlation* is when the response (or some parts of it) of one sampler is used in subsequent samplers.
Lets look at an example to how we can do that with the JsonExtractor post-processor

      .. code-block:: python

        # Json extractor will take the value stored in the json paht args->var and place it in a variable called `variable`

        json_extractor = JsonExtractor("variable", "args.var")
        http_sampler = HttpSampler(
            "Echo", "https://postman-echo.com/get?var=1", json_extractor
        )

        # The extracted value is now used to define the name of the dummy sampler.
        dummy_sampler = DummySampler("dummy ${variable}", "hi dummy")
        thread_group = ThreadGroupSimple(1, 1, http_sampler, dummy_sampler)
        test_plan = TestPlan(thread_group)
        test_plan.run()

"""
from pymeter.api import ChildrenAreNotAllowed, ThreadGroupChildElement


class BasePostProcessors(ThreadGroupChildElement):
    """base class for all post processors"""
    def children(self, *children):
        raise ChildrenAreNotAllowed("Cant append children to a post processor")


class JsonExtractor(BasePostProcessors):
    """
    Extracts a value from a json response using a json path.
    Read more about json path `here <https://support.smartbear.com/alertsite/docs/monitors/api/endpoint/jsonpath.html>`_
    """

    def __init__(self, variable_name: str, jmes_path: str) -> None:
        self._json_extractor_instance = BasePostProcessors.jmeter_class.jsonExtractor(
            variable_name, jmes_path
        )

        super().__init__()
