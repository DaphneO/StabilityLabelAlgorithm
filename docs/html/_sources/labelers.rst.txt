Labelers
=========

What is a labeler?
-------------------
A labeler inherits from :py:class:`~modules.argumentation.labelers.labeler_interface.LabelerInterface`,
assigning a :py:class:`~modules.argumentation.labelers.labeler_interface.Labels` object to the
:py:class:`~modules.argumentation.argumentation_theory.argumentation_theory.ArgumentationTheory`.
Such a :py:class:`~modules.argumentation.labelers.labeler_interface.Labels object assigns a
:py:class:`~modules.argumentation.labelers.labeler_interface.StabilityLabel` object to
each :py:class:`~modules.argumentation.argumentation_theory.literal.Literal` and
:py:class:`~modules.argumentation.argumentation_theory.rule.Rule` in the
:py:class:`~modules.argumentation.argumentation_theory.argumentation_theory.ArgumentationTheory`.

.. automodule:: modules.argumentation.labelers.labels
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: modules.argumentation.labelers.stability_label
    :members:
    :undoc-members:
    :show-inheritance:

Types of labelers
-----------------
.. automodule:: modules.argumentation.labelers.labeler_interface
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: modules.argumentation.labelers.four_bool_labeler
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: modules.argumentation.labelers.satisfiability_labeler
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: modules.argumentation.labelers.acceptability_labeler
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: modules.argumentation.labelers.satisfiable_labeler
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: modules.argumentation.labelers.fqas_labeler
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: modules.argumentation.labelers.naive_stability_labeler
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: modules.argumentation.labelers.timed_four_bool_labeler
    :members:
    :undoc-members:
    :show-inheritance:

Example usage
-------------

.. code-block:: python

    from stability_label_algorithm.modules.argumentation.importers.argumentation_system_xlsx_reader import \
    ArgumentationSystemXLSXReader
    from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system import \
        ArgumentationSystem
    from stability_label_algorithm.modules.argumentation.argumentation_engine import ArgumentationEngine
    from stability_label_algorithm.modules.argumentation.labelers.fqas_labeler import FQASLabeler
    from stability_label_algorithm.modules.argumentation.labelers.four_bool_labeler import FourBoolLabeler
    from stability_label_algorithm.modules.argumentation.labelers.satisfiability_labeler import SatisfiabilityLabeler
    from stability_label_algorithm.modules.argumentation.labelers.acceptability_labeler import AcceptabilityLabeler

    asr = ArgumentationSystemXLSXReader(path_to_resources('03_2019_FQAS_Paper_Example'))
    arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
    arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
    arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())
    arg_engine_acceptability = ArgumentationEngine(arg_system, AcceptabilityLabeler())
    arg_engine_satisfiablility = ArgumentationEngine(arg_system, SatisfiabilityLabeler())

First consider a few usages of :py:class:`modules.argumentation.labelers.fqas_labeler.FQASLabeler`:

>>> arg_engine_fqas_output = arg_engine_fqas.update(['wrong_product'])
>>> arg_engine_fqas_output.labels.literal_labeling[arg_system.language['fraud']].is_stable
False
>>> arg_engine_fqas_output.labels.literal_labeling[arg_system.language['fraud']].is_contested_stable
False
>>> arg_engine_fqas_output = arg_engine_fqas.update(['wrong_product', 'counter_party_delivered'])
>>> arg_engine_fqas_output.labels.literal_labeling[arg_system.language['fraud']].is_stable
True
>>> arg_engine_fqas_output = arg_engine_fqas.update(['counter_party_delivered'])
>>> arg_engine_fqas_output.labels.literal_labeling[arg_system.language['fraud']].is_contested_stable
True
>>> arg_engine_four_bool_output = arg_engine_four_bool.update(['wrong_product'])
>>> arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['fraud']].is_stable
False
>>> arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['fraud']].is_contested_stable)
True

In the same way, other labelers, such as :py:class:`modules.argumentation.labelers.fqas_labeler.FourBoolLabeler`, can be used:

>>> arg_engine_four_bool_output = arg_engine_four_bool.update(['wrong_product', 'counter_party_delivered'])
>>> arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['fraud']].is_stable
True
>>> arg_engine_four_bool_output = arg_engine_four_bool.update(['counter_party_delivered'])
>>> arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['fraud']].is_contested_stable
True

