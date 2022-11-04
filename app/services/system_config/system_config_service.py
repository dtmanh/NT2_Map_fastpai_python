from datetime import datetime
import json
from fastapi import HTTPException
from app.models.system_config import SystemConfig
from databases.db import Session

def get_all(db: Session):
    return db.query(SystemConfig).order_by(SystemConfig.id.asc()).all()

def save(db: Session, body):
    
    try:
        exists = True
        settings = db.query(SystemConfig).all()
        if not settings:
            exists = False
        
        if exists:
            for config in body:
                item = db.query(SystemConfig).get(config['id'])
                if item:
                    item.name = config['name']
                    item.key = config['key']
                    item.key_value = json.dumps(config['key_value'])
                    item.type = config['type']
                    item.created_at = config['created_at']
                    item.updated_at = datetime.now()
                    db.commit()
        else:
            for config in body:
                db_setting_config = SystemConfig(
                name=config['name'],
                key=config['key'],
                key_value=json.dumps(config['key_value']),
                type=config['type'],
                created_at=datetime.now(),
                )
                db.add(db_setting_config)
                db.commit()
                
        db.close()
        settings = db.query(SystemConfig).all()
        return settings       
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Lỗi hệ thống.")
   

