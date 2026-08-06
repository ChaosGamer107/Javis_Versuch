from ai.conversation_analyzer import analyze_conversation
from ai.reasoning import build_reasoning
from ai.planner import create_plan
from ai.ai import ask_llama
from ai.prompt_builder import build_prompt
from memory.conversation import set_topic, set_goal, set_mode, set_user_mood, update_conversation
from memory.memory import get_all_facts, get_recent_conversations, search_memories_semantic
from tools.tool_registry import get_tool_discription

def process(user_input):

    analysis=analyze_conversation(user_input)

    set_topic(analysis["topic"])
    set_user_mood(analysis["emotion"])
    set_mode(analysis["type"])
    set_goal(analysis["goal"])

    reasoning=build_reasoning(user_input)

    plan=create_plan(user_input)

    facts=get_all_facts()

    context=search_memories_semantic(user_input)

    conversation=get_recent_conversations()

    tool_text=get_tool_discription()

    prompt=build_prompt(
        user_input,
        analysis,
        reasoning,
        plan,
        facts,
        context,
        conversation,
        tool_text
    )
    reply=ask_llama(prompt)

    update_conversation(
        user_input,
        reply
    )

    return reply