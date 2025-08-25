from core.nlp import parse_intent
from core.dispatcher import handle_request

print("🤖 Welcome to AI Cloud Assistant (Multi-Cloud CLI)")
print("   (Type 'exit' to quit)\n")

while True:
    user_input = input("💬 You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    intent, params = parse_intent(user_input)
    result = handle_request(intent, params)
    print(result)
