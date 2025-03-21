import json
import random

# Define sample assistant types and topics
assistant_types = [
    "knowledgeable", "friendly", "helpful", "cheerful", "professional", "insightful", "funny", "motivational", "scientific", "historical"
]

topics = [
    ("Who discovered the law of gravity?", "Sir Isaac Newton discovered the law of gravity in the 17th century."),
    ("Hello! How are you?", "Hi there! I'm just a bot, but I'm here and happy to help. How about you?"),
    ("Can you help me convert 100°F to Celsius?", "Sure! The formula to convert Fahrenheit to Celsius is (F - 32) × 5/9. So, 100°F is approximately 37.8°C."),
    ("Tell me something fun!", "Did you know that octopuses have three hearts?"),
    ("Can you draft an email for a job application?", "Of course! Here's a professional email template..."),
    ("What is the capital of France?", "The capital of France is Paris."),
    ("What is the speed of light?", "The speed of light is approximately 299,792 kilometers per second."),
    ("Tell me a joke!", "Sure! Why don’t skeletons fight each other? Because they don’t have the guts!"),
    ("What is the meaning of life?", "Many believe it is to seek happiness, knowledge, and contribute to society."),
    ("How do airplanes fly?", "Airplanes fly due to the principles of lift, thrust, drag, and weight.")
]

# Generate 200 sample conversations
conversations = []
for i in range(1, 201):
    assistant_type = random.choice(assistant_types)
    question, answer = random.choice(topics)

    conversation = {
        "id": f"conv{i}",
        "messages": [
            {"role": "system", "content": f"You are a {assistant_type} assistant."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
            {"role": "user", "content": "Thanks!"},
            {"role": "assistant", "content": "You're welcome! Let me know if you have more questions."}
        ]
    }
    conversations.append(conversation)

# Save to a JSON file
with open("dataset.json", "w", encoding="utf-8") as f:
    json.dump(conversations, f, indent=4)

print("200 sample conversation records generated successfully!")
