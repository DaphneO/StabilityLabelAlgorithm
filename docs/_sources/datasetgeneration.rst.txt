Generating a data set
=====================
In order to empirically assess the accuracy and computation time of the labelling algorithms, one requires a data set.
We added various options for data set generation to our repository.

Generating an argumentation system
----------------------------------
Instead of manually designing an argumentation system and loading it (using an
:py:class:`~modules.argumentation.importers.argumentation_system_xlsx_reader.ArgumentationSystemXLSXReader`)
we also provide functionality to automatically generate an argumentation system.
The repository currently holds two types of generators: a random and a layered argumentation system generator.

Random argumentation system generator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: modules.dataset_generator.argumentation_system_generator.random.random_argumentation_system_generator.RandomArgumentationSystemGenerator
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: modules.dataset_generator.argumentation_system_generator.random.random_argumentation_system_generator_parameters.RandomArgumentationSystemGeneratorParameters
    :members:
    :undoc-members:
    :show-inheritance:

     .. automethod:: __init__

Layered argumentation system generator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: modules.dataset_generator.argumentation_system_generator.layered.layered_argumentation_system_generator.LayeredArgumentationSystemGenerator
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: modules.dataset_generator.argumentation_system_generator.layered.layered_argumentation_system_generator_parameters.LayeredArgumentationSystemGeneratorParameters
    :members:
    :undoc-members:
    :show-inheritance:

     .. automethod:: __init__

Computing properties for an ArgumentationTheory or ArgumentationSystem
----------------------------------------------------------------------
.. autofunction:: modules.dataset_generator.argumentation_theory_property_computer.argumentation_theory_property_computer.compute_argumentation_theory_properties

.. autofunction:: modules.dataset_generator.argumentation_theory_property_computer.argumentation_theory_property_computer.enumerate_future_argumentation_theories

.. autofunction:: modules.dataset_generator.argumentation_system_property_computer.argumentation_system_property_computer.compute_argumentation_system_properties

Generating a Dataset for a specific ArgumentationTheory
-------------------------------------------------------

.. autoclass:: modules.dataset_generator.dataset_generator.DatasetGenerator
    :members:
    :undoc-members:
    :show-inheritance:

DataSet classes
^^^^^^^^^^^^^^^
.. autoclass:: modules.dataset_generator.dataset.Dataset
    :members:
    :undoc-members:
    :show-inheritance:

     .. automethod:: __init__

.. autoclass:: modules.dataset_generator.dataset_item.DatasetItem
    :members:
    :undoc-members:
    :show-inheritance:

     .. automethod:: __init__

.. autoclass:: modules.dataset_generator.annotated_dataset_item.AnnotatedDatasetItem
    :members:
    :undoc-members:
    :show-inheritance:

     .. automethod:: __init__
