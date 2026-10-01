from future.utils import with_metaclass

from .base import BaseModel

from gapipy.utils import get_resource_class_from_resource_name


class HrefBasedServiceMeta(type):
    def __call__(cls, *args, **kwargs):
        # Attempt to extract the resource from the href. If it's not found for
        # whatever reason, we can't assume what the user was attempting, and
        # we'll simply ignore any metaclass magic.
        href = args[0].get('href', None) if args else None
        if href is None:
            return type.__call__(cls, *args, **kwargs)

        resource_name = cls.extract_service_resource_name(href)
        if resource_name is None:
            return type.__call__(cls, *args, **kwargs)

        new_class = get_resource_class_from_resource_name(resource_name)
        if 'stub' not in kwargs:
            kwargs['stub'] = True
        return type.__call__(new_class, *args, **kwargs)

    @classmethod
    def extract_service_resource_name(cls, href):
        """
        Extract the resource name from the href. This is used to determine
        which class to instantiate for a given service.
        """
        if not href:
            return None

        # The resource name is the second-to-last element in the path.
        parts = href.strip('/').split('/')
        if len(parts) < 2:
            return None

        return parts[-2]


class AssociatedService(with_metaclass(HrefBasedServiceMeta, BaseModel)):
    """
    Represent an associated service. Each service can be associated
    to other services within the same booking.
    """
    _as_is_fields = ['id', 'href']
