from __future__ import annotations

from typing import TYPE_CHECKING
import re
from typing import Optional

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule, add_item_rule

from .items import FILLER_ITEM_NAME
from .options import GoalType, _FINAL_CHARACTER_NAMES

if TYPE_CHECKING:
    from .world import DOTA2World

_HERO_WIN_RE = re.compile(r"^Win as a (.+?)$")

def set_dota_rules(world:DOTA2World)-> None:
    multiworld = world.multiworld
    player = world.player

    starting_pool = world.starting_hero_pool
    hero_groups = world.hero_groups

    primordial_gate = world.options.primordial_fragments_to_win.value

    multiworld.completion_condition[player] = lambda state: (
        state.count("Primordial Fragment", player) >= primordial_gate
    )

