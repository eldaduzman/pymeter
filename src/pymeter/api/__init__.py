import re
from jnius import autoclass, JavaException


class BaseJMeterClass:
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    java_duration = autoclass("java.time.Duration")
    jmeter_class = autoclass("us.abstracta.jmeter.javadsl.JmeterDsl")
    test_plan_stats = autoclass("us.abstracta.jmeter.javadsl.core.TestPlanStats")
    wrapped_instance_name = None

    @property
    def java_wrapped_element(self):
        if not self.__class__.wrapped_instance_name:
            self.__class__.wrapped_instance_name = BaseJMeterClass.pattern.sub("_", self.__class__.__name__).lower()

        return object.__getattribute__(self, f"_{self.__class__.wrapped_instance_name}_instance")
