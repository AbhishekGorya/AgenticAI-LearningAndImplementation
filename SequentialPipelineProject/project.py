import os
from typing import TypedDict

#lets create the state first

class pipeline_state(TypedDict):
    raw_input : str
    edited_text : str
    script_w : str
    final_output : str

from langchain_groq import ChatGroq

from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile" , temperature=0.9)

#Now we have to create our nodes ie. Python Function
# will contain a docstring too
#editor node
def editor_node(state: pipeline_state) -> dict:
    """Stage 1: Cleans up grammer, removes types, and refines the tone.
    """
    prompt = (
        "You are an expert copyeditor. Clean up the following raw text. "
        "Fix any grammatical errors, spelling mistakes, and smooth out the transition flow "
        "while keeping the core message intact. Return only the edited text.\n\n"
        f"Text:\n{state['raw_input']}"
    )

    res = llm.invoke(prompt)

    return {"edited_text" : res.content.strip() }

#scripter node
def scriptwriter_node(state: pipelinestate) -> dict:
    """Stage 2: Formats the clean text into an engaging video script style."""
    print("\n--- [Stage 2] Executing Scriptwriter Node ---")
    
    prompt = (
        "You are a charismatic YouTube content creator. Take this edited text and transform "
        "it into a highly engaging, punchy, conversational video script hook. Make it sound "
        "like a real person speaking passionately. Return only the script content.\n\n"
        f"Edited Text:\n{state['edited_text']}"
    )
    
    response = llm.invoke(prompt)
    return {"script_text": response.content.strip()}
  
#translator node

def translator_node(state: pipelinestate) -> dict:
    """Stage 3: Translates the script into natural flowing Hinglish."""
    print("\n--- [Stage 3] Executing Hinglish Translator Node ---")
    
    prompt = (
        "You are an expert content localizer for the Indian market. Take the following script "
        "and convert it into natural, flowing 'Hinglish'. Do not simply translate it sentence-by-sentence "
        "or repeat information. Alternating comfortably between Hindi and English phrases just like "
        "an intellectual tech educator would speak naturally on a live stream. Keep the energy high! "
        "Return only the final Hinglish text.\n\n"
        f"Script:\n{state['script_text']}"
    )
    
    response = llm.invoke(prompt)
    return {"final_output": response.content.strip()}


#Now states and nodes are ready 
#now we will we creating the graphs

#for that we will be connecting the nodes, For this we will be using edges
#edges are very important feature so need to implement them carefully
#most important thing to imp,emnt teh workflow

from langgraph.graph import StateGraph , START , END

#creating the graph
graph = StateGraph(pipeline_state)

#now need to add the nodes in graph
graph.add_node("Editor" , editor_node)
graph.add_node("Scripter" , scriptwriter_node)
graph.add_node("Translator" , translator_node)


#adding edges
graph.add_edge(START,"Editor")
graph.add_edge("Editor","Scripter")
graph.add_edge("Scripter", "Translator")
graph.add_edge("Translator",END)

#compile the graph
app = graph.compile()

result = app.invoke({"raw_input": "Abhishek is a very good man and he deserves all the happiness in the world, he is a quick learner , works hard and smart both, He keeps his family happy and his family love him very much. He is ambitious and dreams always big and works hard too for learning and doing something new in his life"})
#output 
print("Your result is :- \n\n")
print(result["final_output"])