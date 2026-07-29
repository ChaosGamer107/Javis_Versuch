from conversation_analyzer import analyze_conversation
from reasoning import build_reasoning
from planner import create_plan

def think(user_input):

    analysis=analyze_conversation(user_input)

    reasoning=build_reasoning(user_input)

    plan=create_plan(user_input)

    return {
        "analysis":analysis,
        "reasoning":reasoning,
        "plan":plan
    }