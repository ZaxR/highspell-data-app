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
        ui.label("Attackable NPCs").classes("text-xl font-bold")

        with ui.row():
            min_level = ui.number(label='Min Level', value=0, format='%.0f')
            show_aggro_only = ui.checkbox('Only Always Aggro')

        ui.separator()

        content_area = ui.column()
        session = SessionLocal()
        npcs = session.query(models.NPCEntityDef).options(
            selectinload(models.NPCEntityDef.loot_table).selectinload(models.NPCLoot.loot).selectinload(models.NPCLootEntry.item)
        ).filter(models.NPCEntityDef.combat_level.isnot(None)).all()

        rows = []
        npc_lookup = {}
        for npc in npcs:
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
                'lootTableId': npc.loot_table_id
            })
            npc_lookup[npc.name] = npc

        def render_drops(npc):
            with ui.expansion("View Drops", value=False):
                if npc.loot_table and npc.loot_table.loot:
                    with ui.table(columns=[
                        {'name': 'item', 'label': 'Item', 'field': 'item'},
                        {'name': 'amount', 'label': 'Amount', 'field': 'amount'},
                        {'name': 'odds', 'label': 'Odds', 'field': 'odds'}
                    ], rows=[{
                        'item': e.item.name if e.item else '(missing)',
                        'amount': e.amount,
                        'odds': e.odds
                    } for e in npc.loot_table.loot]):
                        pass
                else:
                    ui.label("No drops")

        def refresh_table():
            content_area.clear()
            filtered_rows = sorted([
                r for r in rows
                if r['level'] >= min_level.value and (not show_aggro_only.value or r['isAlwaysAggro'])
            ], key=lambda r: r['level'])

            with content_area:
                with ui.table(columns=[
                    {'name': 'name', 'label': 'Name', 'field': 'name'},
                    {'name': 'level', 'label': 'Level', 'field': 'level'},
                    {'name': 'hitpoints', 'label': 'HP', 'field': 'hitpoints'},
                    {'name': 'accuracy', 'label': 'Accuracy', 'field': 'accuracy'},
                    {'name': 'strength', 'label': 'Strength', 'field': 'strength'},
                    {'name': 'defense', 'label': 'Defense', 'field': 'defense'},
                    {'name': 'magic', 'label': 'Magic', 'field': 'magic'},
                    {'name': 'range', 'label': 'Range', 'field': 'range'},
                    {'name': 'accuracyBonus', 'label': 'Acc Bonus', 'field': 'accuracyBonus'},
                    {'name': 'strengthBonus', 'label': 'Str Bonus', 'field': 'strengthBonus'},
                    {'name': 'defenseBonus', 'label': 'Def Bonus', 'field': 'defenseBonus'},
                    {'name': 'magicBonus', 'label': 'Mag Bonus', 'field': 'magicBonus'},
                    {'name': 'rangeBonus', 'label': 'Rng Bonus', 'field': 'rangeBonus'},
                    {'name': 'speed', 'label': 'Speed', 'field': 'speed'},
                    {'name': 'aggroRadius', 'label': 'Aggro Radius', 'field': 'aggroRadius'},
                    {'name': 'isAlwaysAggro', 'label': 'Always Aggro', 'field': 'isAlwaysAggro'},
                    {'name': 'respawnLength', 'label': 'Respawn', 'field': 'respawnLength'},
                    {'name': 'lootTableId', 'label': 'Loot Table ID', 'field': 'lootTableId'},
                    {'name': 'drops', 'label': 'Drops', 'field': 'drops'}
                ], rows=[{**r,
                    'drops': "".join(
                        f"• {e.item.name if e.item else '(missing)'} x{e.amount} ({e.odds})"
                        for e in npc_lookup[r['name']].loot_table.loot
                    ) if npc_lookup[r['name']].loot_table and npc_lookup[r['name']].loot_table.loot else 'No drops'
                } for r in filtered_rows]):
                    pass

        min_level.on("change", refresh_table)
        show_aggro_only.on("change", refresh_table)
        refresh_table()

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
