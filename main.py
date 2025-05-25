from fastapi import FastAPI, Path,HTTPException,Query
import json
app = FastAPI()     #create an object of FastAPI

def load_data():
    with open("patient.json", "r") as f:  # Open the JSON file in read mode
    # Load your data here
        data = json.load(f)
    return data


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