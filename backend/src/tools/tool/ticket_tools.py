from langchain_core.tools import tool

@tool
def get_tickets(user_id:str):
    pass

@tool
def update_ticket(user_id:str):
    pass

@tool
def delete_ticket(user_id:str):
    pass

@tool
def take_follow_up(user_id,ticket_id):
    pass


ticket_tools = [get_tickets,update_ticket,delete_ticket,take_follow_up]