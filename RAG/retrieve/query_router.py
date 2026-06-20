import ollama

ROUTER_MODEL = "llama3.2"

SYSTEM_PROMPT = """Classify the user's query into exactly one of three categories:

- "on_topic": any question asking to understand, explain, or get an example of a theoretical computer science concept — including automata, regular expressions, Kleene star, formal languages, grammars, Turing machines, decidability, computability, and complexity. Be lenient with typos. Also classify as on_topic if the query is a follow-up, clarification, or example request referring to the previous conversation.
- "greeting": greetings, identity questions ("who are you"), thank you messages, or small talk.
- "off_topic": anything else, including study tips, how to succeed in the course, advice, opinions, or questions unrelated to theoretical computer science concepts.

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
    # Include last exchange so the router understands follow-up questions
    context_messages = chat_history[-4:] if chat_history else []

    response = ollama.chat(
        model=ROUTER_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *context_messages,
            {"role": "user", "content": query}
        ]
    )
    decision = response["message"]["content"].strip().lower()

    if decision.startswith("on_topic"):
        return "on_topic"
    elif decision.startswith("greeting"):
        return "greeting"
    else:
        return "off_topic"
