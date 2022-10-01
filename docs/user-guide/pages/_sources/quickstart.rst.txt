Quickstart
============

simple example
--------------
      .. code-block:: python

            from pymeter.api.config import TestPlan, ThreadGroupSimple
            from pymeter.api.samplers import HttpSampler


            # create HTTP sampler, sends a get request to the given url
            http_sampler = HttpSampler("echo_get_request", "https://postman-echo.com/get?var=1")

            # create a thread group with 10 threads that runs for 1 iterations, give it the http sampler as a child input
            thread_group = ThreadGroupSimple(10, 1, http_sampler)

            # create a test plan with the required thread group
            test_plan = TestPlan(thread_group)

            # run the test plan and take the results
            stats = test_plan.run()


            # Assert that the 99th percentile of response time is less than 2000 milliseconds.
            assert (
                stats.sample_time_99_percentile_milliseconds <= 2000
            ), f"99th precentile should be less than 2000 milliseconds, got {stats.sample_time_99_percentile_milliseconds}"

For more options, please read the  `api documentation <api.html>`_.