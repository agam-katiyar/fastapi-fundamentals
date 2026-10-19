from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of patient',examples=['P001'] )]
    name: Annotated[str,Field(..., description='Name of patient')]
    city: Annotated[str, Field(...,description='City where patient is living')]
    age: Annotated[int, Field(..., description='Age of patient')]
    gender: Annotated[Literal['male','female','others'],Field(..., description='Gender of patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of patient in mtrs')]
    weight: Annotated[float, Field(..., description=' Weight of patient in kgs')]

    @computed_field
    @property
    def bmi(self)-> float:
        bmi = round(self.weight / (self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male','female','others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

        
def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

    

# route definitions and endpoints
@app.get("/")
def hello():
    return {"message":"Patient management system"}

@app.get("/about")
def about():
    return {"message":" Fully functional API to manage your patient records"}

@app.get('/view')
def view():
    data = load_data()
    return data

# get patient data by patient id and proper http request status
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', examples='P001')):
    #load all the pateint's data
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail='Patient not found')

# getting patient data and sorting
@app.get('/sort')
def sort_patients(sort_by :str = Query(...,description='Sort on the basis of height, weight, or bmi'), order: str = Query('asc',description="sort in asc or desc order")):
    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail =f'Invalid field, select from{valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail="Invalid order select b/w asc & desc")

    data = load_data()

    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

# endpoint for Creating patient
@app.post('/create')
def create_patient(patient: Patient): # receives data from user in patient pydantic data type 
    
    # load existing data
    data = load_data()

    # check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    # add new patient to db
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save new data into json file
    save_data(data)
    # returning json response
    return JSONResponse(status_code=201, content={'message':'Patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    ## checking existence of patientid in data
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    # extracting existing patient's data
    existing_patient_info = data[patient_id]

    # converting update data into dictionary
    updated_patient_info = patient_update.model_dump(exclude_unset=True) # exclude fields which are not provided to update

    # updating new value in dictionary
    for key,value in updated_patient_info.items():
        existing_patient_info[key]= value

    # converting existing dictionary into pydantic object to update calculating fields also(bmi, verdict)
    #existing_patient_info -> pydantic object -> update bmi + verdict

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)


    # -> pydantic object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude={'id'})

    # adding this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':"Patient details updated"})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load tha data
    data = load_data()

    # Checking existence of patient
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    # deleting
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patient is deleted'})