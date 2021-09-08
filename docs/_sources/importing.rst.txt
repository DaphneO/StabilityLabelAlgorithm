Reading an argumentation system
===============================

You can read an argumentation system from an .xslx file using the following module:

.. automodule:: modules.argumentation.importers.argumentation_system_xlsx_reader
    :members:
    :undoc-members:
    :show-inheritance:

Example usage:

.. code-block:: python

    asr = ArgumentationSystemXLSXReader(path_to_resources('03_2019_FQAS_Paper_Example'))
    arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)