from __future__ import annotations

from typing import Generic, TypeVar

from factory.base import FactoryMetaClass

T = TypeVar("T")


class BaseMetaFactory(Generic[T], FactoryMetaClass):
    """Factory metaclass with type hinting support for generated objects."""

    def __call__(cls, *args, **kwargs) -> T:  # type: ignore [reportSelfClsParameterName]
        return super().__call__(*args, **kwargs)
