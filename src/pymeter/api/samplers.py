"""
Samplers are the basic test script steps.

They perform a specific action (eg, send an HTTP request) and report their time of completion,
in other words, they are the subject which our test measure.

example - 1:
--------------
The most commonly used sampler is the HTTP sampler, lets take a look at a trivial example:
In this example, our http sampler generates a get request to the postman echo server


      .. code-block:: python

            from pymeter.api.samplers import HttpSampler
            http_sampler = HttpSampler("echo_get_request", "https://postman-echo.com/get?var=1")

example - 2:
--------------
Lets add a header to the request:
Here the headers name is `SomeKey` and it's value is `some_value`

      .. code-block:: python

        from pymeter.api.samplers import HttpSampler
        http_sampler = HttpSampler("echo_get_request", "https://postman-echo.com/get?var=1").header("SomeKey", "some_value")



example - 3:
--------------
Now lets send a post request:
This post request has an application-json as a content type, and the body has a single value with `var1` being the key and 1 being the value


      .. code-block:: python

            from pymeter.api import ContentType
            from pymeter.api.samplers import HttpSampler

            http_sampler = (
                HttpSampler("echo_get_request", "https://postman-echo.com/get?var=1")
                .header("SomeKey", "some_value")
                .post({"var1": 1}, ContentType.APPLICATION_JSON)
            )

example - 4:
--------------
The Dummy Sampler in JMeter simulates requests to the server without actually running the requests,
serving as a placeholder.


      .. code-block:: python

            from pymeter.api.samplers import DummySampler
            dummy_sampler = DummySampler("dummy_sampler", "hi dummy")

example - 5:
--------------
Lets send a post request with multipart/form-data:
This post request has a multipart/form-data as a content type, and the body has a single file with `name` being the key and `path/to/file.ext` being the file_path


      .. code-block:: python

            from pymeter.api import ContentType
            from pymeter.api.samplers import HttpSampler

            http_sampler = (
                HttpSampler("echo_get_request", "http://httpbin.org/post")
                .post_multipart_formdata("name", "path/to/file.ext", ContentType.MULTIPART_FORM_DATA)
            )

"""
import json
import os
from typing import Dict, List, Union


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from pymeter.api import ThreadGroupChildElement, ContentType
from pymeter.api.config import BaseThreadGroup


class BaseSampler(ThreadGroupChildElement, BaseThreadGroup):
    """base class for all samplers"""


class DummySampler(BaseSampler):
    """
    The Dummy Sampler in JMeter simulates requests to the server without actually running the requests,
    serving as a placeholder.
    """

    def __init__(self, name: str, response_body: str, *children) -> None:
        self._dummy_sampler_instance = BaseSampler.jmeter_class.dummySampler(
            name, response_body
        )
        super().__init__(*children)


class HttpSampler(BaseSampler):
    """
    Http sampler sends an http requests to a target server side
    By default it sends HTTP get request
    """

    def __init__(self, name: str, url: str, *children) -> None:
        """

        Args:

            name (str): name to be displayed in reports

            url (str): Full http\\s url (e.g - https://postman-echo.com/get)
        """
        self._http_sampler_instance = BaseSampler.jmeter_class.httpSampler(name, url)

        super().__init__(*children)

    def post(self, body: Union[Dict, List, str], content_type: ContentType) -> Self:
        """Create a post request sampler

        Args:

            body (Union[Dict, List, str]): body of the request

            content_type (ContentType): the content type of the request


        Returns:

            Self: a new sampler instance
        """

        if isinstance(body, (dict, list)):
            body = json.dumps(body)
        elif not isinstance(body, str):
            raise TypeError(
                f"Invalid type, expected `list`, 'dict', or 'str'. got {type(body)}"
            )

        self._http_sampler_instance = self.java_wrapped_element.post(
            body, content_type.value
        )
        return self

    def header(self, key: str, value: str) -> Self:
        """Append a header to request

        Args:

            key (str): Headers name
            value (str): Headers value


        Returns:

            Self: a new sampler instance
        """
        if not isinstance(key, str):
            raise TypeError("key field must be a string")
        if not isinstance(value, str):
            raise TypeError("value field must be a string")
        self._http_sampler_instance = self.java_wrapped_element.header(key, value)
        return self

    def post_multipart_formdata(self, name: str, file_path: str, content_type: ContentType) -> Self:
        """Create a post request sampler

        Args:

            name: the name to be assigned to the file part.

            file_path: path to the file to be sent in the multipart form body.

            content_type (ContentType): the content type of the request


        Returns:

            Self: a new sampler instance
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        self._http_sampler_instance = self.java_wrapped_element.bodyFilePart(
            name, file_path, content_type.value
        ).method("POST")
        return self
