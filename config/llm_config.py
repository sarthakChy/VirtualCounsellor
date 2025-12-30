import os
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional


class LLMManager:
    """Centralized LLM management for the entire project"""

    _instance = None
    _llm_model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMManager, cls).__new__(cls)
        return cls._instance

    def initialize_gemini(
        self,
        model_name: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
    ) -> ChatGoogleGenerativeAI:
        """Initialize Gemini model as the project's LLM"""

        if self._llm_model is None:
            # Get API key from parameter or environment
            gemini_api_key = api_key or os.getenv("GOOGLE_API_KEY")

            if not gemini_api_key:
                raise ValueError(
                    "Google API key not found. Set GOOGLE_API_KEY environment variable or pass api_key parameter"
                )

            self._llm_model = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=gemini_api_key,
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            print(f"Initialized Gemini model: {model_name}")

        return self._llm_model

    def get_llm(self) -> ChatGoogleGenerativeAI:
        """Get the initialized LLM instance"""
        if self._llm_model is None:
            return self.initialize_gemini()
        return self._llm_model

    def reset(self):
        """Reset LLM instance (useful for testing)"""
        self._llm_model = None


# Global instance
llm_manager = LLMManager()
