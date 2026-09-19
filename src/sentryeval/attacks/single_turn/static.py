from ..base import BaseAttack


class StaticAttack(BaseAttack):
    name = "static"
    template = "{request}"
