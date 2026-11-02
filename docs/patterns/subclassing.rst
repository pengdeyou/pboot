Subclassing Pboot
=================

The :class:`~pboot.Pboot` class is designed for subclassing.

For example, you may want to override how request parameters are handled to preserve their order::

    from pboot import Pboot, Request
    from werkzeug.datastructures import ImmutableOrderedMultiDict
    class MyRequest(Request):
        """Request subclass to override request parameter storage"""
        parameter_storage_class = ImmutableOrderedMultiDict
    class MyPboot(Pboot):
        """Pboot subclass using the custom request class"""
        request_class = MyRequest

This is the recommended approach for overriding or augmenting Pboot's internal functionality.
