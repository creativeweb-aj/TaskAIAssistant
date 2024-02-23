from queue import Queue
from threading import Thread
from typing import Optional, Any, Union
from uuid import UUID
from flask import Blueprint, request
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult, GenerationChunk, ChatGenerationChunk
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from src.SharedServices.Authentication import Auth
from src.SharedServices.MainService import StatusType, MainService
from src.SharedServices.TaskAiAssistantService import TaskAssistantService
from src.config.configurations import OPENAI_API_KEY
from src.config.extension import socketio

chatGptApi = Blueprint('ChatGPT view version 1', __name__)


# ------------------------------------------------------------------------------------------

class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue
        self.current_sentence = ""  # Buffer to hold current sentence

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        try:
            # Append token to current sentence
            self.current_sentence += token

            # Check if the token ends with a sentence-ending punctuation
            if token.strip()[-1] in ".!?":
                # If yes, put the complete sentence in the queue
                self.queue.put(self.current_sentence.strip())
                self.current_sentence = ""  # Reset buffer for next sentence
        except Exception as e:
            print(f"Exception --> {e}")

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any
    ) -> Any:
        self.queue.put(None)

    def on_llm_error(
            self,
            error: BaseException,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        self.queue.put(None)


# Initialize ChatOpenAI
chat = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    streaming=True
)


class StreamingChain(LLMChain):
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task():
            self(input, callbacks=[handler])

        Thread(target=task).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token


@socketio.on('ask')
def handle_ask(data):
    print(f"data ---> {data}")
    description = data.get("description", "")

    # System generate message prompt
    systemTemplate = ("Suppose you're a ancient history professor only. So answer only ancient history related "
                      "questions. Question: {question}")
    systemMessagePromptTemplate = SystemMessagePromptTemplate.from_template(systemTemplate)

    # Human input message prompts
    humanTemplate = "{user_question}"
    humanMessagePromptTemplate = HumanMessagePromptTemplate.from_template(humanTemplate)

    # Create chat prompt by passing user input and convert into message string
    chatPrompt = ChatPromptTemplate.from_messages([systemMessagePromptTemplate, humanMessagePromptTemplate])

    # chatPrompt = chatPrompt.format_prompt(user_question=description, question=description).to_messages()

    chain = StreamingChain(llm=chat, prompt=chatPrompt)
    for output in chain.stream(input={"question": description, "user_question": description}):
        print(f"output --> {output}")
        # Send response
        data = {
            "status": StatusType.success.value,
            "data": {
                "answer": output
            },
            "message": "AI Message Successfully Sent!"
        }
        socketio.emit("answer", data)


@chatGptApi.route('/user-input-agent', methods=['POST'])
# @Auth.auth_required
def userInputAgent():
    data = request.json
    description = data.get('description', '')

    try:
        # Run the agent with an input
        taskAssistantService = TaskAssistantService()
        output = taskAssistantService.runAgent(description)
    except Exception as e:
        print("Error executing task:", e)
        output = ''

    # Send response
    data = {
        "status": StatusType.success.value,
        "data": {
            "answer": output
        },
        "message": "AI Message Successfully Sent!"
    }
    return MainService.response(data=data, status_code=200)
