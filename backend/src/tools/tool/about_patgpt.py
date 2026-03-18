from langchain_core.tools import tool
from src.db.engine import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

@tool
def get_info_keywords(category:str,db:Session=Depends(get_db)):
    """
    Summary:
    This function is used to get the info id and its keywords for PatGPT and its parent company. These keywords are given to give you an abstract idea of the information you are looking for.

    Arguments:
    - category: The category of the information, available categories are,
    1. app : for app related queries 
    2. patgpt_globalspace : for patgpt and its parent company:globalspace related queries
    3. data : for data related queries
    4. billing_and_plans : for billing and plans related queries
    5. default: if LLM is nor descisive about the category it can use "default as category" to retrieve all the information's keywords

    Returns:
    A dictionary with the following keys:
    - info_id: The info id 
    - keywords: The keywords as an abstraction for entire information
    """
    query = db.query(AboutPATGPT)
    query = query.filter(AboutPATGPT.is_active == True)
    if category !="default":
        query = query.filter(AboutPATGPT.category == category)
    query = query.order_by(AboutPATGPT.updated_at.desc()) 
    query = query.first()

    return {
        "info_id": query.id,
        "keywords": query.keywords
    }

@tool
def get_info(info_ids:List[str],db:Session=Depends(get_db)):
    """
    Summary:
    This function is used immediately after get_info_keywords to get the latest information about PatGPT and its parent company based on retrieved keyword from get_info_keywords.

    Arguments:
    - info_ids: The info ids

    Returns:
    A concatenated string of all informations
    """
    query = db.query(AboutPATGPT)
    query = query.filter(AboutPATGPT.is_active == True)
    query = query.filter(AboutPATGPT.id.in_(info_ids))
    query = query.order_by(AboutPATGPT.updated_at.desc()) 
    query = query.first()
    return query.information



info_tools=[get_info_keywords,get_info]
