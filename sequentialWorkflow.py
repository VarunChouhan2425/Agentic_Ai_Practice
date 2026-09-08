from langgraph.graph import StateGraph, START, END  
from pydantic import BaseModel

# creating state
class bmiState(BaseModel):

    weight_kg: float
    height_m: float
    bmi: float | None = None
    category: str | None = None

# creating node
def calculateBmiNode(state:bmiState) -> bmiState :

    weight = state.weight_kg
    height = state.height_m

    calBmi = weight/(height**2)

    state.bmi = round(calBmi, 2)

    return state

def labelBmi(state:bmiState) -> bmiState:

    bmi = state.bmi

    if bmi < 18.5:
        state.category = "Underweight"
    elif 18.5 <= bmi < 25:
        state.category = "Normal"
    elif 25 <= bmi < 30:
        state.category = "Overweight"
    else:
        state.category = "Obese"

    return state

# defininig graph
graph = StateGraph(bmiState)

# adding nodes to graph
graph.add_node('calculate_bmi', calculateBmiNode)
graph.add_node('lable_bmi', labelBmi)

# adding edges to graph
graph.add_edge(START, 'calculate_bmi')
graph.add_edge('calculate_bmi', 'lable_bmi')
graph.add_edge('lable_bmi', END)

# compile the graph
workFlow = graph.compile()

# invoke workFlow
final_state = workFlow.invoke(
    {
        'weight_kg':86, 
        'height_m': 1.8906
    }
)

print(final_state)