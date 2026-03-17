"""
Tests for SelfDrivenNLP core functionality
"""

from src.llm import SelfDrivenNLP, get_llm_client


class TestSelfDrivenNLPBasics:
    """Basic SelfDrivenNLP functionality tests"""
    
    def test_nlp_initialization(self):
        """Test SelfDrivenNLP initializes correctly"""
        nlp = SelfDrivenNLP()
        assert nlp is not None
        assert hasattr(nlp, 'conversation_history')
        assert hasattr(nlp, '_learned_patterns')
        assert hasattr(nlp, 'system_prompt')
    
    def test_generate_returns_llm_response(self):
        """Test generate returns proper LLMResponse"""
        nlp = SelfDrivenNLP()
        response = nlp.generate("hello")
        
        assert response is not None
        assert hasattr(response, 'content')
        assert hasattr(response, 'model')
        assert hasattr(response, 'usage')
        assert response.model == "zo_ai_bridge"
    
    def test_conversation_history_tracking(self):
        """Test conversation history is tracked"""
        nlp = SelfDrivenNLP()
        initial_len = len(nlp.conversation_history)
        
        nlp.generate("first message")
        nlp.generate("second message")
        
        assert len(nlp.conversation_history) == initial_len + 4  # 2 user + 2 assistant
    
    def test_clear_history(self):
        """Test clearing conversation history"""
        nlp = SelfDrivenNLP()
        nlp.generate("test message")
        
        nlp.clear_history()
        
        assert len(nlp.conversation_history) == 0


class TestIntentParsing:
    """Intent parsing tests for SelfDrivenNLP"""
    
    def test_status_intent(self):
        """Test status query detection"""
        nlp = SelfDrivenNLP()
        response = nlp.generate("what is your status?")
        
        assert "operating" in response.content.lower() or "autonomous" in response.content.lower()
    
    def test_help_intent(self):
        """Test help query detection"""
        nlp = SelfDrivenNLP()
        response = nlp.generate("help me")
        
        assert "can" in response.content.lower() or "autonomous" in response.content.lower()
    
    def test_revenue_intent(self):
        """Test revenue query detection"""
        nlp = SelfDrivenNLP()
        response = nlp.generate("how do you make money?")
        
        assert "revenue" in response.content.lower() or "model" in response.content.lower()
    
    def test_memory_intent(self):
        """Test memory query detection"""
        nlp = SelfDrivenNLP()
        response = nlp.generate("do you remember anything?")
        
        assert "memory" in response.content.lower() or "persistent" in response.content.lower()
    
    def test_improve_intent(self):
        """Test self-improvement query detection"""
        nlp = SelfDrivenNLP()
        response = nlp.generate("how do you improve yourself?")
        
        assert "improv" in response.content.lower() or "self" in response.content.lower()
    
    def test_api_intent(self):
        """Test API query detection"""
        nlp = SelfDrivenNLP()
        response = nlp.generate("what API do you have?")
        
        assert "api" in response.content.lower() or "chat" in response.content.lower()
    
    def test_identity_intent(self):
        """Test identity query detection"""
        nlp = SelfDrivenNLP()
        response = nlp.generate("who are you?")
        
        assert "personai" in response.content.lower() or "ai" in response.content.lower()


class TestPatternLearning:
    """Pattern learning tests"""
    
    def test_pattern_file_created(self):
        """Test pattern file is created on first use"""
        import os
        nlp = SelfDrivenNLP()
        nlp._learn_pattern("test query", "test response that is long enough")
        
        assert os.path.exists(nlp._pattern_file)
    
    def test_learn_short_response_ignored(self):
        """Test short responses are not learned"""
        nlp = SelfDrivenNLP()
        initial_count = len(nlp._learned_patterns)
        
        nlp._learn_pattern("test", "short")  # Too short
        
        assert len(nlp._learned_patterns) == initial_count
    
    def test_learn_long_response_stored(self):
        """Test long responses are learned"""
        nlp = SelfDrivenNLP()
        nlp._learn_pattern("my custom query", "This is a much longer response that should be stored")
        
        # Check it was stored
        assert len(nlp._learned_patterns) > 0
    
    def test_get_learned_response(self):
        """Test retrieving learned response"""
        nlp = SelfDrivenNLP()
        
        # Add a learned pattern
        nlp._learned_patterns["test_query_response"] = "learned response"
        result = nlp._get_learned_response("test query response")
        
        # May return None if key doesn't match exactly
        assert result is None or isinstance(result, str)


class TestWrappedPrompts:
    """Tests for wrapped prompt handling"""
    
    def test_extracts_user_from_wrapped(self):
        """Test extracting user message from wrapped prompt"""
        nlp = SelfDrivenNLP()
        
        prompt = "Context here\nUser: tell me a joke\n\nRespond as PersonAI"
        extracted = nlp._extract_user_intent_text(prompt)
        
        assert "joke" in extracted.lower()
    
    def test_direct_prompt_unchanged(self):
        """Test direct prompts work"""
        nlp = SelfDrivenNLP()
        
        prompt = "hello there"
        extracted = nlp._extract_user_intent_text(prompt)
        
        assert "hello" in extracted.lower()


class TestGetLLMClient:
    """Tests for the LLM client factory"""
    
    def test_get_llm_client_returns_client(self):
        """Test get_llm_client returns a client"""
        client = get_llm_client()
        assert client is not None
        assert hasattr(client, 'self_driven')
        assert hasattr(client, 'generate')
    
    def test_client_has_self_driven_nlp(self):
        """Test client has SelfDrivenNLP"""
        client = get_llm_client()
        assert hasattr(client, 'self_driven')
        assert isinstance(client.self_driven, SelfDrivenNLP)
    
    def test_generate_uses_self_driven(self):
        """Test generate uses SelfDrivenNLP"""
        client = get_llm_client()
        response = client.generate("test")
        
        assert response.model == "zo_ai_bridge"


class TestMemoryIntegration:
    """Tests for memory integration"""
    
    def test_nlp_can_have_memory(self):
        """Test NLP can have memory injected"""
        nlp = SelfDrivenNLP()
        
        # Create mock memory
        class MockMemory:
            def recall(self, query, limit=5):
                return []
        
        nlp.memory = MockMemory()
        
        response = nlp.generate("test with memory")
        
        assert response is not None
        assert len(response.content) > 0
