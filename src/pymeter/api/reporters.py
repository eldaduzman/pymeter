import os
from datetime import datetime
from typing import Optional

from pymeter.api import BaseJMeterClass


class BaseReporter(BaseJMeterClass):
    ...


class HtmlReporter(BaseReporter):
    def __init__(self, directory: Optional[str] = None) -> None:

        directory = directory or os.path.join(
            "output", f'html-report-{datetime.now().strftime("%m%d%Y%H%M%S")}'
        )
        self._html_reporter_instance = HtmlReporter.jmeter_class.htmlReporter(directory)
        super().__init__()
