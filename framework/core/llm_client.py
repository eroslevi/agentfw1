"""
LLM Access Module for Azure-hosted OpenAI Models

This module provides a unified interface for accessing Azure-hosted OpenAI LLM models
using URI and API key credentials.
"""

import os
from typing import Optional, List, Dict, Any
from openai import AzureOpenAI


class AzureLLMClient:
    """
    Client for accessing Azure-hosted OpenAI LLM models.
    
    This client manages connections to Azure OpenAI API endpoints and provides
    methods for generating completions and chat responses.
    """
    
    def __init__(
        self,
        azure_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: str = "2024-02-15-preview",
        deployment_name: str = "gpt-4"
    ):
        """
        Initialize the Azure LLM client.
        
        Args:
            azure_endpoint: The Azure OpenAI endpoint URI. If not provided,
                          will use AZURE_OPENAI_ENDPOINT environment variable.
            api_key: The Azure OpenAI API key. If not provided,
                    will use AZURE_OPENAI_API_KEY environment variable.
            api_version: The Azure OpenAI API version to use.
            deployment_name: The name of the deployment to use.
        
        Raises:
            ValueError: If endpoint or API key are not provided and not found in environment.
        """
        self.azure_endpoint = azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = api_version
        self.deployment_name = deployment_name
        
        if not self.azure_endpoint:
            raise ValueError(
                "Azure endpoint must be provided via parameter or AZURE_OPENAI_ENDPOINT environment variable"
            )
        if not self.api_key:
            raise ValueError(
                "Azure API key must be provided via parameter or AZURE_OPENAI_API_KEY environment variable"
            )
        
        self.client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version=self.api_version
        )
    
    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs
    ) -> str:
        """
        Create a chat completion using the Azure OpenAI API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
                     Example: [{"role": "system", "content": "You are helpful..."},
                              {"role": "user", "content": "What is...?"}]
            temperature: Controls randomness. 0 = deterministic, 1 = very random.
            max_tokens: Maximum tokens in the response. If None, uses model default.
            top_p: Controls diversity via nucleus sampling.
            frequency_penalty: Penalizes repeating tokens.
            presence_penalty: Penalizes new tokens.
            **kwargs: Additional parameters to pass to the API.
        
        Returns:
            The text content of the assistant's response.
        
        Raises:
            Exception: If the API call fails.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Failed to create chat completion: {str(e)}")
    
    def create_chat_completion_with_retries(
        self,
        messages: List[Dict[str, str]],
        max_retries: int = 3,
        retry_delay: float = 1.0,
        **kwargs
    ) -> str:
        """
        Create a chat completion with automatic retries on failure.
        
        Args:
            messages: List of message dictionaries.
            max_retries: Maximum number of retry attempts.
            retry_delay: Delay between retries in seconds.
            **kwargs: Additional parameters for create_chat_completion.
        
        Returns:
            The text content of the assistant's response.
        
        Raises:
            Exception: If all retry attempts fail.
        """
        import time
        
        for attempt in range(max_retries):
            try:
                return self.create_chat_completion(messages, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(retry_delay)
                continue
    
    def generate_from_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> str:
        """
        Generate text from system and user prompts.
        
        Args:
            system_prompt: The system prompt that sets context/behavior.
            user_prompt: The user's prompt/query.
            **kwargs: Additional parameters for create_chat_completion.
        
        Returns:
            The generated text response.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self.create_chat_completion(messages, **kwargs)
    
    def generate_specification(
        self,
        template: str,
        context: str,
        spec_type: str = "specification",
        **kwargs
    ) -> str:
        """
        Generate a specification document using the LLM.
        
        This is a convenience method for generating various types of specifications
        (architectural, technical, test, etc.) using templates and context.
        
        Args:
            template: The specification template to use.
            context: The context/requirements for generation.
            spec_type: The type of specification being generated.
            **kwargs: Additional parameters for create_chat_completion.
        
        Returns:
            The generated specification in Markdown format.
        """
        system_prompt = f"""You are an expert software architect and technical writer.
Your task is to generate a detailed {spec_type} document in Markdown format.
Use the provided template structure and context to create a comprehensive, 
well-organized document suitable for software development teams."""
        
        user_prompt = f"""Generate a {spec_type} using the following:

## Template Structure:
{template}

## Context and Requirements:
{context}

Please generate a complete {spec_type} document following the template structure
and incorporating the context provided. Ensure all sections are filled with specific,
actionable information."""
        
        return self.generate_from_prompt(system_prompt, user_prompt, **kwargs)


def get_llm_client(
    azure_endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs
) -> AzureLLMClient:
    """
    Factory function to create an AzureLLMClient instance.
    
    Args:
        azure_endpoint: Azure OpenAI endpoint URI.
        api_key: Azure OpenAI API key.
        **kwargs: Additional parameters for AzureLLMClient.
    
    Returns:
        An initialized AzureLLMClient instance.
    """
    return AzureLLMClient(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        **kwargs
    )
