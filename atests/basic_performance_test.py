"""unittest module"""
from unittest import TestCase, main
from pymeter.api.reporters import HtmlReporter
from pymeter.api.timers import UniformRandomTimer
from pymeter.api.config import TestPlan, ThreadGroup
from pymeter.api.samplers import HttpSampler


class TestTestPlanClass(TestCase):
    def test_1(self):

        timer = UniformRandomTimer(100, 200)
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1", timer)
        tg = ThreadGroup(10, 1, 20, http_sampler, name="Some Name")
        html_reporter = HtmlReporter()
        tp = TestPlan(tg, html_reporter)
        stats = tp.run()
        print(
            f"duration= {stats.duration},",
            f"mean= {stats.sample_time_mean_milliseconds},",
            f"min= {stats.sample_time_min_milliseconds},",
            f"median= {stats.sample_time_median_milliseconds},",
            f"90p= {stats.sample_time_90_percentile_milliseconds},",
            f"95p= {stats.sample_time_95_percentile_milliseconds},",
            f"99p= {stats.sample_time_99_percentile_milliseconds},",
            f"max= {stats.sample_time_max_milliseconds},",

            sep="\t\t",
        )
        self.assertLess(stats.sample_time_90_percentile_milliseconds, 1000)
        self.assertLess(stats.sample_time_95_percentile_milliseconds, 1000)
        self.assertLess(stats.sample_time_99_percentile_milliseconds, 1000)


if __name__ == "__main__":
    main()
