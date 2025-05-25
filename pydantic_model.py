from pydantic import BaseModel, Field,EmailStr, AnyUrl
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, description="Full name of the patient",examples='John Doe')] #i ma applying a metadata to the field
    age: int
    height: float
    weight: float
    bmi: Annotated[float, Field(gt=0, description="Body Mass Index of the patient", examples=24.5)]
    married: Optional[bool] = None
    allergies: List[str]
    contact: Dict[str, str]
    email = EmailStr
    url = AnyUrl

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
        print(patient.weight)
        print(patient.bmi)
        print(patient.married)
        print(patient.allergies)
        print(patient.contact)
        print("updated")
        
patient_info= {'name': 'John Doe', 'age': 30, 'height': 5.9, 'weight': 70.5, 'bmi': 24.5, 'married': True, 'allergies': ['peanuts', 'dust'], 'contact': {'email':'abc@gmail.com', 'phone': '1234567890'}}

patient1=Patient(**patient_info)

insert_patient_data(patient1)