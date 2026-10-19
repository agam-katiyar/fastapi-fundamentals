

# Not scalable code
def insert_patient_data(name:str, age:int):
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print('Inserted into db')
    else :
        raise TypeError('Incorrect data type')

    
insert_patient_data('nitish','thirty') ## no type validation

