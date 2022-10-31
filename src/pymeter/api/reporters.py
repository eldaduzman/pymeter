"""
Reporters represent measurements about the samplers for testers to analyze.

example - 1:
--------------
HTML reporter creates a JMeter html dashboard
You can read more about JMeter's dashboard `here <https://jmeter.apache.org/usermanual/generating-dashboard.html>`_

By default, resulting dashboard will be saved at output/html-report-{current-date %m%d%Y%H%M%S}
      .. code-block:: python

            from pymeter.api.config import TestPlan, ThreadGroupWithRampUpAndHold
            from pymeter.api.reporters import HtmlReporter
            from pymeter.api.samplers import HttpSampler


            http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1")
            thread_group = ThreadGroupWithRampUpAndHold(2, 1, 2, http_sampler)
            html_reporter = HtmlReporter()
            test_plan = TestPlan(thread_group, html_reporter)
            test_plan.run()

example - 2:
--------------
You can override the directory in the object's constructor.

By default, resulting dashboard will be saved at output/html-report-{current-date %m%d%Y%H%M%S}
      .. code-block:: python

            html_reporter = HtmlReporter("somefolder")

"""
import os
from datetime import datetime
from typing import Optional

from pymeter.api import ChildrenAreNotAllowed, TestPlanChildElement

class BaseReporter(TestPlanChildElement):
    """base class for all reporters"""
    def children(self, *children):
        raise ChildrenAreNotAllowed("Cant append children to a reporter")


class HtmlReporter(BaseReporter):
    """Reports results to HTML format"""

    def __init__(self, directory: Optional[str] = None) -> None:
        if directory:
            path_parts = os.path.split(directory)
            self._html_reporter_instance = HtmlReporter.jmeter_class.htmlReporter(
                os.path.join(*path_parts[0 : len(path_parts) - 1]), path_parts[-1]
            )
        else:

            self._html_reporter_instance = HtmlReporter.jmeter_class.htmlReporter(
                "output", f'html-report-{datetime.now().strftime("%m%d%Y%H%M%S")}'
            )
        super().__init__()
