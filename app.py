from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from collections import Counter
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/public", StaticFiles(directory="public"), name="public")

# Serve index.html at root
@app.get("/")
def read_index():
    return FileResponse(os.path.join("public", "index.html"))

# SQLite setup
DATABASE_URL = "sqlite:///./survey.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SurveyResponseDB(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(50), nullable=True)
    department = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=True)
    residence = Column(String(50), nullable=True)
    attendance = Column(String(50), nullable=True)
    reason = Column(Text, nullable=True)
    vision = Column(String(100), nullable=True)
    fecamds = Column(String(100), nullable=True)
    academic = Column(String(100), nullable=True)
    connection = Column(String(100), nullable=True)
    sports = Column(String(100), nullable=True)
    social = Column(String(100), nullable=True)
    spiritual = Column(String(100), nullable=True)
    male_barrier = Column(String(100), nullable=True)
    male_solution = Column(String(100), nullable=True)
    best_day = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    venue = Column(String(100), nullable=True)
    transport = Column(Integer, nullable=True)
    communication = Column(String(100), nullable=True)
    role = Column(String(100), nullable=True)
    leadership = Column(String(100), nullable=True)
    alumni = Column(String(100), nullable=True)
    idea = Column(Text, nullable=True)
    thoughts = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)

class SurveyResponse(BaseModel):
    level: str = None
    department: str = None
    gender: str = None
    residence: str = None
    attendance: str = None
    reason: list = []
    vision: str = None
    fecamds: str = None
    academic: str = None
    connection: str = None
    sports: str = None
    social: str = None
    spiritual: str = None
    male_barrier: str = None
    male_solution: str = None
    best_day: str = None
    duration: str = None
    venue: str = None
    transport: int = None
    communication: str = None
    role: str = None
    leadership: str = None
    alumni: str = None
    idea: str = None
    thoughts: str = None

@app.post("/submit")
async def submit_survey(response: SurveyResponse):
    db = SessionLocal()
    db_response = SurveyResponseDB(
        level=response.level,
        department=response.department,
        gender=response.gender,
        residence=response.residence,
        attendance=response.attendance,
        reason=','.join(response.reason) if response.reason else None,
        vision=response.vision,
        fecamds=response.fecamds,
        academic=response.academic,
        connection=response.connection,
        sports=response.sports,
        social=response.social,
        spiritual=response.spiritual,
        male_barrier=response.male_barrier,
        male_solution=response.male_solution,
        best_day=response.best_day,
        duration=response.duration,
        venue=response.venue,
        transport=response.transport,
        communication=response.communication,
        role=response.role,
        leadership=response.leadership,
        alumni=response.alumni,
        idea=response.idea,
        thoughts=response.thoughts
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    db.close()
    return {"message": "Response saved successfully"}

@app.get("/results")
async def get_results():
    db = SessionLocal()
    rows = db.query(SurveyResponseDB).all()
    db.close()
    if not rows:
        return {}
    results = {}
    # Get all columns except id
    columns = [c.name for c in SurveyResponseDB.__table__.columns if c.name != 'id']
    for col in columns:
        values = [getattr(row, col) for row in rows if getattr(row, col) is not None]
        if col == 'reason':
            values = [item for sublist in [v.split(',') for v in values if v] for item in sublist]
        if col == 'idea' or col == 'thoughts':
            results[col] = values
        else:
            results[col] = dict(Counter(values))
    return results 
