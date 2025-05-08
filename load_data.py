# load_data.py
import json
import os
from sqlmodel import Session, SQLModel
from app.database import engine
from app import models
from asset_registry import ASSETS

DATA_DIR = "game_asset_files"

# General-purpose JSON loader
def load_json(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Single unified loader
def load_data(session: Session):
    for asset_name, meta in ASSETS.items():
        model_cls = meta.get("model")
        if not model_cls:
            continue

        file_name = meta.get("filename") or f"{asset_name}.{meta['version']}.carbon"
        data = load_json(file_name)

        if hasattr(model_cls, 'from_file'):
            model_cls.from_file(session, data)
        else:
            for record in data:
                obj = model_cls.from_dict(record)
                session.merge(obj)
    session.commit()

if __name__ == "__main__":
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        load_data(session)
