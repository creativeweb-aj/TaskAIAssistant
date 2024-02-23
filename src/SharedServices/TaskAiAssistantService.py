from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from src.SharedServices.AgentTools import list_tables, run_query_tool, describe_tables_tool
from src.config.configurations import OPENAI_API_KEY

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chat = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.0,
    openai_api_key=OPENAI_API_KEY
)


class TaskAssistantService:
    def __init__(self):
        self.tables = list_tables()
        self.tools = [run_query_tool, describe_tables_tool]
        self.systemContext = ("Your role as an AI assistant is to manage database operations in response to user "
                              "commands, focusing on the 'customers', 'project', or 'activities' tables. Utilize "
                              "describe_tables to grasp table structures and seek further details from users as needed."

                              "Key Points: "
                              "Customers Table: Treat 'company name' as 'customer name'. Ensure user inputs align "
                              "with the table schema."
                              "Project Table: Confirm the customer exists before adding a project, matching inputs "
                              "with the table schema."
                              "Activities Table: Recognize 'tasks' as entries for this table, including columns for "
                              "'activity name' (task name), 'description' (task description), 'hours' (work "
                              "duration), and 'date' (when performed). Verify related project existence in the "
                              "project table."
                              
                              "After input validation, use run_postgresql_query to execute PostgreSQL queries, "
                              "adapting to user inputs for any clarifications or additional information needed for "
                              "database success. Always send response in good conversational way to user.")
        self.prompt = self.setChatPrompt()
        self.agent = self.createAgent()

    def setChatPrompt(self):
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(content=self.systemContext),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )
        return prompt

    def createAgent(self):
        agent = OpenAIFunctionsAgent(
            llm=chat,
            prompt=self.prompt,
            tools=self.tools
        )
        return agent

    def runAgent(self, userInput):
        agent_executor = AgentExecutor(
            agent=self.agent,
            memory=memory,
            verbose=True,
            tools=self.tools
        )
        result = agent_executor.invoke(input=userInput)
        return result.get('output', '')
