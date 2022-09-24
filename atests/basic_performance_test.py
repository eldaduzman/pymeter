"""run a basic test with pytest"""

from pymeter.api.reporters import HtmlReporter
from pymeter.api.timers import UniformRandomTimer
from pymeter.api.config import TestPlan, ThreadGroup
from pymeter.api.samplers import HttpSampler


def main():
    timer = UniformRandomTimer(100, 200)
    http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1", timer)
    tg = ThreadGroup(10, 1, 30, http_sampler)
    html_reporter = HtmlReporter()
    tp = TestPlan(tg, html_reporter)
    stats = tp.run()


if __name__ == "__main__":
    main()
