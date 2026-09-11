#so now we are creating a graph
# and the first thing you create is a state

import os

#now create a state
# 1st way --> typed Dictionary
#most common
from typing import TypedDict

class state(TypedDict):
    #create a blueprint
    topic : str
    summary : str
    score : str
    #will be passed to all nodes 

#2nd way - Pydantic Model
#it is good at data validation and type checking
#at runtime

from pydantic import BaseModel , field_validator

class state(BaseModel):
    topic : str
    summary : str
    score : str = "" #default

    @field_validator
    def score_positive(cls , v):
        if v < 0:
            raise ValueError("Score must be positive")


#3rd way -> Python dataclasses
#standard python dataclass but it is used very rarely

from dataclasses import dataclass, field
class state:
    topic : str = ""
    summary : str = ""
    messages : list = field(default_factory=list) #default


from langgraph.graph import MessagesState

class State(MessagesState):
    #messages field is already included with add_messages reducer
    #just add your extra field
    user_name: str
    language: str

