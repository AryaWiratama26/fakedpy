from faker import Faker
import pandas as pd

fake = Faker()


def faked(rows: int = 10 , req : list = ["name", "address", "job"]) -> pd.DataFrame:

    """
    Generate fake data to csv

    Parameter :
    
    rows = The number of rows of fake data (int)
    req = The list of columns to include. If None, defaults to ["name", "address", "job"] (List).

    Returns :
    
    pd.DataFrame = Containing the generated fake data

    """
    data = []
    fake_dict = {
        "name" : fake.name,
        "address" : fake.address,
        "job" : fake.job,
        "email" : fake.email,
        "phone_number": fake.phone_number,
        "company": fake.company,
        "text": fake.text,
        "date_of_birth": fake.date_of_birth,
    }    
    
    
    for i in range(rows):
        content = {col: fake_dict[col]() for col in req if col in fake_dict}
        data.append(content)
    
    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=False)
    return df
