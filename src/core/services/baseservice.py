from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from typing import Any, get_origin, get_args, get_type_hints
from django.db import models
from dataclasses import fields
from django.db.models import Model


class BaseService(metaclass=ABCMeta):

    def __call__(self) -> Any:
        self.validate()
        return self.execute()

    def get_validators(self) -> list[Callable]:
        return []

    def validate(self) -> None:
        validators = self.get_validators()
        for validator in validators:
            validator()

    @abstractmethod
    def execute(self) -> Any:
        raise NotImplementedError("Please implement in the service class")


class BaseUpdateService(BaseService):

    def update(self, instance, validated_data):
        model_meta = instance._meta
        m2m_fields = []
        update_fields = []

        for attr, value in validated_data.items():

            field = model_meta.get_field(attr)

            if isinstance(field, models.ManyToManyField):
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
                update_fields.append(attr)

        instance.save(update_fields=update_fields)

        for attr, value in m2m_fields:
            # if value:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class GetObjectsByIdService:
    """Automatically retrieves Django model objects by their ID

    - It is necessary to indicate in the type annotation the model from which the object should be selected
    - Use the load_objects() method to load objects

    """

    def load_objects(self) -> None:
        hints = get_type_hints(self.__class__)

        for field in fields(self):
            value = getattr(self, field.name)
            field_type = hints.get(field.name)

            if get_origin(field_type) is list:
                list_type_args = self.extract_types(field_type)  # Get the set of all possible types in the list

                # If there is at least one Django model type
                if any(issubclass(arg, Model) for arg in list_type_args):
                    model_class = next(
                        arg for arg in list_type_args if issubclass(arg, Model)
                    )  # Get this model type

                    if value:
                        loaded_objects = []

                        for item in value:
                            if isinstance(item, int):  # If ID then we try to load the object
                                try:
                                    obj = model_class.objects.get(pk=item)
                                    loaded_objects.append(obj)
                                except model_class.DoesNotExist:
                                    pass
                            elif isinstance(item, model_class): # If already an object
                                loaded_objects.append(item)
                        setattr(self, field.name, loaded_objects)

            # If the field is a single object
            elif isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
                for arg in get_args(field_type):
                    if issubclass(arg, Model):
                        try:
                            obj = arg.objects.get(pk=value)
                            setattr(self, field.name, obj)
                        except arg.DoesNotExist:
                            setattr(
                                self, field.name, None
                            )
                        break

    def extract_types(self, field_type):
        # If this is a union (e.g. User | int)
        if get_origin(field_type) is None:
            return [field_type]  # Not a Union, returns as is
        args = get_args(field_type)
        extracted = []
        for arg in args:
            # Recursively handle nested joins
            extracted.extend(self.extract_types(arg))
        return extracted
