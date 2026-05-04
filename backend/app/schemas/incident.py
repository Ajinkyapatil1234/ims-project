from pydantic import BaseModel

class IncidentCreate(BaseModel):
    component: str
    severity: str

class IncidentResolve(BaseModel):
    rca: str

class IncidentIngest(BaseModel):
    component: str
    severity: str
    message: str
