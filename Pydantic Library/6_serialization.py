from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'farrukhabad', 'state': 'uttar pradesh', 'pin': '209739'}

address1 = Address(**address_dict)

patient_dict = {'name': 'Agam', 'age': 21, 'address': address1}

# unpacking
patient1 = Patient(**patient_dict)

temp = patient1.model_dump(include=['name','gender'])
temp = patient1.model_dump(exclude_unset=True) # exclude_unset -> it exclude values which are not set during object creation

print(temp)
print(type(temp))
