from fastapi import FastAPI, HTTPException
from .database import get_connection, init_database, insert_records, read_records, search_record_by_id
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



# создание экземпляра fast api, это уйдет в сваггер
app = FastAPI(
    title="Diabetes Management API",
    description="Self-made API for glucose control with SQLite DB. Самописный API для отслеживания уровня глюкозы у диабетиков с бд SQLite.",
    version="2.1",
)

init_database()

# класс для записи глюкозы
# class GlucoseRecord(BaseModel):
#     id: int
#     user_id: int
#     glucose_level: float
#     glucose_measure: str
#     measurement_time: datetime
#     notes: Optional[str] = None #str or none

class GlucoseRecordInput(BaseModel):
    user_id: int
    glucose_level: float
    glucose_measure: str
    measurement_time: datetime
    notes: Optional[str] = None  # str or none

@app.on_event("startup")
def startup_event():
    init_database()

# эндпоинты
@app.get("/glucose") # декоратор, который сообщает апи, что функция ниже должна обрабатывать get-запросы по маршруту "/glucose"
def get_glucose_records(): # функция, которая выполняется при вызове запроса
    try:
        records = read_records()
    except Exception as e:
        raise HTTPException(status_code=500, detail="А ничо тот факт что не работает ничо...")
    result = []
    for record in records:
        result.append({
            "id": record[0],
            "user_id": record[1],
            "glucose_level": record[2],
            "glucose_measure": record[3],
            "measurement_time": record[4],
            "notes": record[5]
        })
    return result

@app.post("/glucose", status_code=201)
def create_glucose_record(record: GlucoseRecordInput):
    measurement_time_str = record.measurement_time.isoformat()
    try:
        insert_records(record.user_id, record.glucose_level, record.glucose_measure, measurement_time_str, record.notes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Запись о глюкозе успешно создана"}

@app.get("/glucose/{record_id}")
def get_glucose_record_by_id(record_id: int):
    record = search_record_by_id(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail=str("А ничо тот факт что записи с таким id нет??"))
    result = {
        "id": record[0],
        "user_id": record[1],
        "glucose_level": record[2],
        "glucose_measure": record[3],
        "measurement_time": record[4],
        "notes": record[5]
    }
    return result


# @app.put("/glucose/{record_id}", glucose_records=GlucoseRecordInput, updated_record=GlucoseRecordUpdate)
# def update_glucose_record(record: int, GlucoseRecord):
#     try:
#         insert_records(record.user_id, record.glucose_level, record.glucose_measure, measurement_time_str, record.notes)
#
#     raise HTTPException(status_code=404, detail="А ничо тот факт что записи такой нет???")
# #
# @app.delete("/glucose/{record_id}", status_code=204)
# def delete_glucose_record(record_id: int):
#     for index, existing_record in enumerate(glucose_records):
#         if existing_record.id == record_id:
#             glucose_records.remove(existing_record)
#             return
#     raise HTTPException(status_code=404, detail="А ничо тот факт что записи такой нет, мне как ее удалить???")
