#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from enum import IntEnum


class ItemType(IntEnum):
    CLOTHING_HEAD = 100
    CLOTHING_FACE = 101
    CLOTHING_JACKET = 102
    CLOTHING_PANTS = 103
    CLOTHING_GLOVES = 104
    CLOTHING_SHOES = 105
    CLOTHING_ACC = 106
    CLOTHING_PET = 107
    WEAPON_MELEE = 200
    WEAPON_GUN = 201
    WEAPON_HEAVY = 202
    WEAPON_SNIPE = 203
    WEAPON_DEPLOY = 204
    WEAPON_THROWING = 205
    WEAPON_SPECIAL = 206
    SKILL = 3


class ItemGender(IntEnum):
    UNISEX = 0
    MAN = 1
    WOMAN = 2


class Item:
    def __init__(self, id):
        self.id = id
        self.gender = ItemGender.UNISEX

    def get_id(self):
        return self.id

    def set_gender(self, gender):
        self.gender = gender

    def get_gender(self):
        return self.gender

    def get_type(self):
        for itemType in ItemType:
            if self.id.startswith(str(itemType.value)):
                return itemType

        raise ValueError("Unknown item type")


def calculate_tab_info(item):
    type = item.get_type()

    if type == ItemType.CLOTHING_HEAD:
        return (3, 2)
    elif type == ItemType.CLOTHING_FACE:
        return (3, 3)
    elif type == ItemType.CLOTHING_JACKET:
        return (3, 4)
    elif type == ItemType.CLOTHING_PANTS:
        return (3, 5)
    elif type == ItemType.CLOTHING_GLOVES:
        return (3, 6)
    elif type == ItemType.CLOTHING_SHOES:
        return (3, 7)
    elif type == ItemType.CLOTHING_ACC:
        return (3, 8)
    elif type == ItemType.CLOTHING_PET:
        return (3, 9)
    elif type == ItemType.WEAPON_MELEE:
        return (2, 1)
    elif type == ItemType.WEAPON_GUN:
        return (2, 3)
    elif type == ItemType.WEAPON_HEAVY:
        return (2, 4)
    elif type == ItemType.WEAPON_SNIPE:
        return (2, 5)
    elif type in [ItemType.WEAPON_DEPLOY, ItemType.WEAPON_SPECIAL]:
        return (2, 6)
    elif type == ItemType.WEAPON_THROWING:
        return (2, 7)
    elif type == ItemType.SKILL:
        return (2, 8)
        

def parse_items(tree):
    items = []

    root = tree.getroot()
    for x7item in root:
        if "item_key" in x7item.attrib:
            id = x7item.attrib["item_key"]
        elif "name" in x7item.attrib:
            id = x7item.attrib["name"]
        else:
            continue

        item = Item(id=id)

        for part in x7item:
            if part.tag == "base":
                if "sex" in part.attrib:
                    item.set_gender(ItemGender[part.attrib["sex"].upper()])
    
        try:
            item.get_type()
        except ValueError:
            continue
    
        items.append(item)

    return items


items = []

items.extend(parse_items(ET.parse("action.x7")))
items.extend(parse_items(ET.parse("_eu_weapon.x7")))
items.extend(parse_items(ET.parse("item.x7")))

# Create required groups for foreign keys
print(f"INSERT IGNORE INTO shop_effect_groups (Id, Name, PreviewEffect) VALUES (1, 'None', 0);")
print(f"INSERT IGNORE INTO shop_price_groups (Id, Name, PriceType) VALUES (1, 'Free', 1);")

for item in items:
    tab_info = calculate_tab_info(item)

    print(f"INSERT IGNORE INTO shop_items (Id, RequiredGender, RequiredLicense, Colors, UniqueColors, RequiredLevel, LevelLimit, RequiredMasterLevel, IsOneTimeUse, IsDestroyable, MainTab, SubTab) VALUES ({item.get_id()}, {item.get_gender().value}, 0, 0, 0, 0, 0, 0, 0, 1, {tab_info[0]}, {tab_info[1]});")
    print(f"INSERT IGNORE INTO shop_iteminfos (ShopItemId, PriceGroupId, EffectGroupId, DiscountPercentage, IsEnabled) VALUES ({item.get_id()}, 1, 1, 0, 1);")
