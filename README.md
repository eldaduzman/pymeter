# pymeter
Simple JMeter performance tests API for python

[![Version](https://img.shields.io/pypi/v/pymeter.svg)](https://pypi.python.org/pypi/pymeter)
![](https://raw.githubusercontent.com/eldaduzman/pymeter/main/docs/badges/coverage-badge.svg?token=GHSAT0AAAAAABXHOUKX7CDKWJUQVFEEANY6YZRISTA)
![](https://raw.githubusercontent.com/eldaduzman/pymeter/main/docs/badges/pylint.svg?token=GHSAT0AAAAAABXHOUKXXRUTX7IO7LVMHVNCYZRITPQ)
![](https://raw.githubusercontent.com/eldaduzman/pymeter/main/docs/badges/mutscore.svg)

<img src="./docs/images/pymeter-logo-full.jpg" height="450" width="100%"/>

## Load testing with JMeter using python!

### Pre-requisites:
1. python version 3.9 or higher - [download](https://www.python.org/)
2. Java version 8 or 11 - [download](https://adoptium.net/temurin/releases)
3. JAVA_HOME environment variable set - [read](https://confluence.atlassian.com/doc/setting-the-java_home-variable-in-windows-8895.html)

### Install pymeter
```
>>> pip install pymeter
```

### simple pymeter script:

```
"""unittest module"""
from unittest import TestCase, main
from pymeter.api.reporters import HtmlReporter
from pymeter.api.timers import UniformRandomTimer
from pymeter.api.config import TestPlan, ThreadGroupWithRampUpAndHold
from pymeter.api.samplers import HttpSampler


class TestTestPlanClass(TestCase):
    def test_1(self):

        timer = UniformRandomTimer(100, 200)
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1", timer)
        tg = ThreadGroupWithRampUpAndHold(10, 1, 20, http_sampler, name="Some Name")
        html_reporter = HtmlReporter()
        tp = TestPlan(tg, html_reporter)
        stats = tp.run()
        print(
            f"duration= {stats.duration}",
            f"mean= {stats.sample_time_mean_milliseconds}",
            f"min= {stats.sample_time_min_milliseconds}",
            f"median= {stats.sample_time_median_milliseconds}",
            f"90p= {stats.sample_time_90_percentile_milliseconds}",
            f"95p= {stats.sample_time_95_percentile_milliseconds}",
            f"99p= {stats.sample_time_99_percentile_milliseconds}",
            f"max= {stats.sample_time_max_milliseconds}",
            sep="\t",
        )
        self.assertLess(stats.sample_time_99_percentile_milliseconds, 1000)


if __name__ == "__main__":
    main()

```

In this example, the standard python unittest was used to execute the test code, however pymeter is framework agnostic and can be used by any other testing framework

## Code styling
### `black` used for auto-formatting code [read](https://pypi.org/project/black/),
### `pylint` used for code linting and pep8 compliance [read](https://pypi.org/project/pylint/),
### `mypy` used for type hinting [read](https://pypi.org/project/mypy/),
### `robocop` static code analyzer for robotframework [read](https://pypi.org/project/robotframework-robocop/),
### `perflint` pylint extension for performance linting [read](https://betterprogramming.pub/use-perflint-a-performance-linter-for-python-eae8e54f1e99)
### `cosmic-ray` Python tool for mutation testing [read](https://python.plainenglish.io/python-mutation-testing-with-cosmic-ray-4b78eb9e0676)

## links
1. [JMeter Dsl](https://abstracta.github.io/jmeter-java-dsl/)
2. [pyjnius](https://github.com/kivy/pyjnius)