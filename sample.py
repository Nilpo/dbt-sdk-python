from dbtsdk import Dbt
import os

api_key = os.environ['DBT_API_KEY']

dbt = Dbt.Dbt(api_key)

