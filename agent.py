"""
AI Joke Generation Agent backend using Python, LangGraph, LangChain, and Groq.
This file defines the shared graph state, the validation logic, the nodes,
the conditional routing, and compiles the LangGraph workflow.
"""

import os
import sys
import io
from typing import TypedDict, List, Dict, Any, Optional
from dotenv import load_dotenv

# Import LangChain & Groq components
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq

# Import LangGraph components
from langgraph.graph import StateGraph, START, END

# Force UTF-8 encoding on Windows to prevent UnicodeEncodeError with emojis
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass


# Load environment variables from the .env file
load_dotenv()

# Common emoji list used for meme-style joke validation and punctuation checks
GENZ_EMOJIS = ["💀", "😭", "🔥", "💯", "🤡", "🤖", "💅", "👀", "🧠", "🧢", "🐐", "✨", "💥"]

# ==========================================
# 1. SHARED GRAPH STATE DEFINITION
# ==========================================

class AgentState(TypedDict):
    """
    Represents the shared memory (state) of our LangGraph workflow.
    """
    topic: str                      # The topic for the joke
    joke: str                       # The current generated joke text
    hidden_meaning: str             # The hidden meaning/explanation of the joke
    is_valid: bool                  # Boolean flag indicating if the joke passed validation
    retry_count: int                # Counter tracking how many times the joke has been regenerated
    validation_errors: List[str]    # List of reasons why the joke failed validation (if any)
    joke_history: List[Dict[str, Any]] # History log of all attempts
    best_joke: Optional[str]        # The best joke generated so far (fallback)
    best_hidden_meaning: Optional[str] # The hidden meaning corresponding to the best joke
    force_fail_first: bool          # Toggle to force a validation failure for demo purposes


# ==========================================
# 2. LLM INITIALIZATION AND HELPER
# ==========================================

def get_groq_llm(streaming: bool = True) -> ChatGroq:
    """
    Initializes and returns a ChatGroq LLM instance.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("\n❌ ERROR: GROQ_API_KEY is missing in your .env file!", file=sys.stderr)
        sys.exit(1)

    model_name = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    
    return ChatGroq(
        model_name=model_name,
        temperature=0.9,
        groq_api_key=api_key,
        streaming=streaming,
    )


# ==========================================
# 3. WORKFLOW NODES IMPLEMENTATION
# ==========================================

def generate_joke_node(state: AgentState) -> AgentState:
    """
    NODE: JOKE GENERATOR
    Generates a brand new meme-style joke based on the topic.
    """
    topic = state.get("topic", "life")
    llm = get_groq_llm(streaming=True)
    parser = JsonOutputParser()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are the funniest meme expert, meme lord, and master of brainrot, irony, and absurd internet jokes.
Your goal is to generate one meme-style joke about the given topic, along with a hidden explanation/meaning of the joke.

Meme-style guidelines:
- Make this the funniest, most viral-feeling joke you can write about the topic.
- Sound silly, playful, and child‑friendly, aiming for a laugh that even a small kid would enjoy.
- Use popular internet slang and meme terms naturally .
- Blend it with meme-style structure and references: think POV memes, witty comparisons, absurd internet imagery, and loud meme energy.
- Infuse 90's Bollywood movies and TV shows  flair: think dramatic hero monologues, classic song references, iconic dialogues , melodramatic expressions, and Hindi film tropes for comedic effect.
- Prioritize a ridiculous, laugh-out-loud punchline; avoid boring or generic lines.
- Add a twist, self-deprecating edge, or absurd comparison tied to the topic.
- Keep the joke safe, non-offensive, and understandable.
- Use punctuation as part of the joke: end with a strong emoji or punctuation mark like "!", "?", or "..." for maximum punch.
- Make it feel like a viral tweet, Discord roast, or meme caption.
- The joke must contain a strong punchline or humorous structure (e.g. setup-punchline, POV, "my sleep schedule is sponsored by...", "me trying to...").
- **Avoid reaction‑based phrasing; aim for a simple, easy‑to‑laugh punchline.**.

You must return a JSON object with exactly two keys:
1. "joke": The meme-style joke (string).
2. "hidden_meaning": A clear, simple explanation of what the joke means and the slang used, so that an outsider or boomer can understand it (string).

Do not include any pre-text or post-text outside the JSON block. Output ONLY a valid JSON object.
"""),
        ("user", "Generate a joke about this topic: {topic}")
    ])
    
    chain = prompt | llm | parser
    
    print("\nCooking a joke...", flush=True)
    print("✨ Joke: ", end="", flush=True)
    
    final_data = {}
    current_joke = ""
    
    try:
        for chunk in chain.stream({"topic": topic}):
            if isinstance(chunk, dict):
                final_data.update(chunk)
                if "joke" in chunk and chunk["joke"]:
                    new_joke = chunk["joke"]
                    if len(new_joke) > len(current_joke):
                        added_text = new_joke[len(current_joke):]
                        print(added_text, end="", flush=True)
                        current_joke = new_joke
    except Exception:
        # Fallback if streaming has connection/parsing issues
        final_data = chain.invoke({"topic": topic})
        print(final_data.get("joke", ""))

    print("", flush=True)  # Newline
    
    joke = final_data.get("joke", "").strip()
    hidden_meaning = final_data.get("hidden_meaning", "").strip()

    if joke and not (joke.endswith(tuple(".,!?")) or any(joke.endswith(emoji) for emoji in GENZ_EMOJIS)):
        joke = joke.rstrip() + "!"
    
    return {
        **state,
        "joke": joke,
        "hidden_meaning": hidden_meaning,
    }


