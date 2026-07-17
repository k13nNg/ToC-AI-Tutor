from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ROUTER_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """You are a query classifier for a Theory of Computation course chatbot.

Classify the query as one of: on_topic, greeting, off_topic.

- "greeting": ONLY greetings ("hi", "hello"), identity questions ("who are you"), or thank you messages.
- "off_topic": ONLY questions clearly unrelated to computer science, math, or academics (e.g. "what's the weather", "tell me a joke", "how to cook pasta").
- "on_topic": EVERYTHING ELSE. Any question about CS, math, logic, automata, languages, computation, or anything that could plausibly relate to a Theory of Computation course is on_topic. When in doubt, classify as on_topic.

Reply with exactly one word: on_topic, greeting, or off_topic."""

GREETING_RESPONSE = (
    "Hi! I'm **Decidr**, your AI tutor for **INFO 47546 – Theory of Computation** "
    "at Sheridan College. I can help you with automata, formal languages, Turing machines, "
    "decidability, complexity theory, and more. What would you like to explore?"
)

OFF_TOPIC_RESPONSE = (
    "I'm only able to help with Theory of Computation topics such as automata, "
    "formal languages, Turing machines, decidability, and complexity theory. "
    "Please ask a related question!"
)


def route(query: str, chat_history: list = []) -> str:
    """Returns one of: 'on_topic', 'greeting', 'off_topic'"""
    context_messages = chat_history[-4:] if chat_history else []

    response = client.chat.completions.create(
        model=ROUTER_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *context_messages,
            {"role": "user", "content": query}
        ],
        temperature=0,
        max_completion_tokens=5
    )
    decision = response.choices[0].message.content.strip().lower()

    if decision.startswith("on_topic"):
        return "on_topic"
    elif decision.startswith("greeting"):
        return "greeting"
    else:
        return "off_topic"
