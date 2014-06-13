from importlib import import_module


def get_resource_class_from_class_name(name):
    resource_module = import_module('gapipy.resources')
    return getattr(resource_module, name)


def get_resource_class_from_resource_name(name):
    mapping = {resource._resource_name: resource
               for resource in get_available_resource_classes()}
    return mapping[name]


def get_available_resource_classes():
    from .resources import available_resources
    resource_module = import_module('gapipy.resources')
    return [getattr(resource_module, r) for r in available_resources]
