from fastapi import FastAPI
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
import pandas as pd
import pickle

#import the model
with open('model.pkl','rb') as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

#pydantic model for input data
class InputData(BaseModel):
    age : Annotated[int, Field(...,gt =0,lt =100, description="Age of the person in years")]
    weight : Annotated[float, Field(...,gt =0, description="Weight of the person in kg")]
    height : Annotated[float, Field(...,gt =0,lt =2.5, description="Height of the person in cm")]
    income_lpa: Annotated[float, Field(...,gt =0, description="Income of the person in lakhs per annum")]
    smoker: Annotated[bool,Field(..., description="Is user a smoker")]
    city : Annotated[str, Field(..., description="City of the person")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="occupation of the person")]
    

    @computed_field
    @property
    def bmi(self) ->float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def lifestyle_risk(self)-> str:
        if self.smoker['Smoker'] and self.bmi > 30:
            return "High"
        elif self.smoker['smoker'] or self.bmi > 27:
            return "Medium"
        else:
            return "Low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle-aged"
        else:
            return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post("/predict")
def perdict_premium(input_data: InputData):

    input_df = pd.DataFrame([{
        "bmi": input_data.bmi,
        "age_group": input_data.age_group,
        "lifestyle_risk": input_data.lifestyle_risk,
        "city_tier": input_data.city_tier,
        "income_lpa": input_data.income_lpa,
        "occupation": input_data.occupation
        }])
    
    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': prediction})


