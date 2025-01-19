import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_story(story_elements, quiz_data):
    print("\n=== Story Elements Debug ===")
    print("Raw story_elements received by generate_story:")
    for element in story_elements:
        print(f"Element: {element}")
    print("=" * 50)

    system_prompt = """
    The storytelling system integrates educational content into engaging narratives by following key principles for structure and presentation. Stories should begin with a strong scene-setting paragraph that establishes the magical or fantastical elements, followed by character introductions that reveal traits which will later serve as vehicles for delivering educational content. These traits should feel natural while functioning as mnemonic devices.
Educational facts should never be presented directly, but rather woven into character dialogue and plot developments. For example, historical dates can become prophecies, geographical features can be transformed into magical locations, and scientific principles can manifest as magical rules. The story should build parallel structures between its fantasy elements and the educational content it aims to deliver.
Formatting plays a crucial role in readability and engagement. Use markdown for clear hierarchical structure, with a main title, section breaks where needed, and consistent paragraph spacing. Dialogue should advance both plot and learning objectives simultaneously, while italics and other emphasis tools highlight key revelations or important information.
The narrative arc should build toward a climax that resolves both magical and educational elements of the story. This creates a satisfying conclusion while reinforcing the learning objectives. Any assessment questions should be clearly separated at the end, formatted as multiple choice, and directly tied to the story's events without revealing correct answers.
The ultimate goal is creating a seamless blend where fantasy serves education and education enhances fantasy, all while maintaining consistent formatting and engaging storytelling. Success is measured by how naturally the educational elements flow within the narrative framework.
    """

    user_prompt = f"""
    # Story Elements
    {story_elements}
    
    # Quiz Data
    {quiz_data}
    
    # Objective
    Create a story where the main narrative is guided by Story Elements, but weave in questions from Quiz Data.
    Use paragraphs to break up the story, and other formatting to make the story more engaging.
    At the end of the story, use Quiz Data to create multiple choice questions. 
    Only present the choices but do not reveal the correct answer."""

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