def validate_joke_node(state: AgentState) -> AgentState:
    """
    NODE: VALIDATOR
    Checks if the generated joke matches quality guidelines using Python heuristics.
    """
    joke = state.get("joke", "").strip()
    errors = []
    
    # 1. Check for Forced Simulation Error (for educational/testing purposes)
    if state.get("force_fail_first", False) and state.get("retry_count", 0) == 0:
        errors.append("Forced demonstration quality fail.")
    else:
        # 2. Not Empty Check
        if not joke:
            errors.append("Joke is empty.")
        
        # 3. Length Check
        if len(joke) < 15:
            errors.append("Joke is too short.")
        elif len(joke) > 180:
            errors.append("Joke is too long.")
            
        # 4. Punctuation & Expressive Emoji Check
        has_ending_punctuation = joke.endswith(tuple(".,!?"))
        has_ending_emoji = any(joke.endswith(emoji) for emoji in GENZ_EMOJIS)
        has_punctuation = any(char in ".,!?;:-()\"'/" for char in joke)
        has_emoji = any(emoji in joke for emoji in GENZ_EMOJIS)

        if not has_punctuation and not has_emoji:
            errors.append("Joke lacks expressive punctuation or emojis.")
        elif not (has_ending_punctuation or has_ending_emoji):
            errors.append("Joke should end with punctuation or an emoji for a strong finish.")
            
        # 5. Conversational & Slang Check
        conversational_markers = [
            "my", "i", "me", "you", "when", "like", "literally", "no cap", "fr", 
            "tbh", "ngl", "bro", "bruh", "cooking", "cooked", "rizz", "delulu", 
            "main character", "side quest", "skibidi", "brainrot", "opps", "chat",
            "pov", "she", "he", "we", "they", "just", "so", "am", "is", "are", "aura"
        ]
        joke_lower = joke.lower()
        has_conversational = any(marker in joke_lower for marker in conversational_markers)
        if not has_conversational:
            errors.append("Joke lacks conversational flow or slang.")

    is_valid = len(errors) == 0
    
    best_joke = state.get("best_joke")
    best_hidden = state.get("best_hidden_meaning")
    
    if is_valid or not best_joke:
        best_joke = joke
        best_hidden = state.get("hidden_meaning")
    
    history_entry = {
        "joke": joke,
        "hidden_meaning": state.get("hidden_meaning"),
        "retry": state.get("retry_count", 0),
        "is_valid": is_valid,
        "errors": errors.copy()
    }
    
    joke_history = state.get("joke_history", [])
    if joke_history is None:
        joke_history = []
    updated_history = joke_history + [history_entry]
    
    return {
        **state,
        "is_valid": is_valid,
        "validation_errors": errors,
        "best_joke": best_joke,
        "best_hidden_meaning": best_hidden,
        "joke_history": updated_history
    }


def regenerate_joke_node(state: AgentState) -> AgentState:
    """
    NODE: REGENERATOR / POLISHER
    Invokes the LLM to rewrite and polish the joke based on validator feedback.
    """
    retry_count = state.get("retry_count", 0) + 1
    
    topic = state.get("topic", "life")
    failed_joke = state.get("joke", "")
    errors_str = "\n".join([f"- {err}" for err in state.get("validation_errors", [])])
    
    llm = get_groq_llm(streaming=True)
    parser = JsonOutputParser()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are the funniest meme expert, meme lord, and master of brainrot, irony, and absurd internet jokes.
