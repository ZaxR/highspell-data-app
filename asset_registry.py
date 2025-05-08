# app/asset_registry.py

from app import models

ASSETS = {
    # .carbon files with model bindings
    "itemdefs": {
        "version": 25,
        "subpath": "",
        "model": models.ItemDef,
    },
    "worldentitydefs": {
        "version": 10,
        "subpath": "",
        "model": None,
    },
    "worldentities": {
        "version": 20,
        "subpath": "",
        "model": None,
    },
    "npcentitydefs": {
        "version": 18,
        "subpath": "",
        "model": models.NPCEntityDef,
    },
    "npcentities": {
        "version": 17,
        "subpath": "",
        "model": None,
    },
    "instancednpcentities": {
        "version": 5,
        "subpath": "",
        "model": None,
    },
    "shopdefs": {
        "version": 9,
        "subpath": "",
        "model": None,
    },
    "conversationdefs": {
        "version": 7,
        "subpath": "",
        "model": None,
    },
    "grounditems": {
        "version": 12,
        "subpath": "",
        "model": None,
    },
    "spelldefs": {
        "version": 7,
        "subpath": "",
        "model": None,
    },
    "npcloot": {
        "version": 13,
        "subpath": "",
        "model": models.NPCLoot,
    },
    "questdefs": {
        "version": 3,
        "subpath": "",
        "model": None,
    },
    "pickpocketdefs": {
        "version": 2,
        "subpath": "",
        "model": models.PickpocketDef,
    },
    "worldentitylootdefs": {
        "version": 6,
        "subpath": "",
        "model": None,
    },
    "npcconversationdefs": {
        "version": 2,
        "subpath": "",
        "model": None,
    },
    "worldentityactions": {
        "version": 4,
        "subpath": "",
        "model": None,
    },
    "specialcoordinatesdefs": {
        "version": 1,
        "subpath": "",
        "model": None,
    },
    "appearance": {
        "version": 36,
        "subpath": "carbon/",
        "model": None,
    },
    "creatures": {
        "version": 17,
        "subpath": "carbon/",
        "model": None,
    },
    "heightmaps": {
        "version": 23,
        "subpath": "carbon/",
        "model": None,
    },
    "items": {
        "version": 43,
        "subpath": "carbon/",
        "model": None,
    },
    "meshes": {
        "version": 43,
        "subpath": "carbon/",
        "model": None,
    },
    "textures": {
        "version": 31,
        "subpath": "carbon/",
        "model": None,
    },

    # Static asset files (non-carbon)
    "earthoverworldtexture": {
        "subpath": "assets/heightmaps/",
        "filename": "earthoverworldtexture.png",
        "model": None,
    },
    "earthoverworldmap": {
        "subpath": "assets/heightmaps/",
        "filename": "earthoverworldmap.png",
        "model": None,
    },
    "earthoverworldpath": {
        "subpath": "assets/heightmaps/",
        "filename": "earthoverworldpath.png",
        "model": None,
    },
    "earthskytexture": {
        "subpath": "assets/heightmaps/",
        "filename": "earthskytexture.png",
        "model": None,
    },
    "earthskymap": {
        "subpath": "assets/heightmaps/",
        "filename": "earthskymap.png",
        "model": None,
    },
    "earthskypath": {
        "subpath": "assets/heightmaps/",
        "filename": "earthskypath.png",
        "model": None,
    },
    "earthundergroundtexture": {
        "subpath": "assets/heightmaps/",
        "filename": "earthundergroundtexture.png",
        "model": None,
    },
    "earthundergroundmap": {
        "subpath": "assets/heightmaps/",
        "filename": "earthundergroundmap.png",
        "model": None,
    },
    "earthundergroundpath": {
        "subpath": "assets/heightmaps/",
        "filename": "earthundergroundpath.png",
        "model": None,
    },
    "moontexture": {
        "subpath": "assets/heightmaps/",
        "filename": "moontexture.png",
        "model": None,
    },
    "moonmap": {
        "subpath": "assets/heightmaps/",
        "filename": "moonmap.png",
        "model": None,
    },
    "moonpath": {
        "subpath": "assets/heightmaps/",
        "filename": "moonpath.png",
        "model": None,
    },
}
