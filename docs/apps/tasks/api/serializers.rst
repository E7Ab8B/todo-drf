.. currentmodule:: apps.tasks.api.serializers

.. _tasks_api_serializers:

``apps.tasks.api.serializers`` -- `tasks` serializers
=============================================

TaskNestedSerializer
---------------------

.. autoclass:: TaskNestedSerializer(instance=None, data=empty, **kwargs)
    :show-inheritance:
    :members:
    :undoc-members:
    :class-doc-from: class

    **Fields**:

    - title
    - completed
    - uuid
    - parent_uuid
    - subtasks
    - created

TaskListSerializer
---------------------

.. autoclass:: TaskListSerializer(instance=None, data=empty, **kwargs)
    :show-inheritance:
    :members:
    :undoc-members:
    :class-doc-from: class

    **Fields**:

    - title
    - completed
    - uuid
    - parent_uuid
    - subtasks
    - created

TaskCreateSerializer
---------------------

.. autoclass:: TaskCreateSerializer(instance=None, data=empty, **kwargs)
    :show-inheritance:
    :members: validate_parent_uuid
    :undoc-members:
    :class-doc-from: class

    **Fields**:

    - title
    - uuid
    - parent_uuid

TaskUpdateSerializer
---------------------

.. autoclass:: TaskUpdateSerializer(instance=None, data=empty, **kwargs)
    :show-inheritance:
    :members:
    :undoc-members:
    :class-doc-from: class

    **Fields**:

    - title
    - completed
    - parent_uuid


UsersTaskField
----------------

.. autoclass:: UsersTaskField(source='parent', slug_field='uuid', **kwargs)
    :class-doc-from: class
