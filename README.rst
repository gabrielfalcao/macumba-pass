MacumbaPass
===========

An experimental lambda-based password manager API made with `chalice <chalice.readthedocs.io>`_, `localstack <https://localstack.cloud>`_ and `SAM Local <https://github.com/awslabs/aws-sam-local>`_.

Goals:

- Ability to develop the whole AWS application entirely in the local environment, no need for real AWS until is time to deploy.
- Leverage a development workflow similar to test-driven `Flask <>`_ applications


Development Workflow
--------------------

.. image:: docs/diagrams/diagram-development-workflow.png
   :scale: 50 %
   :alt: Development Workflow
   :align: center
   :target: docs/diagrams/diagram-development-workflow.png

Test-Driven Development
-----------------------

.. image:: docs/diagrams/diagram-unit-refactor-cleanup.png
   :scale: 50 %
   :alt: Test-Driven Development Flow
   :align: center
   :target: docs/diagrams/diagram-unit-refactor-cleanup.png


Local Debugging
---------------

.. image:: docs/diagrams/diagram-local-debugging.png
   :scale: 50 %
   :alt: Local Debugging
   :align: center
   :target: docs/diagrams/diagram-local-debugging.png
