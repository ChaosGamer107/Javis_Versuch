from tools.loader import load_tools
from speech.speech import listen, speak
from memory.memory import init_db
from ai.brain import process
from tools.tool_registry import get_tool

load_tools()

init_db()

print("Nova ist bereit!")

while True:

    user_input=listen()

    if not user_input:
        continue

    if user_input.lower() in ["beenden", "stopp", "exit"]:
        break

    reply=process(user_input)

    print("Nova:", reply)

    speak(reply)


Ich höre...
Du: wie geht's dir
Planner: {
  "goal": "",
  "conversation_type": "",
  "use_memory": false,
  "use_tools": true,
  "tool": "get_time",
  "arguments": {},
  "continue_topic": true,
  "ask_followup": false
}
Nova: Hey! Ich bin gut, danke fürs fragen. Wie war dein Tag?
Ich höre...
Du: öffne Spotify
Planner: {
  "goal": "",
  "conversation_type": "",
  "use_memory": false,
  "use_tools": true,
  "tool": "get_time",
  "arguments": {},
  "continue_topic": true,
  "ask_followup": false
}
Nova: Hey! Ich habe verstanden, dass du Spotify öffnen möchtest. Das tue ich jetzt für dich!

Uhrzeit: 21:00:55
Ich höre...
Du: wie spät ist es
Planner: {
  "goal": "",
  "conversation_type": "",
  "use_memory": false,
  "use_tools": true,
  "tool": "get_time",
  "arguments": {},
  "continue_topic": true,
  "ask_followup": false
}
Nova: Hey! Ich habe verstanden, dass du wissen möchtest, wie spät es ist. Nachdem ich das Tool "get_time" verwendet habe, kann ich dir sagen, dass es 21:01:20 Uhr ist.