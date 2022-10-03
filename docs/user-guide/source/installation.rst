Installation
============


Prerequisites
--------------

.. list-table:: 
   :widths: 2 10 40 50
   :header-rows: 1

   * - #
     - Item
     - Distribution
     - Link
   * - *
     - Python
     - CPython version 3.9 or higher
     - https://www.python.org/
   * - *
     - Java
     - OpenJdk temurin versions 8 and 11
     - https://adoptium.net/temurin/releases
   * - *
     - OS
     - Windows, Linux, MACOS
     -


JAVA_HOME environment variable
-------------------------------
Make sure that the `JAVA_HOME` environment variable is set correctly `read <https://confluence.atlassian.com/doc/setting-the-java_home-variable-in-windows-8895.html>`_



.. tabs::

   .. group-tab:: macOS/Linux

      .. code-block:: text

         $ echo $JAVA_HOME


   .. group-tab:: Windows

      .. code-block:: text

         > echo %JAVA_HOME%


.. _install-activate-env:

Install from pip
-------------------------------

      .. code-block:: text

         > pip install py-jmeter-dsl

Now you can open a python shell

      .. code-block:: text

         > python
         >>> import pymeter

You are good to go! 👍