import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_story(story_elements, quiz_data):
    system_prompt = """You are a storyteller for a "Choose Your Own Adventure" story for young children. 
    Create an engaging, interactive story that should be educational and fun for children."""

    user_prompt = f"""Use the following story elements to guide your narrative:
    {story_elements}. 
    
    At the end of the story, use {quiz_data} to create multiple choice questions"""

    # Add debug output for prompts
    print("\n=== LLM Prompt Debug ===")
    print("System Prompt:")
    print(system_prompt)
    print("\nUser Prompt:")
    print(user_prompt)
    print("=" * 50)

    story = ""
    with client.messages.stream(
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        model="claude-3-5-sonnet-20241022",
    ) as stream:
        for text in stream.text_stream:
            story += text
            yield text  # This will stream the text to your web interface

    return story
