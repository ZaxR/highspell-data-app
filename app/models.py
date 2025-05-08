from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class ItemDef(Base):
    __tablename__ = 'itemdefs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    cost = Column(Integer)
    is_name_plural = Column(Boolean)
    is_stackable = Column(Boolean)
    is_tradeable = Column(Boolean)

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d['_id'],
            name=d['name'],
            description=d.get('description', ''),
            cost=d.get('cost', 0),
            is_name_plural=d.get('isNamePlural', False),
            is_stackable=d.get('isStackable', False),
            is_tradeable=d.get('isTradeable', False),
        )

class PickpocketDef(Base):
    __tablename__ = 'pickpocketdefs'
    id = Column(Integer, primary_key=True)
    desc = Column(String)
    xp = Column(Integer)
    base_probability = Column(String)
    stun_ticks = Column(Integer)
    stun_damage = Column(Integer)
    stun_message = Column(String)
    loot = relationship("PickpocketLoot", back_populates="parent")

    @classmethod
    def from_dict(cls, d):
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

class PickpocketLoot(Base):
    __tablename__ = 'pickpocket_loot'
    id = Column(Integer, primary_key=True)
    pickpocket_id = Column(Integer, ForeignKey('pickpocketdefs.id'))
    item_id = Column(Integer, ForeignKey('itemdefs.id'))
    amount = Column(Integer)
    odds = Column(String)
    parent = relationship("PickpocketDef", back_populates="loot")
    item = relationship("ItemDef")

class NPCEntityDef(Base):
    __tablename__ = 'npcentitydefs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    pickpocket_id = Column(Integer, ForeignKey('pickpocketdefs.id'))
    loot_table_id = Column(Integer, ForeignKey('npcloot.id'))

    pickpocket = relationship("PickpocketDef")
    loot_table = relationship("NPCLoot")

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d['_id'],
            name=d['name'],
            description=d.get('description', ''),
            pickpocket_id=d.get('pickpocketId'),
            loot_table_id=(d.get('combat') or {}).get('lootTableId')
        )

class NPCLoot(Base):
    __tablename__ = 'npcloot'
    id = Column(Integer, primary_key=True)
    loot = relationship("NPCLootEntry", back_populates="parent")

    @classmethod
    def from_file(cls, session: Session, data):
        loot_data = data.get("rareLootTable") or data
        loot_container = cls(id=loot_data['_id'])
        
        session.merge(loot_container)
        for entry in loot_data['loot']:
            session.add(NPCLootEntry(
                loot_id=loot_container.id,
                item_id=entry['itemId'],
                amount=entry.get('amount', 1),
                odds=str(entry.get('odds', 1))
            ))

class NPCLootEntry(Base):
    __tablename__ = 'npcloot_entry'
    id = Column(Integer, primary_key=True)
    loot_id = Column(Integer, ForeignKey('npcloot.id'))
    item_id = Column(Integer, ForeignKey('itemdefs.id'))
    amount = Column(Integer)
    odds = Column(String)
    parent = relationship("NPCLoot", back_populates="loot")
    item = relationship("ItemDef")
