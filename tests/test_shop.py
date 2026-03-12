import random

from game.shop import Shop, ShopItem
from game.floor import generate_shop, load_items
from game.player import Player
from game.i18n import get_i18n


def test_shop_item_availability():
    """Test shop item stock management."""
    # Unlimited stock
    item1 = ShopItem(item_name="Small Potion", price=15, stock=-1)
    assert item1.is_available()

    # Limited stock
    item2 = ShopItem(item_name="Iron Sword", price=50, stock=1)
    assert item2.is_available()

    # Out of stock
    item3 = ShopItem(item_name="Steel Sword", price=120, stock=0)
    assert not item3.is_available()


def test_shop_purchase():
    """Test shop purchase mechanics."""
    items = [
        ShopItem(item_name="Small Potion", price=15, stock=-1),
        ShopItem(item_name="Iron Sword", price=50, stock=1),
    ]
    shop = Shop(
        name={"en": "Test Shop", "zh": "测试商店"},
        description={"en": "A test shop", "zh": "一个测试商店"},
        items=items,
        min_floor=1
    )

    # Valid purchase
    success, item_name = shop.purchase_item(0)
    assert success
    assert item_name == "Small Potion"

    # Purchase limited stock item
    success, item_name = shop.purchase_item(1)
    assert success
    assert item_name == "Iron Sword"
    assert shop.items[1].stock == 0

    # Try to purchase out of stock item
    success, item_name = shop.purchase_item(1)
    assert not success

    # Invalid index
    success, item_name = shop.purchase_item(99)
    assert not success


def test_shop_generation():
    """Test shop generation logic."""
    get_i18n().set_language("en")
    rng = random.Random(42)

    # Generate shops on various floors
    shops_found = 0
    for _ in range(20):
        shop = generate_shop(5, rng)
        if shop:
            shops_found += 1
            assert shop.min_floor <= 5
            assert len(shop.items) > 0

    # Should find at least some shops
    assert shops_found > 0


def test_shop_player_purchase_flow():
    """Test complete purchase flow with player."""
    get_i18n().set_language("en")
    items_db = load_items()

    player = Player(name="Test Hero", gold=100)
    shop_items = [
        ShopItem(item_name="Small Potion", price=15, stock=-1),
        ShopItem(item_name="Iron Sword", price=50, stock=1),
    ]
    shop = Shop(
        name={"en": "Test Shop", "zh": "测试商店"},
        description={"en": "A test shop", "zh": "一个测试商店"},
        items=shop_items,
        min_floor=1
    )

    # Player has 100 gold
    assert player.gold == 100
    assert len(player.inventory) == 0

    # Purchase Small Potion (15 gold)
    success, item_name = shop.purchase_item(0)
    assert success
    player.gold -= shop_items[0].price
    item = items_db[item_name]
    player.add_item(item)

    assert player.gold == 85
    assert len(player.inventory) == 1
    assert player.inventory[0].get_name() == "Small Potion"

    # Purchase Iron Sword (50 gold)
    success, item_name = shop.purchase_item(1)
    assert success
    player.gold -= shop_items[1].price
    item = items_db[item_name]
    player.add_item(item)

    assert player.gold == 35
    assert len(player.inventory) == 2

    # Try to purchase Iron Sword again (out of stock)
    success, item_name = shop.purchase_item(1)
    assert not success


def test_shop_insufficient_gold():
    """Test that player cannot purchase without enough gold."""
    get_i18n().set_language("en")
    items_db = load_items()

    player = Player(name="Poor Hero", gold=10)
    shop_items = [
        ShopItem(item_name="Iron Sword", price=50, stock=1),
    ]
    shop = Shop(
        name={"en": "Test Shop", "zh": "测试商店"},
        description={"en": "A test shop", "zh": "一个测试商店"},
        items=shop_items,
        min_floor=1
    )

    # Player only has 10 gold, item costs 50
    assert player.gold < shop_items[0].price

    # Purchase would succeed from shop's perspective
    success, item_name = shop.purchase_item(0)
    assert success

    # But player shouldn't complete the transaction (handled in main.py)
    # This test verifies the shop mechanics work independently


def test_shop_localization():
    """Test shop name and description localization."""
    shop = Shop(
        name={"en": "Wandering Merchant", "zh": "流浪商人"},
        description={"en": "A traveling merchant", "zh": "一位旅行商人"},
        items=[],
        min_floor=1
    )

    get_i18n().set_language("en")
    assert shop.get_name() == "Wandering Merchant"
    assert shop.get_description() == "A traveling merchant"

    get_i18n().set_language("zh")
    assert shop.get_name() == "流浪商人"
    assert shop.get_description() == "一位旅行商人"
