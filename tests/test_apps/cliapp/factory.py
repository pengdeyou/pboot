from pboot import Pboot


def create_app():
    return Pboot("app")


def create_app2(foo, bar):
    return Pboot("_".join(["app2", foo, bar]))


def no_app():
    pass
