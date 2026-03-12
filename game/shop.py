from dataclasses import dataclass

from game.i18n import t


@dataclass
class ShopItem:
    """An item available for purchase in a shop."""
    item_name: str  # Reference to item in items.json
    price: int
    stock: int = -1  # -1 means unlimited stock

    def is_available(self) -> bool:
        """Check if item is still in stock."""
        return self.stock != 0


@dataclass
class Shop:
    """A shop that appears on certain floors."""
    name: dict  # {"en": "...", "zh": "..."}
    description: dict  # {"en": "...", "zh": "..."}
    items: list[ShopItem]
    min_floor: int

    def get_name(self) -> str:
        return t(self.name)

    def get_description(self) -> str:
        return t(self.description)

    def purchase_item(self, index: int) -> tuple[bool, str]:
        """Attempt to purchase an item.

        Returns:
            (success, item_name) - success indicates if purchase was valid
        """
        if index < 0 or index >= len(self.items):
            return False, ""

        shop_item = self.items[index]
        if not shop_item.is_available():
            return False, ""

        if shop_item.stock > 0:
            shop_item.stock -= 1

        return True, shop_item.item_name
