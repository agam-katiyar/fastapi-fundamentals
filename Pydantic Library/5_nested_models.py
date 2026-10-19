# Using some pydantic model inside another pydantic model as a field
from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

## Adress pydantic model used inside Patient pydantic model
class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'Farrukhabad', 'state': 'UP', 'pin': '209739'}

address1 = Address(**address_dict)

patient_dict = {'name': 'Agam', 'gender': 'male', 'age': 21, 'address': address1}

patient1 = Patient(**patient_dict)

print(patient1)

print(patient1.name)
print(patient1.address.city)
print(patient1.address.pin)


# Exporting model ad python dictionary format
temp = patient1.model_dump()
print(temp)
print(type(temp))

# exporting as json format
temp = patient1.model_dump_json()

# Better organization of related data (e.g., vitals, address, insurance)

# Reusability: Use Vitals in multiple models (e.g., Patient, MedicalRecord)

# Readability: Easier for developers and API consumers to understand

# Validation: Nested models are validated automatically—no extra work needed
