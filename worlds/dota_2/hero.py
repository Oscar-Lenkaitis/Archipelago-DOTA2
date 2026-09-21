from __future__ import annotations
from dataclasses import dataclass
import json
from importlib import resources
from typing import TYPE_CHECKING, Optional


@dataclass
class Hero:
    id: int
    api_name: str
    name: str
    primary_attr: str
    attack_type: str
    roles: list[str]
    legs: int

def get_all_heroes() -> list[Hero]:
    all_heroes: list[Hero] = []
    with resources.files(__package__).joinpath("data/heroes.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
    
        for hero in data['dota_heroes']:
            id = hero['id']
            api_name = hero['name']
            name = hero['localized_name']
            attr = hero['primary_attr']
            attack_type = hero['attack_type']
            roles = hero['roles']
            legs = hero['legs']
            all_heroes.append(Hero(id = id, api_name = api_name, name = name, primary_attr = attr, attack_type = attack_type, roles= roles, legs = legs ))
    
    return all_heroes

def get_starting_hero_pool(self, pool_size: int, all_heroes:list[Hero]) -> list[Hero]:
    starting_hero_pool: list[Hero] = []
    starting_hero_pool = self.multiworld.random.sample(all_heroes, pool_size)
    return starting_hero_pool



