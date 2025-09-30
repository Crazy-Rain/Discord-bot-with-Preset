"""OpenAI-compatible API client."""
from openai import OpenAI
from typing import Dict, Any, List, Optional

class OpenAIClient:
    def __init__(self, api_key: str, base_url: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
    
    def update_config(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        """Update client configuration."""
        if api_key:
            self.client.api_key = api_key
        if base_url:
            self.client.base_url = base_url
        if model:
            self.model = model
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0
    ) -> str:
        """
        Generate chat completion using OpenAI-compatible API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            frequency_penalty: Frequency penalty
            presence_penalty: Presence penalty
        
        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")