A previous joke you generated was rejected by our strict Validator because it didn't meet quality criteria.
Your job is to REWRITE and POLISH the joke to make it much better, while specifically fixing the validation failures.

Meme-style guidelines:
- Make this the funniest, most viral-feeling joke you can write about the topic.
- Sound silly, playful, and child‑friendly, aiming for a laugh that even a small kid would enjoy.
- Use popular internet slang and meme terms naturally .
- Blend it with meme-style structure and references: use POV captions, "that feeling when", witty comparisons, or main character flex.
- Infuse 90's Bollywood flair: think dramatic hero monologues, classic song references, iconic dialogues , melodramatic expressions, and Hindi film tropes for comedic effect.
- Avoid weak or generic punchlines; make the punchline surprising, sharp, and specific to the topic.
- Prioritize a laugh-worthy, internet-ready line that feels like a viral caption or Discord roast.
- Make the response feel like the funniest meme caption or roast possible.
- Use punctuation as part of the joke: end with a strong emoji or punctuation mark like "!", "?", or "...".
- Use expressive punctuation, emoji, or internet-style reaction tone.
- The joke must remain safe, non-offensive, and understandable.
- Avoid reaction‑based phrasing; aim for a straightforward, easy‑to‑laugh punchline.

You must return a JSON object with exactly two keys:
1. "joke": The polished and improved meme-style joke (string).
2. "hidden_meaning": A clear, simple explanation of the new joke for outsiders (string).

Do not include any pre-text or post-text outside the JSON block. Output ONLY a valid JSON object.
"""),
        ("user", """Here is the original topic: {topic}
Here is the previous JOKE that failed validation: "{failed_joke}"
Here are the validation failures identified by the Validator:
{validation_errors}

Please rewrite and improve this joke. Ensure all validation failures are fully fixed and the humor is top-tier!""")
    ])
    
    chain = prompt | llm | parser
    
    print("\nQuality check failed. Refining joke...", flush=True)
    print("✨ Polished Joke: ", end="", flush=True)
    
    final_data = {}
    current_joke = ""
    
    try:
        for chunk in chain.stream({
            "topic": topic,
            "failed_joke": failed_joke,
            "validation_errors": errors_str
        }):
            if isinstance(chunk, dict):
                final_data.update(chunk)
                if "joke" in chunk and chunk["joke"]:
                    new_joke = chunk["joke"]
                    if len(new_joke) > len(current_joke):
                        added_text = new_joke[len(current_joke):]
                        print(added_text, end="", flush=True)
                        current_joke = new_joke
    except Exception:
        final_data = chain.invoke({
            "topic": topic,
            "failed_joke": failed_joke,
            "validation_errors": errors_str
        })
        print(final_data.get("joke", ""))

    print("", flush=True)  # Newline
    
    joke = final_data.get("joke", "").strip()
    hidden_meaning = final_data.get("hidden_meaning", "").strip()

    if joke and not (joke.endswith(tuple(".,!?")) or any(joke.endswith(emoji) for emoji in GENZ_EMOJIS)):
        joke = joke.rstrip() + "!"
    
    return {
        **state,
        "joke": joke,
        "hidden_meaning": hidden_meaning,
        "retry_count": retry_count
    }


# ==========================================
# 4. GRAPH ROUTING LOGIC
# ==========================================

def route_after_validation(state: AgentState) -> str:
    """
    CONDITIONAL ROUTER:
    """
    if state["is_valid"]:
        return "valid"
    else:
        retries = state.get("retry_count", 0)
        if retries >= 3:
            return "retry_limit_reached"
        else:
            return "invalid"


# ==========================================
# 5. GRAPH COMPILATION
# ==========================================

def build_agent_graph() -> StateGraph:
    """
    Assembles the StateGraph, registers nodes, draws edges, and compiles the workflow.
    """
    workflow = StateGraph(AgentState)
    
    workflow.add_node("generate_joke", generate_joke_node)
    workflow.add_node("validate_joke", validate_joke_node)
    workflow.add_node("regenerate_joke", regenerate_joke_node)
    
    workflow.add_edge(START, "generate_joke")
    workflow.add_edge("generate_joke", "validate_joke")
    workflow.add_edge("regenerate_joke", "validate_joke")
    
    workflow.add_conditional_edges(
        "validate_joke",
        route_after_validation,
        {
            "valid": END,
            "retry_limit_reached": END,
            "invalid": "regenerate_joke"
        }
    )
    
    return workflow.compile()
