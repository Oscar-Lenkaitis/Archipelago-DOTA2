from __future__ import annotations
import json
from importlib import resources
from typing import TYPE_CHECKING, Dict, List, Optional
from dataclasses import dataclass

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import DOTA2World


# MacGuffin item: collect X to win (Prim goal) or unlock final character (Win with Character).
# Spirits stay classified as filler in item definitions so they don't interfere with progression
# density, but we override DeadlockItem.excludable so Spirits are never placed in excluded
# locations.
FILLER_ITEM_NAME = "Madstone"

class DOTA2Item(Item):
    game = "DOTA 2"

    @property
    def excludable(self) -> bool:  # type: ignore[override]
        # Treat Primordial Fragments (MacGuffin) as non-excludable even though they are filler-classified.
        # This ensures they can't be placed on user-excluded locations while keeping them
        # out of progression-balancing logic.
        if self.name == FILLER_ITEM_NAME:
            return False
        return super().excludable
    
@dataclass(frozen=True)
class ItemDef:
    name: str
    classification: ItemClassification
    copies: int
    include_in_filler: bool

def _parse_classification(value: str) -> ItemClassification:
    v = (value or "").strip().lower()
    match v:
        case "progression":
            return ItemClassification.progression
        case "useful":
            return ItemClassification.useful
        case "trap":
            return ItemClassification.trap
        case "filler":
            return ItemClassification.filler
        case _:
            # Default to filler if unknown, but better to be strict for dev:
            raise ValueError(f"Unknown item classification '{value}'")

def load_hero_unlock_items(self:DOTA2World) -> List[ItemDef]:
    # Works in source and in zipped apworld due to importlib.resources.
    items: List[ItemDef] = []


    name = "Progressive Group Unlock"
    classification = _parse_classification("progression")
    copies = len(self.hero_groups)
    include_in_filler = False
    items.append(ItemDef(name=name, classification=classification, copies=copies, include_in_filler=include_in_filler))

    items.append(ItemDef(
        name="Primordial Fragment",
        classification=_parse_classification("progression"),
        copies=self.options.primordial_fragments_to_win.value + 5,
        include_in_filler=False
    ))

    return items

# Internal filler item used to pad itempool to location count when needed.
FILLER_ITEM_NAME = "Madstone"

def build_item_name_to_id(base_id: int, item_defs: list[ItemDef]) -> dict[str, int]:
    names = [d.name for d in item_defs]

    if FILLER_ITEM_NAME not in names:
        names.append(FILLER_ITEM_NAME)


    return {name: i for i, name in enumerate(names, base_id)}

