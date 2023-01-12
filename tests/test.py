from pyvcr_cleaner import CleanYAMLSerializer
import pytest

def ():
    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(imported_fun1)
    serializer.register_cleaner(builtin_fun2)
    my_vcr.register_serializer("cleanyaml", serializer)
