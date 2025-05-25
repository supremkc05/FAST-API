from pydantic import BaseModel, Field, EmailStr, AnyUrl, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int
    height: float
    weight: float
    bmi: Annotated[float, Field(gt=0, description="Body Mass Index of the patient", examples=24.5)]
    married: Optional[bool] = None
    allergies: List[str]
    contact: Dict[str, str]
    email: EmailStr
    url: AnyUrl

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if not value.endswith('@globalbank.com'):
            raise ValueError('Email must be a globalbank.com email address')
        return value
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if value < 0 or value > 120:
            raise ValueError('Age must be between 0 and 120')
        return value

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.height)
    print(patient.weight)
    print(patient.bmi)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print("Patient data inserted successfully.")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.height)
    print("updated")

patient_info = {
    'name': 'John Doe',
    'age': 30,
    'height': 5.9,
    'weight': 70.5,
    'bmi': 24.5,
    'married': True,
    'allergies': ['peanuts', 'dust'],
    'contact': {'email': 'suprem@globalbank.com', 'phone': '1234567890'},
    'email': 'suprem@g.com',
    'url': 'https://globalbank.com/profile/johndoe'
}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)