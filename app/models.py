from typing import Optional, List, Any
from sqlmodel import SQLModel, Field, Relationship, Session

# Shared Models using SQLModel (combines Pydantic + SQLAlchemy)

class ItemDef(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""
    cost: int = 0
    is_name_plural: bool = False
    is_stackable: bool = False
    is_tradeable: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> "ItemDef":
        return cls(
            id=d['_id'],
            name=d['name'],
            description=d.get('description', ''),
            cost=d.get('cost', 0),
            is_name_plural=d.get('isNamePlural', False),
            is_stackable=d.get('isStackable', False),
            is_tradeable=d.get('isTradeable', False)
        )

class PickpocketLoot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pickpocket_id: Optional[int] = Field(default=None, foreign_key="pickpocketdef.id")
    item_id: Optional[int] = Field(default=None, foreign_key="itemdef.id")
    amount: int = 1
    odds: str = "1"

    parent: Optional["PickpocketDef"] = Relationship(back_populates="loot")

class PickpocketDef(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    desc: str
    xp: int = 0
    base_probability: str = "0"
    stun_ticks: int = 0
    stun_damage: int = 0
    stun_message: str = ""
    loot: List[PickpocketLoot] = Relationship(back_populates="parent")

    @classmethod
    def from_dict(cls, d: dict) -> "PickpocketDef":
        return cls(
            id=d['_id'],
            desc=d['desc'],
            xp=d.get('xp', 0),
            base_probability=str(d.get('baseProbabilityOfSuccess', 0)),
            stun_ticks=d.get('stunTicks', 0),
            stun_damage=d.get('stunDamage', 0),
            stun_message=d.get('stunMessage', '')
        )

    @classmethod
    def from_file(cls, session: Session, data):
        for record in data['pickpocketing']:
            obj = cls.from_dict(record)
            session.merge(obj)
            for drop in record.get('loot', []) + record.get('baseLoot', []):
                session.add(PickpocketLoot(
                    pickpocket_id=obj.id,
                    item_id=drop['itemId'],
                    amount=drop.get('amount', 1),
                    odds=str(drop.get('odds', 1))
                ))

class NPCLootEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    loot_id: Optional[int] = Field(default=None, foreign_key="npcloot.id")
    item_id: Optional[int] = Field(default=None, foreign_key="itemdef.id")
    amount: int = 1
    odds: str = "1"

    parent: Optional["NPCLoot"] = Relationship(back_populates="loot")
    item: Optional["ItemDef"] = Relationship()

class NPCLoot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    loot: List[NPCLootEntry] = Relationship(back_populates="parent")
    npcs: List["NPCEntityDef"] = Relationship(back_populates="loot_table")

    @classmethod
    def from_file(cls, session: Session, data):
        loot_data = data.get("rareLootTable") or data
        loot_container = session.merge(cls(id=loot_data['_id']))
        session.flush()
        for entry in loot_data['loot']:
            session.add(NPCLootEntry(
                loot_id=loot_container.id,
                item_id=entry['itemId'],
                amount=entry.get('amount', 1),
                odds=str(entry.get('odds', 1))
            ))

class NPCEntityDef(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""
    pickpocket_id: Optional[int] = Field(default=None, foreign_key="pickpocketdef.id")
    loot_table_id: Optional[int] = Field(default=None, foreign_key="npcloot.id")

    # Optional combat stats
    combat_level: Optional[int] = None
    hitpoints: Optional[int] = None
    accuracy: Optional[int] = None
    strength: Optional[int] = None
    defense: Optional[int] = None
    magic: Optional[int] = None
    range: Optional[int] = None
    accuracy_bonus: Optional[int] = None
    strength_bonus: Optional[int] = None
    defense_bonus: Optional[int] = None
    magic_bonus: Optional[int] = None
    range_bonus: Optional[int] = None
    speed: Optional[int] = None
    aggro_radius: Optional[int] = None
    is_always_aggro: bool = False
    respawn_length: Optional[int] = None

    loot_table: Optional["NPCLoot"] = Relationship(back_populates="npcs")

    @classmethod
    def from_dict(cls, d: dict) -> "NPCEntityDef":
        combat = d.get('combat') or {}
        return cls(
            id=d['_id'],
            name=d['name'],
            description=d.get('description', ''),
            pickpocket_id=d.get('pickpocketId'),
            loot_table_id=combat.get('lootTableId'),
            combat_level=combat.get('level'),
            hitpoints=combat.get('hitpoints'),
            accuracy=combat.get('accuracy'),
            strength=combat.get('strength'),
            defense=combat.get('defense'),
            magic=combat.get('magic'),
            range=combat.get('range'),
            accuracy_bonus=combat.get('accuracyBonus'),
            strength_bonus=combat.get('strengthBonus'),
            defense_bonus=combat.get('defenseBonus'),
            magic_bonus=combat.get('magicBonus'),
            range_bonus=combat.get('rangeBonus'),
            speed=combat.get('speed'),
            aggro_radius=combat.get('aggroRadius'),
            is_always_aggro=bool(combat.get('isAlwaysAggro')),
            respawn_length=combat.get('respawnLength')
        )
