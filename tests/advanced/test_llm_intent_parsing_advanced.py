from src.llm import SelfDrivenNLP


def test_wrapped_prompt_uses_latest_user_message_for_intent():
    nlp = SelfDrivenNLP()
    prompt = (
        "Current priorities:\n"
        "- item one\n\n"
        "User: tell me a joke\n\n"
        "Respond as PersonAI, be concise and helpful."
    )

    response = nlp.generate(prompt)

    assert "I understand: 'tell me a joke'" in response.content
    assert "I can:" not in response.content


def test_direct_help_prompt_still_returns_help_response():
    """Test that help queries return appropriate help response"""
    nlp = SelfDrivenNLP()
    response = nlp.generate("help")
    
    # Should return help information - now includes Real-Mode messaging
    assert "Self-Driven" in response.content or "native" in response.content.lower() or "autonomous" in response.content.lower()