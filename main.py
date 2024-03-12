from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import text
from database import SessionLocal, engine
from langchain.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from pprint import pprint
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType

import getpass
import os


app = FastAPI()

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request):
    return {"Hello": "World Something"}

@app.get("/db")
async def database(request: Request):
    db = SQLDatabase(engine)
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key= "AIzaSyAQHuuH2tOzusBJeyIQIRHB2I_YZ-SnXLU")
    # chain = create_sql_query_chain(llm, db)
    # response = chain.invoke({"question": "How many customers are there"})
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    db_agent = create_sql_agent(
        llm = llm,
        toolkit = toolkit,
        agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    result_db = db_agent.invoke("what is the phone number of Atelier graphique")
    print(result_db)
    # result = db.run("SELECT COUNT(*) AS `total_customers` FROM customers;")
    # print(result)
    # execute_query = QuerySQLDataBaseTool(db=db)
    # write_query = create_sql_query_chain(llm, db)
    # chain = write_query | execute_query
    # response = chain.invoke({"question": "How many customers are there"})
    # print(type(result))
    # pprint(list(result.mappings()))
    return {"Hello": "World Something"}

@app.get("/show")
async def get_info(db: Session = Depends(get_database_session)):
    try:
        query = text("select customerName from customers where customerNumber=103")
        result = db.execute(query)
        for row in result.fetchall():
            customer_name = row[0]  # Access the first (and only) element of the tuple
            print(customer_name)
        return JSONResponse({
            "result": customer_name
        })
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)   


@app.get("/prompt/{prompt_value}")
async def read_query(prompt_value: str):
    get_prompt= prompt_value
    query_get = await generate_sql_query(get_prompt)
    print(f"query get {query_get}")
    result_db = await run_sql_query(query_get)
    print(f"result_db  {result_db}")
    formatted_result = await format_response(result_db)
    return formatted_result

async def connect_db(query: str) -> str:
    # Use the LLM to generate a SQL query
    # This is a placeholder function, replace it with actual LLM code
    query_to_return = query
    return query_to_return
  
async def generate_sql_query(query: str) -> str:
    # Use the LLM to generate a SQL query
    # This is a placeholder function, replace it with actual LLM code
    query_to_return = query
    return query_to_return

async def run_sql_query(sql_query: str) -> str:
    # Run the SQL query on the database
    # This is a placeholder function, replace it with actual database interaction code
    return "SQL query result"

async def format_response(result: str) -> str:
    # Format the response
    # This is a placeholder function, replace it with actual response formatting code
    return f"Formatted result: {result}"