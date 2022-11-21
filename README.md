# pymeter
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
Simple JMeter performance tests API for python

#### Powered by [JMeter-DSL](https://abstracta.github.io/jmeter-java-dsl/) and [pyjnius](https://github.com/kivy/pyjnius) 


[![Version](https://img.shields.io/pypi/v/pymeter.svg)](https://pypi.python.org/pypi/pymeter)
![](https://raw.githubusercontent.com/eldaduzman/pymeter/main/docs/badges/coverage-badge.svg)
![](https://raw.githubusercontent.com/eldaduzman/pymeter/main/docs/badges/pylint.svg)
![](https://raw.githubusercontent.com/eldaduzman/pymeter/main/docs/badges/mutscore.svg)
[![Generic badge](https://img.shields.io/badge/python-3.8|3.9|3.10|3.11-blue.svg)](https://python.org/)
[![Generic badge](https://img.shields.io/badge/JMeterDsl-1.3-blue.svg)](https://abstracta.github.io/jmeter-java-dsl/)
[![Documentation Status](https://readthedocs.org/projects/pymeter/badge/?version=latest)](https://pymeter.readthedocs.io/en/latest/?badge=latest)


[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


<br/>

<div style="text-align:center"><img src="https://raw.githubusercontent.com/eldaduzman/pymeter/main/docs/user-guide/source/_static/pymeter-logo-full.jpg" width="70%" /></div>

<br/>
<br/>
<br/>
<br/>



## Load testing with JMeter using python!


Read the documentation [here](https://pymeter.readthedocs.io/en/latest/) <br/>
Read about performance benchmarking [here](https://github.com/eldaduzman/pymeter-benchmark)

**JMeter** is one of the most popular and long standing load testing tools. <br/>
The original implementation is a gui based tool to script load test scenarios in a hierarchical structure, however this came with limitations and shortcomings.

For once, upgrading JMeter versions is painful, as it involved manually downloading and deploying executable files.
This became very clear when [log4j](https://en.wikipedia.org/wiki/Log4Shell) vulnerability was discovered, and software developers needed to instantly upgrade their log4j versions.
With JMeter, this was even more painful without a proper package management system such as maven or gradle.

Other limitations include difficulty to share code between different projects, using source control management tools such as git or svn.
It is quite difficult to extend JMeter and it requires a GUI editor which means to use additional development environment instead of using a single IDE for all needs.

The awesome folks at [abstracta](https://abstracta.us/) have put up an amazing amount of work to deliver [JMeter-DSL](https://abstracta.github.io/jmeter-java-dsl/), which allows developers to use plain Java to script their load test scenarios, and pretty much solve all the pain mentioned above.

`pymeter` project is aimed to capitalize on the success of JMeter-DSL and extend it to the python community!
Using [pyjnius](https://github.com/kivy/pyjnius) developed by Kivy, it is possible to bridge between JMeter-DSLs classes written in Java and reflect them into python's runtime environment without spawning up java runtime and relying on costly inter-process communication.


### Pre-requisites:
1. python version 3.9 or higher - [download](https://www.python.org/)
2. Java version 8 or 11 - [download](https://adoptium.net/temurin/releases)
3. JAVA_HOME environment variable set - [read](https://confluence.atlassian.com/doc/setting-the-java_home-variable-in-windows-8895.html)

### Install pymeter
```bash
>>> pip install pymeter
```

### simple pymeter script:

```python
"""unittest module"""
from unittest import TestCase, main

from pymeter.api.config import TestPlan, ThreadGroupWithRampUpAndHold
from pymeter.api.postprocessors import JsonExtractor
from pymeter.api.reporters import HtmlReporter
from pymeter.api.samplers import DummySampler, HttpSampler
from pymeter.api.timers import UniformRandomTimer


class TestTestPlanClass(TestCase):
    def test_1(self):
        json_extractor = JsonExtractor("variable", "args.var")
        timer = UniformRandomTimer(1000, 2000)
        http_sampler = HttpSampler(
            "Echo",
            "https://postman-echo.com/get?var=${__Random(0,10)}",
            timer,
            json_extractor,
        )
        dummy_sampler = DummySampler("dummy ${variable}", "hi dummy")
        tg = ThreadGroupWithRampUpAndHold(
            10, 1, 60, http_sampler, dummy_sampler, name="Some Name"
        )
        html_reporter = HtmlReporter()
        tp = TestPlan(tg, html_reporter)
        stats = tp.run()
        print(
            f"duration= {stats.duration_milliseconds}",
            f"mean= {stats.sample_time_mean_milliseconds}",
            f"min= {stats.sample_time_min_milliseconds}",
            f"median= {stats.sample_time_median_milliseconds}",
            f"90p= {stats.sample_time_90_percentile_milliseconds}",
            f"95p= {stats.sample_time_95_percentile_milliseconds}",
            f"99p= {stats.sample_time_99_percentile_milliseconds}",
            f"max= {stats.sample_time_max_milliseconds}",
            sep="\t",
        )
        self.assertLess(stats.sample_time_99_percentile_milliseconds, 2000)


if __name__ == "__main__":
    main()

```

In this example, the standard python unittest was used to execute the test code, however pymeter is framework agnostic and can be used by any other testing framework

## File Structure

```
|   .coverage
|   .gitignore
|   .pylintrc
|   cosmic-ray-config.ini
|   LICENSE
|   make.bat
|   Makefile
|   poetry.lock
|   pyproject.toml
|   README.md
|   tox.ini               
+---source
|   |   conf.py
|   |   index.rst
|   |   
|   +---_static
|   \---_templates
+---src
|   \---pymeter
|       |   __init__.py
|       |   
|       +---api
|       |   |   config.py
|       |   |   postprocessors.py
|       |   |   reporters.py
|       |   |   samplers.py
|       |   |   timers.py
|       |   |   __init__.py
|       |   |   
+---utests
|   |   test_postprocessors.py
|   |   test_reporter.py
|   |   test_sampler.py
|   |   test_test_plan.py
|   |   test_thread_group.py
|   |   test_timers.py
|   |   __init__.py
|   |   
```
## Code styling
### `black` used for auto-formatting code [read](https://pypi.org/project/black/),
### `pylint` used for code linting and pep8 compliance [read](https://pypi.org/project/pylint/),
### `mypy` used for type hinting [read](https://pypi.org/project/mypy/),
### `perflint` pylint extension for performance linting [read](https://betterprogramming.pub/use-perflint-a-performance-linter-for-python-eae8e54f1e99)
### `cosmic-ray` Python tool for mutation testing [read](https://python.plainenglish.io/python-mutation-testing-with-cosmic-ray-4b78eb9e0676)

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://www.linkedin.com/in/antonio-zaitoun/"><img src="https://avatars.githubusercontent.com/u/17438617?v=4?s=100" width="100px;" alt="Antonio Zaitoun"/><br /><sub><b>Antonio Zaitoun</b></sub></a><br /><a href="https://github.com/eldaduzman/pymeter/commits?author=Minitour" title="Documentation">📖</a></td>
      <td align="center"><a href="https://medium.com/@eldadu1985"><img src="https://avatars.githubusercontent.com/u/55621402?v=4?s=100" width="100px;" alt="Eldad Uzman"/><br /><sub><b>Eldad Uzman</b></sub></a><br /><a href="#infra-eldaduzman" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/eldaduzman/pymeter/commits?author=eldaduzman" title="Tests">⚠️</a> <a href="https://github.com/eldaduzman/pymeter/commits?author=eldaduzman" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## links
1. [JMeter Dsl](https://abstracta.github.io/jmeter-java-dsl/)
2. [pyjnius](https://github.com/kivy/pyjnius)
