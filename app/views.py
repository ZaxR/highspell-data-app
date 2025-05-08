# views.py — NiceGUI frontend

from nicegui import ui
from sqlalchemy.orm import selectinload
from app.database import SessionLocal
from app import models


def register_ui_pages():
    @ui.page("/")
    def index():
        ui.label("Highspell Data Viewer")
        ui.link("View Items", "/items")
        ui.link("View Pickpockets", "/pickpockets")
        ui.link("View NPC Entities", "/npcs")

    @ui.page("/items")
    def item_view():
        session = SessionLocal()
        items = session.query(models.ItemDef).all()
        session.close()

        ui.label("Item Definitions").classes("text-xl font-bold")
        with ui.table(columns=[
            {'name': 'id', 'label': 'ID', 'field': 'id'},
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'description', 'label': 'Description', 'field': 'description'},
            {'name': 'cost', 'label': 'Cost', 'field': 'cost'}
        ], rows=[item.__dict__ for item in items]):
            pass

    @ui.page("/pickpockets")
    def pickpocket_view():
        session = SessionLocal()
        defs = session.query(models.PickpocketDef).options(
            selectinload(models.PickpocketDef.loot).selectinload(models.PickpocketLoot.item)
        ).all()
        rows = []
        for pp in defs:
            for loot in pp.loot:
                rows.append({
                    'id': pp.id,
                    'desc': pp.desc,
                    'xp': pp.xp,
                    'loot_item': loot.item.name if loot.item else '(missing)',
                    'loot_amount': loot.amount,
                    'loot_odds': loot.odds,
                })
        session.close()

        ui.label("Pickpocket Definitions").classes("text-xl font-bold")
        with ui.table(columns=[
            {'name': 'id', 'label': 'ID', 'field': 'id'},
            {'name': 'desc', 'label': 'Description', 'field': 'desc'},
            {'name': 'xp', 'label': 'XP', 'field': 'xp'},
            {'name': 'loot_item', 'label': 'Loot Item', 'field': 'loot_item'},
            {'name': 'loot_amount', 'label': 'Amount', 'field': 'loot_amount'},
            {'name': 'loot_odds', 'label': 'Odds', 'field': 'loot_odds'}
        ], rows=rows):
            pass

    @ui.page("/npcs")
    def npc_view():
        session = SessionLocal()
        npcs = session.query(models.NPCEntityDef).options(
            selectinload(models.NPCEntityDef.loot_table).selectinload(models.NPCLoot.loot).selectinload(models.NPCLootEntry.item),
            selectinload(models.NPCEntityDef.pickpocket)
        ).all()
        rows = []
        for npc in npcs:
            row = {
                'id': npc.id,
                'name': npc.name,
                'description': npc.description,
                'pickpocket_desc': npc.pickpocket.desc if npc.pickpocket else None,
            }
            if npc.loot_table and npc.loot_table.loot:
                for loot in npc.loot_table.loot:
                    rows.append({**row,
                        'loot_item': loot.item.name if loot.item else '(missing)',
                        'loot_amount': loot.amount,
                        'loot_odds': loot.odds
                    })
            else:
                rows.append(row)
        session.close()

        ui.label("NPC Entity Definitions").classes("text-xl font-bold")
        with ui.table(columns=[
            {'name': 'id', 'label': 'ID', 'field': 'id'},
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'description', 'label': 'Description', 'field': 'description'},
            {'name': 'pickpocket_desc', 'label': 'Pickpocket Group', 'field': 'pickpocket_desc'},
            {'name': 'loot_item', 'label': 'Loot Item', 'field': 'loot_item'},
            {'name': 'loot_amount', 'label': 'Amount', 'field': 'loot_amount'},
            {'name': 'loot_odds', 'label': 'Odds', 'field': 'loot_odds'}
        ], rows=rows):
            pass
