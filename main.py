from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# создание экземпляра fast api, это уйдет в сваггер
app = FastAPI(
    title="Diabetes Management API",
    description="Self-made API for glucose control. Самописный API для отслеживания уровня глюкозы у диабетиков.",
    version="1.0",

)

# класс для записи глюкозы
class GlucoseRecord(BaseModel):
    id: Optional[int] = None #int or none
    user_id: int
    glucose_level: float
    measurement_time: datetime
    notes: Optional[str] = None #str or none

# вместо БД
glucose_records: List[GlucoseRecord] = [  # в этой переменной будет храниться список объектов, каждый из которых соответствует модели GlucoseRecord
    GlucoseRecord(
        id=1,
        user_id=1,
        glucose_level=7.5,
        measurement_time=datetime(2025, 2, 19, 8, 0),
        notes="Натощак"
    ),
    GlucoseRecord(
        id=2,
        user_id=1,
        glucose_level=9.0,
        measurement_time=datetime(2025, 2, 19, 10, 30),
        notes="После еды"
    )
]

# эндпоинты
@app.get("/glucose") # декоратор, который сообщает апи, что функция ниже должна обрабатывать get-запросы по маршруту "/glucose"
def get_glucose_records(): # функция, которая выполняется при вызове запроса
    return glucose_records

@app.get("/glucose/{record_id}") #
def get_glucose_records():
    return glucose_records

@app.post("/glucose")
def create_glucose_record(record: GlucoseRecord):
    new_id = max([r.id for r in glucose_records], default=0) + 1 # вычисляем новый айди, если записей нет - 0
    record.id = new_id
    glucose_records.append(record)
    return record

@app.put("/glucose/{record_id}", response_model=GlucoseRecord)
def update_glucose_record(record_id: int, updated_record: GlucoseRecord):
    for index, existing_record in enumerate(glucose_records):
        if existing_record.id == record_id:
            updated_data = updated_record.dict(exclude_unset=True)  # обновляем только то, что передал пользователь, остальное без изменений, так как это удобнее и безопаснее для пользователей, и вообще мой апи - что хочу то и делаю!
            updated_glucose_record = GlucoseRecord(**{**existing_record.dict(), **updated_data, "id": record_id})
            glucose_records[index] = updated_glucose_record
            return updated_glucose_record

    raise HTTPException(status_code=404, detail="А ничо тот факт что записи такой нет???")

@app.delete("/glucose/{record_id}", status_code=204)
def delete_glucose_record(record_id: int):
    for index, existing_record in (glucose_records):
        if existing_record.id == record_id:
            glucose_records.remove(existing_record)
            return
    raise HTTPException(status_code=404, detail="А ничо тот факт что записи такой нет, мне как ее удалить???")
