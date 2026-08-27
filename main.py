"""
CLI Entry Point for the Gen Z AI Joke-Generation Agent.
Handles CLI user input, initiates the LangGraph agent, and simulates the
frontend expandable box for the hidden joke meaning.
"""

import sys
import io
import json
from agent import build_agent_graph

# Force UTF-8 encoding on Windows to prevent UnicodeEncodeError with emojis
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass


# Simple ANSI escape codes for clean terminal formatting
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print(f"\n{Colors.BOLD}{Colors.CYAN}🚀 AI JOKE GENERATOR AGENT (LangGraph & Groq Backend) 🚀{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}================================================================{Colors.ENDC}\n")

def simulate_expandable_box(joke: str, hidden_meaning: str, retry_count: int, is_valid: bool):
    """
    Simulates a frontend UI with a clickable dropdown/expandable box in the CLI.
    """
    print(f"\n{Colors.BOLD}{Colors.GREEN}================ JOKE GENERATION COMPLETE ================{Colors.ENDC}")
    print(f"\n🎤 {Colors.BOLD}Final Joke:{Colors.ENDC}")
    print(f"   {Colors.CYAN}\"{joke}\"{Colors.ENDC}")
    
    print(f"\n📊 {Colors.BOLD}Backend Response Payload (JSON format for Frontend):{Colors.ENDC}")
    metadata = {
        "joke": joke,
        "hidden_meaning": hidden_meaning,
        "is_valid": is_valid,
        "retry_count": retry_count
    }
    print(f"   {Colors.CYAN}{json.dumps(metadata, indent=4)}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}----------------------------------------------------------{Colors.ENDC}")
    print(f"💡 {Colors.BOLD}Boomer / Outsider Translator Simulator:{Colors.ENDC}")
    print(f"   Want to understand the slang? (Simulating expandable dropdown)")
    
    # Wait for keypress
    input(f"   {Colors.WARNING}[Press ENTER to Click & Expand Hidden Meaning 🔓]{Colors.ENDC} ")
    
    print(f"\n📖 {Colors.BOLD}{Colors.GREEN}Expanded Hidden Meaning / Explanation:{Colors.ENDC}")
    print(f"   {Colors.GREEN}{hidden_meaning}{Colors.ENDC}")
    print(f"\n{Colors.BOLD}{Colors.GREEN}=========================================================={Colors.ENDC}\n")

def main():
    print_header()
    app = build_agent_graph()

    while True:
        topic = input(f"{Colors.BOLD}👉 Enter joke topic (e.g. programming, exams, sleep, coffee) or type 'stop' to exit:{Colors.ENDC} ").strip()
        if not topic:
            topic = "programming"
            print(f"{Colors.WARNING}No topic entered. Defaulting to '{topic}'.{Colors.ENDC}")

        if topic.lower() in {"stop", "quit", "exit"}:
            print(f"\n{Colors.BOLD}{Colors.GREEN}👋 Thanks for using the AI Joke Generator. Bye!{Colors.ENDC}")
            break

        initial_state = {
            "topic": topic,
            "joke": "",
            "hidden_meaning": "",
            "is_valid": False,
            "retry_count": 0,
            "validation_errors": [],
            "joke_history": [],
            "best_joke": None,
            "best_hidden_meaning": None,
            "force_fail_first": False  # Run normally without forcing demonstration failure
        }

        try:
            final_state = app.invoke(initial_state)
        except Exception as e:
            print(f"\n{Colors.FAIL}❌ An error occurred during graph execution: {e}{Colors.ENDC}")
            continue

        final_joke = final_state.get("joke")
        final_meaning = final_state.get("hidden_meaning")
        is_valid = final_state.get("is_valid", False)

        if not is_valid:
            final_joke = final_state.get("best_joke", "My code is like my sleep schedule: completely broken and non-existent. 💀")
            final_meaning = final_state.get("best_hidden_meaning", "The joke relates poor coding structures to poor sleep habits using Gen Z exaggeration.")

        simulate_expandable_box(
            joke=final_joke,
            hidden_meaning=final_meaning,
            retry_count=final_state.get("retry_count", 0),
            is_valid=is_valid
        )

        print(f"{Colors.CYAN}Type another topic to keep generating jokes, or type 'stop' to exit.{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
