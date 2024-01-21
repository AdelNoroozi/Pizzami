from pizzami.common.managers import BaseManager


class FoodManager(BaseManager):
    def public(self, **kwargs):
        return self.active(is_public=True, **kwargs)

    def confirmed(self, **kwargs):
        return self.active(is_public=True, **kwargs)
