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
        ui.link("View Attackble NPCs", "/npcs-attackable")

    @ui.page("/npcs-attackable")
    def npc_attackable_view():
        session = SessionLocal()
        npcs = session.query(models.NPCEntityDef).options(
            selectinload(models.NPCEntityDef.loot_table)
            .selectinload(models.NPCLoot.loot)
            .selectinload(models.NPCLootEntry.item)
        ).filter(models.NPCEntityDef.combat_level.isnot(None)).all()

        rows = []
        for npc in sorted(npcs, key=lambda n: n.combat_level or 0):
            drops_html = "<em>No drops</em>"
            if npc.loot_table and npc.loot_table.loot:
                drop_rows = "".join(
                    f"<tr><td>{e.item.name if e.item else '(missing)'}</td><td>{e.amount}</td><td>{e.odds}</td></tr>"
                    for e in npc.loot_table.loot
                )
                drops_html = (
                    "<details>"
                    "<summary>View Drops</summary>"
                    "<table style='width:100%; border-collapse:collapse; margin-top:0.5em;'>"
                    "<thead><tr><th>Item</th><th>Amount</th><th>Odds</th></tr></thead>"
                    f"<tbody>{drop_rows}</tbody>"
                    "</table>"
                    "</details>"
                )

            rows.append({
                'name': npc.name,
                'level': npc.combat_level,
                'hitpoints': npc.hitpoints,
                'accuracy': npc.accuracy,
                'strength': npc.strength,
                'defense': npc.defense,
                'magic': npc.magic,
                'range': npc.range,
                'accuracyBonus': npc.accuracy_bonus,
                'strengthBonus': npc.strength_bonus,
                'defenseBonus': npc.defense_bonus,
                'magicBonus': npc.magic_bonus,
                'rangeBonus': npc.range_bonus,
                'speed': npc.speed,
                'aggroRadius': npc.aggro_radius,
                'isAlwaysAggro': npc.is_always_aggro,
                'respawnLength': npc.respawn_length,
                'lootTableId': npc.loot_table_id,
                'drops': drops_html
            })

        ui.aggrid({
            "defaultColDef": {
                "sortable": True,
                "filter": True,
                "floatingFilter": True,
                "resizable": True,
                "wrapText": True,
                "autoHeight": True
            },
            "columnDefs": [
                {"field": "name"},
                {"field": "level", "filter": "agNumberColumnFilter", "sort": "asc"},
                {"field": "hitpoints", "filter": "agNumberColumnFilter"},
                {"field": "accuracy", "filter": "agNumberColumnFilter"},
                {"field": "strength", "filter": "agNumberColumnFilter"},
                {"field": "defense", "filter": "agNumberColumnFilter"},
                {"field": "magic", "filter": "agNumberColumnFilter"},
                {"field": "range", "filter": "agNumberColumnFilter"},
                {"field": "accuracyBonus", "filter": "agNumberColumnFilter"},
                {"field": "strengthBonus", "filter": "agNumberColumnFilter"},
                {"field": "defenseBonus", "filter": "agNumberColumnFilter"},
                {"field": "magicBonus", "filter": "agNumberColumnFilter"},
                {"field": "rangeBonus", "filter": "agNumberColumnFilter"},
                {"field": "speed", "filter": "agNumberColumnFilter"},
                {"field": "aggroRadius", "filter": "agNumberColumnFilter"},
                {"field": "isAlwaysAggro", "filter": "agSetColumnFilter"},
                {"field": "respawnLength", "filter": "agNumberColumnFilter"},
                {"field": "lootTableId", "filter": "agNumberColumnFilter"},
                {
                    "field": "drops",
                    ":cellRenderer": "params => { const e = document.createElement('div'); e.innerHTML = params.value || '<em>No drops</em>'; return e; }"
                }
            ],
            "rowData": rows,
            "domLayout": "autoHeight",
        }).classes("w-full")

        session.close()



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
