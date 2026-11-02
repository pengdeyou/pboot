Caching
=======

When your application runs slow, throw some caches in.  Well, at least
it's the easiest way to speed up things.  What does a cache do?  Say you
have a function that takes some time to complete but the results would
still be good enough if they were 5 minutes old.  So then the idea is that
you actually put the result of that calculation into a cache for some
time.

Pboot itself does not provide caching for you, but `pboot-caching`_, an
extension for Pboot does. pboot-caching supports various backends, and it is
even possible to develop your own caching backend.


.. _pboot-caching: https://gitee.com/pboot-org/pboot-caching
