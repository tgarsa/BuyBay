import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
from pandas import notnull, read_json
# to have access to PostgreSQL database
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
conexion = psycopg2.connect(
    host=ip,
    port=5432,
    database="BuyBay",
    user="postgres",
    password="lop34sw@D")


class Input(BaseModel):
    df_json: str


app = FastAPI(title="Classification pipeline",
              description="A simple text classifier",
              version="1.0")


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


@app.post('/load_products', tags=["LoadProducts"])
async def post_product(incoming_data: Input,
                             current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
                             ):
    df = read_json(incoming_data.df_json)

    # Access to the database
    cursor = conexion.cursor()
    # Insert data into sold_products_bronze table.
    sql_a = "INSERT INTO sold_products_bronze (license_plate, status, platform, created_at, shipped_at, updated_at, " \
            "sold_price, country, channel_ref, platform_fee) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql_b = "INSERT INTO sold_products_bronze (license_plate, status, platform, created_at, updated_at, sold_price, " \
            "country, channel_ref, platform_fee) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    for cont in range(df.shape[0]):
        data = df.iloc[cont]

        if notnull(data['shipped_at']):
            cursor.execute(sql_a,
                           (data['license_plate'], data['status'], data['platform'], data['created_at'],
                            data['shipped_at'], data['updated_at'], data['sold_price'], data['country'],
                            data['channel_ref'], data['platform_fee']))
        else:
            cursor.execute(sql_b,
                           (data['license_plate'], data['status'], data['platform'], data['created_at'],
                            data['updated_at'], data['sold_price'], data['country'], data['channel_ref'],
                            data['platform_fee']))

        conexion.commit()

    return {"label": 'It done'}


@app.post('/load_graded', tags=["LoadGraded"])
async def post_graded(incoming_data: Input,
                             current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
                             ):
    df = read_json(incoming_data.df_json)

    # Access to the database
    cursor = conexion.cursor()
    # Insert data into graded_products_bronze table.
    sql = "INSERT INTO graded_products_bronze (license_plate, grading_cat, grading_time, created_at, updated_at ) " \
          "values (%s,%s,%s,%s,%s)"

    for cont in range(df.shape[0]):
        data = df.iloc[cont]
        cursor.execute(sql,
                       (data['License_plate'], data['grading_cat'], data['grading_time'], data['created_at'],
                        data['updated_at']))
        conexion.commit()

    return {"label": 'It done'}


@app.post('/load_grading_fees', tags=["LoadGradingFees"])
async def post_grading_fees(incoming_data: Input,
                             current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
                             ):
    df = read_json(incoming_data.df_json)

    # Access to the database
    cursor = conexion.cursor()
    # Insert data into grading_fees_bronze table.
    sql = "INSERT INTO grading_fees_bronze (grading_cat, cost, created_at, updated_at) values (%s,%s,%s,%s)"
    for cont in range(df.shape[0]):
        data = df.iloc[cont]
        cursor.execute(sql, (data['grading_cat'], data['cost'], data['created_at'], data['updated_at']))
        conexion.commit()

    return {"label": 'It done'}


@app.post('/load_transport_cost', tags=["LoadTransportCost"])
async def post_transport_cost(incoming_data: Input,
                             current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
                             ):
    df = read_json(incoming_data.df_json)

    # Access to the database
    cursor = conexion.cursor()
    # Insert data into transport_cost_bronze table.
    sql = "INSERT INTO transport_cost_bronze (country, transport_cost, created_at, updated_at) values (%s,%s,%s,%s)"
    for cont in range(df.shape[0]):
        data = df.iloc[cont]
        cursor.execute(sql, (data['country'], data['transport_cost'], data['created_at'], data['updated_at']))
        conexion.commit()

    return {"label": 'It done'}


@app.post('/load_platform_cost', tags=["LoadPlatformCost"])
async def post_platform_cost(incoming_data: Input,
                             current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
                             ):

    df = read_json(incoming_data.df_json)

    # Access to the database
    cursor = conexion.cursor()
    # Insert data into transport_cost_bronze table.
    sql = "INSERT INTO platform_cost_bronze (platform, cost, created_at, updated_at) values (%s,%s,%s,%s)"
    for cont in range(df.shape[0]):
        data = df.iloc[cont]
        cursor.execute(sql, (data['platform'], data['cost'], data['created_at'], data['updated_at']))
        conexion.commit()

    return {"label": 'It done'}




