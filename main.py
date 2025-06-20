from fastapi import FastAPI, Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field,computed_field
from typing import Annotated,Literal,Optional
import json
app = FastAPI()     #create an object of FastAPI

class Patient(BaseModel):
    id: Annotated[str,Field(...,description="id of the patient", example="P001")]
    name:Annotated[str,Field(...,description="Full name of the patient", example="John Doe")]  # Applying metadata to the field
    city: Annotated[str,Field(...,description="City of the patient is living", example="New York")]
    age: Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient", example=30)]
    gender: Annotated[str,Literal['male','female','other'],Field(...,description="gender of the patient")]
    height: Annotated[float,Field(...,gt=0,description="Height of the patient in meters")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the patient in kg")]

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate the Body Mass Index (BMI) of the patient."""
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        """Provide a health verdict based on the BMI."""
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None, gt=0 ,lt=120)]
    gender: Annotated[Optional[Literal['male','female']],Field(default=None)]
    height: Annotated[Optional[float],Field(default=None)]
    weight: Annotated[Optional[float],Field(default=None)]


def load_data():
    with open("patient.json", "r") as f:  # Open the JSON file in read mode
    # Load your data here
        data = json.load(f)
    return data

def save_data(data): #saving data to the json file
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)

@app.get("/") # This is the root endpoint like route

def hello():            # This is the function that will be called when the endpoint is accessed
    return {"message": "Patient management API"}

@app.get("/about")

def about():
    return {"message": "A fully functional API to manage patients and their data."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')

def view_patient(patient_id: str= Path(...,description='ID of the patient',example='P001') ):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')

def sort_data(sort_by: str = Query(..., description="Sort on the basis of height, weight and bmi"), order: str= Query('asc', description="Sort in ascending or descending order")):
    
    valid_sort_by = ['height', 'weight', 'bmi']

    if sort_by not in valid_sort_by:
        raise HTTPException(status_code=400,detail="Invalid sort_by parameter. Choose from height, weight, or bmi.")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400,detail="Invalid order parameter. Choose from asc or desc.")

    data= load_data()

    sort_order = True if order =='desc' else False
    
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=sort_order)

    return sorted_data

#post endpoint to add a new patient

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    patient.model_dump(exclude='id')  # Convert Pydantic model to dict
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)  # Save the updated data 

    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient_id": patient.id})

@app.put('/edit/{patient_id}')
def edit_patient(patient_id: str,patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update the patient data
    existing_patient_info = data[patient_id]

    patient_update_dict = patient_update.model_dump(exclude_unset=True)  # Convert Pydantic model to dict, excluding unset fields
    for key,value in patient_update_dict.items():
        existing_patient_info[key] = value

    #existing patient info is updated with the new data, pydantic object ma change gare
    existing_patient_info['id'] = patient_id
    patient_pydantic_object=Patient(**existing_patient_info)  # Validate the updated data using Pydantic model

    # pydantic obj to dict
    existing_patient_info = patient_pydantic_object.model_dump(exclude=['id'])

    #add dit to data
    data[patient_id] = existing_patient_info

    save_data(data)  # Save the updated data

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})
    
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data= load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    data[patient_id]# Remove the patient from the data
    save_data(data)  # Save the updated data
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})