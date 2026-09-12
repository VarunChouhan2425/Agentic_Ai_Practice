from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# initializing model
model = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash"
)

# creating state
class llmState(BaseModel):

    question : str
    answer : str | None = None

parser = PydanticOutputParser(pydantic_object=llmState)

# creating node
def llmQaNode (state: llmState) -> llmState:

    question = state.question

    templet = PromptTemplate(
        template= "Answer the following question {question} {formate_instructions}",
        input_variables=['question'],
        partial_variables={"formate_instructions":parser.get_format_instructions()}
    )   

    prompt = templet.invoke({'question':question})
    response = model.invoke(prompt)
    content = response.content[0]["text"]
    answer = parser.parse(content)

    state.answer = answer.answer

    return state

# creating graph
graph = StateGraph(llmState)

# add node
graph.add_node('llm_qa', llmQaNode)

# add edges
graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)

workFlow = graph.compile()

initial_state = {"question": "was the ai first used in world war?"}
final_state = workFlow.invoke(initial_state)

print(final_state)
