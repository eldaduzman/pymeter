import re
from jnius import autoclass, JavaException


class BaseJMeterClass:
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    java_duration = autoclass("java.time.Duration")
    jmeter_class = autoclass("us.abstracta.jmeter.javadsl.JmeterDsl")

    @property
    def java_wrapped_element(self):
        cls_name = self.__class__.__name__
        wrapped_instance_name = BaseJMeterClass.pattern.sub("_", cls_name).lower()

        return object.__getattribute__(self, f"_{wrapped_instance_name}_instance")