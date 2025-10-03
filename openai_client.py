"""OpenAI-compatible API client."""
from openai import OpenAI
from typing import Dict, Any, List, Optional

class OpenAIClient:
    def __init__(self, api_key: str, base_url: str, model: str = "gpt-3.5-turbo"):
        # Store the API key even if it's a placeholder
        # This allows the bot to start and be configured via web interface
        self.api_key = api_key or "none"
        self.model = model
        
        # Only create the client if we have a valid API key
        # Otherwise, defer client creation until a valid key is provided
        if self.api_key and self.api_key not in ["YOUR_API_KEY", "", "none"]:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        else:
            # Create a dummy client - will be replaced when config is updated
            self.client = OpenAI(
                api_key="none",  # Placeholder to prevent errors
                base_url=base_url
            )
    
    def update_config(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        """Update client configuration."""
        if api_key:
            # Validate API key is not a placeholder
            if api_key in ["YOUR_API_KEY", "", "none"]:
                raise ValueError(
                    "API key is not configured. Please set a valid API key in the configuration."
                )
            self.client.api_key = api_key
            self.api_key = api_key
        if base_url:
            self.client.base_url = base_url
        if model:
            self.model = model
    
    def list_models(self) -> List[str]:
        """
        Fetch available models from the OpenAI-compatible API.
        
        Returns:
            List of available model names
        """
        # Check if API key is configured
        if not self.api_key or self.api_key in ["YOUR_API_KEY", "", "none"]:
            raise ValueError(
                "API key is not configured. Please set a valid API key in the configuration."
            )
        
        try:
            models_response = self.client.models.list()
            return [model.id for model in models_response.data]
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid_api_key" in error_msg:
                raise Exception(
                    f"API authentication failed. Please verify your API key is correct. "
                    f"Original error: {error_msg}"
                )
            raise Exception(f"Error fetching models from API: {error_msg}")
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        frequency_penalty_enabled: bool = True,
        presence_penalty_enabled: bool = True
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
            frequency_penalty_enabled: Whether to include frequency penalty in request
            presence_penalty_enabled: Whether to include presence penalty in request
        
        Returns:
            Generated text response
        """
        # Check if API key is configured
        if not self.api_key or self.api_key in ["YOUR_API_KEY", "", "none"]:
            raise ValueError(
                "API key is not configured. Please set a valid API key in the configuration. "
                "You can configure it via the web interface at http://localhost:5000 or by editing config.json"
            )
        
        try:
            # Build request parameters
            request_params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }
            
            # Only include penalties if they are enabled
            if frequency_penalty_enabled:
                request_params["frequency_penalty"] = frequency_penalty
            if presence_penalty_enabled:
                request_params["presence_penalty"] = presence_penalty
            
            response = self.client.chat.completions.create(**request_params)
            
            return response.choices[0].message.content
        except Exception as e:
            # Provide more helpful error message for API key issues
            error_msg = str(e)
            if "401" in error_msg or "invalid_api_key" in error_msg or "Incorrect API key" in error_msg:
                raise Exception(
                    f"API authentication failed. Please verify your API key is correct. "
                    f"You can update it via the web interface at http://localhost:5000. "
                    f"Original error: {error_msg}"
                )
            raise Exception(f"Error calling OpenAI-compatible API: {error_msg}")
