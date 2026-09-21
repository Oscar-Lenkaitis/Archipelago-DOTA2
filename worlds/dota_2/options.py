from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from Options import Choice, Range, PerGameCommonOptions

def _load_hero_names() -> list[str]:
    """Hero names in order (matches heroes.csv; used for FinalCharacter option value -> name)."""
    names: list[str] = []
    try:
        with resources.files(__package__).joinpath("data/heroes.json").open("r", encoding="utf-8") as f:
            data = json.load(f)
            for hero in data["dota_heroes"]:
                names.append(hero["localized_name"])
    except Exception:
        pass
    return names if names else ["Dragon Knight"]

class GoalType(Choice):
    """How game completion is determined.

    - **Unique Characters:** Win with N different characters.
    - **Total Wins:** Win N matches total.
    - **Spirits:** Collect N Spirits (MacGuffin) to win.
    - **Win with Character:** Collect X Spirits to unlock your chosen final character, then win one match with that character.
    """
    display_name = "Goal Type"
    option_unique_characters = 0
    option_total_wins = 1
    option_primordial_fragments = 2
    option_win_with_character = 3
    default = 0

class UniqueCharactersToWin(Range):
    """Number of unique characters you must win with to finish (1-20)."""
    display_name = "Unique Characters to Win"
    range_start = 1
    range_end = 20
    default = 5


class TotalWinsToWin(Range):
    """Number of total match wins you must achieve to finish."""
    display_name = "Total Wins to Win"
    range_start = 1
    range_end = 20
    default = 5


class PrimordialFragmentsToWin(Range):
    """Number of Primordial Fragments (MacGuffin) you must collect to finish. Max depends on game mode (Standard: 162, Street Brawl: 143)."""
    display_name = "Primordial Fragments to Win"
    range_start = 1
    range_end = 10  # Standard max; Street Brawl is clamped to 143 in world
    default = 5

class PrimordialFragmentsToUnlockFinal(Range):
    """Number of Primordial Fragments (MacGuffin) you must collect to unlock your final character (Win with Character goal).

    The world caps this below the usual Primordial Fragments max by three: the final hero's three win checks require
    this many Primordial Fragments first and may themselves contain Primordial Fragments, so the threshold must be reachable using
    other locations only.
    """
    display_name = "Spirits to Unlock Final Character"
    range_start = 1
    range_end = 10
    default = 5

_FINAL_CHARACTER_NAMES: list[str] = _load_hero_names()

def _hero_name_to_option_key(name: str) -> str:
    return name.lower().replace(" ", "_").replace("&", "and")

# Build FinalCharacter with all option_* in the class namespace at creation time so the
# Choice metaclass (AssembleOptions) sees them and populates .options / .name_lookup.
_final_char_attrs: dict = {
    "__module__": __name__,
    "display_name": "Final Character (Win With)",
    "default": 0,
}
for _i, _name in enumerate(_FINAL_CHARACTER_NAMES):
    _final_char_attrs[f"option_{_hero_name_to_option_key(_name)}"] = _i

FinalCharacter = type("FinalCharacter", (Choice,), _final_char_attrs)


@dataclass
class DOTA2Options(PerGameCommonOptions):
    goal_type: GoalType
    unique_characters_to_win: UniqueCharactersToWin
    total_wins_to_win: TotalWinsToWin
    primordial_fragments_to_win: PrimordialFragmentsToWin
    primordial_fragments_to_unlock_final: PrimordialFragmentsToUnlockFinal
    final_character: FinalCharacter
    # game_mode: GameMode
    # exclude_hard_locations: ExcludeHardLocations




# class HardMode(Toggle):
#     """
#     In hard mode, the basic enemy and the final boss will have more health.
#     The Health Upgrades become progression, as they are now required to beat the final boss.
#     """

#     # The docstring of an option is used as the description on the website and in the template yaml.

#     # You'll also want to set a display name, which will determine what the option is called on the website.
#     display_name = "Hard Mode"


# class Hammer(Toggle):
#     """
#     Adds another item to the itempool: The Hammer.
#     The top middle chest will now be locked behind a breakable wall, requiring the Hammer.
#     """

#     display_name = "Hammer"
# class ExtraStartingChest(Toggle):
#     """
#     Adds an extra chest in the bottom left, making room for an extra Confetti Cannon.
#     """

#     display_name = "Extra Starting Chest"


# class TrapChance(Range):
#     """
#     Percentage chance that any given Confetti Cannon will be replaced by a Math Trap.
#     """

#     display_name = "Trap Chance"

#     range_start = 0
#     range_end = 100
#     default = 0


# class StartWithOneConfettiCannon(Toggle):
#     """
#     Start with a confetti cannon already in your inventory.
#     Why? Because you deserve it. You get to celebrate yourself without doing any work first.
#     """

#     display_name = "Start With One Confetti Cannon"


# # A Range is a numeric option with a min and max value. This will be represented by a slider on the website.
# class ConfettiExplosiveness(Range):
#     """
#     How much confetti each use of a confetti cannon will fire.
#     """

#     display_name = "Confetti Explosiveness"

#     range_start = 0
#     range_end = 10

#     # Range options must define an explicit default value.
#     default = 3

# # A Choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
# class PlayerSprite(Choice):
#     """
#     The sprite that the player will have.
#     """

#     display_name = "Player Sprite"

#     option_human = 0
#     option_duck = 1
#     option_horse = 2
#     option_cat = 3

#     # Choice options must define an explicit default value.
#     default = option_human

#     # For choices, you can also define aliases.
#     # For example, we could make it so "player_sprite: kitty" resolves to "player_sprite: cat" like this:
#     alias_kitty = option_cat


# # We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# # This is in the format "option_name_in_snake_case: OptionClassName".

# @dataclass
# class DOTA2Options(PerGameCommonOptions):
#     hard_mode: HardMode
#     hammer: Hammer
#     extra_starting_chest: ExtraStartingChest
#     start_with_one_confetti_cannon: StartWithOneConfettiCannon
#     trap_chance: TrapChance
#     confetti_explosiveness: ConfettiExplosiveness
#     player_sprite: PlayerSprite


# # If we want to group our options by similar type, we can do so as well. This looks nice on the website.
# option_groups = [
#     OptionGroup(
#         "Gameplay Options",
#         [HardMode, Hammer, ExtraStartingChest, StartWithOneConfettiCannon, TrapChance],
#     ),
#     OptionGroup(
#         "Aesthetic Options",
#         [ConfettiExplosiveness, PlayerSprite],
#     ),
# ]

# # Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
# option_presets = {
#     "boring": {
#         "hard_mode": False,
#         "hammer": False,
#         "extra_starting_chest": False,
#         "start_with_one_confetti_cannon": False,
#         "trap_chance": 0,
#         "confetti_explosiveness": ConfettiExplosiveness.range_start,
#         "player_sprite": PlayerSprite.option_human,
#     },
#     "the true way to play": {
#         "hard_mode": True,
#         "hammer": True,
#         "extra_starting_chest": True,
#         "start_with_one_confetti_cannon": True,
#         "trap_chance": 50,
#         "confetti_explosiveness": ConfettiExplosiveness.range_end,
#         "player_sprite": PlayerSprite.option_duck,
#     },
# }