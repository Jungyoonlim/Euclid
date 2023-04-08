import logging
from datetime import datetime, timedelta
from typing import List, Optional
from langchain.llms import openai as llms_openai
from langchain.schema import Object, Text
from langchain import create_extraction_chain  

#Congifure logging
logging.basicConfig(level=logging.INFO)

llm = llms_openai.ChatOpenAI(
    model_name = "gpt-3.5-turbo",
    temperature = 0,
    max_tokens = 2000,
    frequency_penalty = 0,
    presence_penalty = 0,
    top_p = 1.0,
)

schema = Object(
    id = "spaced_rep",
    description = "Spaced Repetition Algorithm",
    attributes = [
        Text(
            id="user_id",
            description="A unique identifier for each student.",
            examples=[],
        ),
        Text(
            id="question",
            description="The question to be asked",
            examples=[],
        ),
        Text(
            id="answer",
            description="The answer to the question",
            examples=[],
        ),
        Text(
            id="last_asked",
            description="The last date the question was asked",
            examples=[],
        ),
        Text(
            id="interval",
            description="The current interval for the question",
            examples=[],
        ),
        Text(
            id="repetitions",
            description="The current number of repetitions for the question",
            examples=[],
        ),
        Text(
            id="ease_factor",
            description="The ease factor for the question",
            examples=[],
        ),
        Text(
            id="correct",
            description="Whether the previous answer was correct or not",
            examples=[],
        ),
    ],
    many=False,
)

chain = create_extraction_chain(llm, schema, encoder_or_encoder_class="json")


class Flashcard:
    """
    A flashcard class manages spaced repetition flaschards for a user. 
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.questions: List[dict]=[]

    def add_question(self, question: str, answer: str) -> None: 
        """
        Add a question to the flashcard.

        """
        self.questions.append({
            "question": question,
            "answer": answer,
            "next_review": datetime.now(),
            "interval": 1,
            "easiness_factor": 2.5,
            "repetitions": 0,
            "last_asked": None,
        })

    def get_question(self) -> Optional[str]:
        """
        Get a question for review.

        :return: The question text or None if there are no questions to review.
        """
        for q in self.questions:
            if q["last_asked"] is None or datetime.now() >= q["next_review"] + timedelta(days=q["interval"]):
                question = q
                break
        else:
            return None 
        
        result = chain.predict_and_parse(text=question["question"])
        question_text = result["data"].get("question")
        if question_text is None:
            return None
        
        question["last_asked"] = datetime.now()
        question["repetitions"] += 1
        return question_text

    def answer_question(self, question_text: str, correct: bool) -> Optional[str]:
        """
        Answer a question and update its review status. 
        Using the SM-2 spaced repetition algorithm. 

        :param question_text: The question text.
        :param correct: Whether the answer is correct.
        :return: The answer to the question.
        """
        question = None
        for q in self.questions:
            if q["question"] == question_text:
                question = q
                break
        else:
            return None 
        
        question["repetitions"] += 1
        if correct:
            if question["repetitions"] == 1:
                question["interval"] = 1
            elif question["repetitions"] == 2:
                question["interval"] = 6
            else:
                question["interval"] = int(question["interval"] * question["easiness_factor"])

            question["easiness_factor"] = max(1.3, question["easiness_factor"] + 0.1 - (5 - 5) * (0.08 + (5 - 5) * 0.02))
        else:
            question["repetitions"] = 0
            question["interval"] = 1

        question["next_review"] = datetime.now() + timedelta(days=question["interval"])
        return question["answer"]