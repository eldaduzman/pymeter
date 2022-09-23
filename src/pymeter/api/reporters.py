from datetime import datetime
from typing import Optional

from jnius import JavaException, autoclass
from pymeter.api import BaseJMeterClass


class BaseReporter(BaseJMeterClass):
    ...


class HtmlReporter(BaseReporter):
    def __init__(self, directory: Optional[str] = None) -> None:

        directory = (
            directory or f'html-report-{datetime.now().strftime("%m%d%Y%H%M%S")}'
        )
        self._html_reporter_instance = HtmlReporter.jmeter_class.htmlReporter(directory)
        super().__init__()
