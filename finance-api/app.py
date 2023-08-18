import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
# to have access to PostgresSQL database
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
register_adapter(np.int64, AsIs)
# To add security
import security as sec
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta


# Our ip
# ip = '192.168.178.35'
# Raspberry pi 3
ip = '192.168.178.172'

# To connect with the database
connexion = psycopg2.connect(
    host=ip,
    port=5432,
    database="BuyBay",
    user="postgres",
    password="lop34sw@D")


class Input(BaseModel):
    license_plate: str


app = FastAPI(title="Partners API.",
              description="A simple API to recover data",
              version="1.0")


# Puede que sea adecuado sacarlo de aquí.
def _to_dataframe(cursor, columns):
    '''
    This function build a dataframe with the data downloaded by the query and using the columns' name.
    :param cursor: Access to the database
    :param columns: Name of the table's columns
    :return: The DataFrame
    '''

    df = pd.DataFrame(columns=columns)
    for fila in cursor:
        df = pd.concat([df, pd.DataFrame(pd.Series(fila, columns)).transpose()])
    return df.reset_index(drop=True)


# These are the functions that help us to recover the data
def _get_product_data(license_plate):
    # Access to the database
    cursor = connexion.cursor()

    # Recover the necessary data from the sold_products_gold table.
    sql = "select license_plate, sold_price, transport_cost, platform_fee, grading_fee, updated_at " \
          "from products_gold " \
          "where license_plate = '{}'".format(license_plate)

    # Recover the data
    cursor.execute(sql)

    # Build the dict that I will return
    return_dict = {}

    if cursor.rowcount == 0:
        print('The Product is not in our Database')
    elif cursor.rowcount == 1:
        for fila in cursor:
            return_dict['license_plate'] = fila[0]
            return_dict['sold_price'] = fila[1]
            return_dict['transport_cost'] = fila[2]
            return_dict['platform_fee'] = fila[3]
            return_dict['grading_fee'] = fila[4]
            return_dict['last-update'] = fila[5]
    else:
        print("Multiples product with the same license_plate")

    return return_dict


# These are the API definition.
@app.post("/token", response_model=sec.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = sec.authenticate_user(sec.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=sec.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = sec.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/partner_data', tags=["PartnerAPI"])
async def partner_api(
        incoming_data: Input,
        current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
):

    # license_plate. Our input data
    license_plate = incoming_data.license_plate
    int_dict = _get_product_data(license_plate)
    int_dict['buybay_fee'] = round(0.1 * int_dict.get('sold_price'), 2)
    int_dict['partner_payout'] = int_dict.get('sold_price')-int_dict.get('buybay_fee')-int_dict.get('transport_cost')\
                                 -int_dict.get('platform_fee')-int_dict.get('grading_fee')

    return_dict = {}
    return_dict['metadata'] = {'last-update': int_dict.get('last-update')}
    del int_dict['last-update']
    return_dict['product'] = int_dict

    return return_dict


@app.get('/finance_report', tags=["Finance Report"])
async def finance_report(
        current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
):

    # Connected to the server
    cursor = connexion.cursor()

    sql = "select platform, created_at, sold_price, " \
          "(0.1 * sold_price) + platform_fee + grading_fee as Total_fees, transport_cost " \
          "from products_gold"
    cursor.execute(sql)
    columns = ['platform', 'created_at', 'sold_price', 'total fees', 'transport cost']
    df = _to_dataframe(cursor, columns)
    df['created_at'] = df['created_at'].apply(lambda x: str(x)[:10])
    df['partner_payout'] = df[['sold_price', 'total fees', 'transport cost']].apply(
        lambda x: x[0] - x[1] - x[2], axis=1)
    df_exit = df.groupby(['platform', 'created_at']).sum()
    df_exit.reset_index(inplace=True)
    return df_exit.to_json()
