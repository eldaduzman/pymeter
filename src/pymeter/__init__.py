"""
Welcome to pymeter's documentation.


"""
import os
import pathlib

import jnius_config

jars = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources", "jars", "*")

jnius_config.set_classpath(".", jars)
