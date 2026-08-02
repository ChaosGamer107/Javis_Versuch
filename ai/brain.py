from conversation_analyzer import analyze_conversation
from reasoning import build_reasoning
from planner import create_plan
from ai import ask_llama
from memory.conversation import set_topic, set_goal, set_mode, set_user_mood, update_conversation

def process(user_input):

    analysis=analyze_conversation(user_input)

    set_topic(analysis["topic"])
    set_user_mood(analysis["emotion"])
    set_mode(analysis["type"])
    set_goal(analysis["goal"])

    reasoning=build_reasoning(user_input)

    plan=create_plan(user_input)

    reply=ask_llama(
        user_input,
        analysis,
        reasoning,
        plan
    )

    update_conversation(
        user_input,
        reply
    )

    return reply