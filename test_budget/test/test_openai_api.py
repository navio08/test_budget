import pytest
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_budget.main import LOGS_PATH, get_date_time_str, log_message, read_prompt
from test_budget.tools.tools import create_openai_request

# Test data with various parameter combinations
@pytest.mark.parametrize(
    "prompt,model,developer_prompt,reasoning_effort,temperature",
    [
        ("Allocate $25000 for a wedding", "gpt-3.5-turbo", "You are a wedding budget expert", "low", 1),
        ("Create a budget for $30000 wedding", "gpt-4", "Provide detailed budget allocation", "medium", 0.7),
        ("Budget planning for $20000", "gpt-3.5-turbo", "Focus on essential items", "minimal", 0.5),
        ("Luxury wedding budget $50000", "gpt-4", "High-end wedding planner", "high", 1.2),
        ("Simple ceremony $15000", "gpt-3.5-turbo", "", "low", 0.9),
    ]
)
def test_tool_actual_calls(prompt, model, developer_prompt, reasoning_effort, temperature):
    """Test the tool object with actual API calls using various parameters."""
    # Use MockOpenAI for testing (no API key) - this calls the actual tool implementation
    tool = create_openai_request(tool="response", api_key=None)
    
    # Call the tool with actual implementation
    response = tool(
        prompt=prompt,
        model=model,
        developer_prompt=developer_prompt,
        reasoning_effort=reasoning_effort,
        temperature=temperature
    )
    
    # Assertions on the actual response
    assert response is not None
    assert isinstance(response, str)
    
    # Test the output method
    formatted_output = tool.output(response)
    assert isinstance(formatted_output, str)
    assert "=" in formatted_output  # Should contain separator lines
    
    # Verify the response contains expected wedding budget categories
    assert "WEDDING_SUBCATEGORY" in response

@pytest.mark.parametrize(
    "prompt_file_path,model,developer_prompt_file_path,reasoning_effort,temperature",
    [
        ("test_budget/prompts/prompt_02_user_low_budget.txt", "gpt-5", "test_budget/prompts/prompt_02_developer.txt", "low", 1),
    ]
)
def test_tool_with_real_api(prompt_file_path, model, developer_prompt_file_path, reasoning_effort, temperature):
    """Test the tool with real OpenAI API calls (requires API key)."""
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv('OPENAI_API_KEY')
    tool = create_openai_request(tool="response", api_key=api_key)
    prompt = read_prompt(filename=prompt_file_path)
    developer_prompt = read_prompt(filename=developer_prompt_file_path)
    # make sure that the api key is being loaded
    assert api_key is not None
    response = tool(
        prompt=prompt, 
        model=model, 
        developer_prompt=developer_prompt, 
        reasoning_effort=reasoning_effort, 
        temperature=temperature,
    )
    kwargs = {
            "prompt": prompt_file_path,
            "developer_prompt": developer_prompt_file_path,
            "model": model,
            "reasoning_effort": reasoning_effort,
            "temperature": temperature
        }
    message = tool.output(response, **kwargs)
    logfilename = ["response", os.path.splitext(os.path.basename(prompt_file_path))[0], get_date_time_str()]
    log_message(message=message, log_file=os.path.join(os.path.join(LOGS_PATH, "tests"), "_".join(logfilename) + ".txt") )
    
    """# Verify response structure
    assert response is not None
    assert hasattr(response, 'output_text')
    assert hasattr(response, 'usage')
        
    # Test output formatting
    formatted_output = tool.output(response, debug=True)
    assert isinstance(formatted_output, str)
    assert "Tokens utilizados" in formatted_output
    assert "Prompt:" in formatted_output
    assert "Completion:" in formatted_output"""


def test_tool_invalid_parameters():
    """Test tool validation with invalid parameters."""
    tool = create_openai_request(tool="response", api_key="random_key")
    
    # Test invalid reasoning_effort
    with pytest.raises(ValueError, match="Invalid reasoning_effort value"):
        tool(
            prompt="test",
            model="gpt-3.5-turbo",
            developer_prompt="test",
            reasoning_effort="invalid_effort",
            temperature=1
        )
    
    # Test invalid temperature (too high)
    with pytest.raises(ValueError, match="Invalid temperature value"):
        tool(
            prompt="test",
            model="gpt-3.5-turbo",
            developer_prompt="test", 
            reasoning_effort="low",
            temperature=3
        )
    
    # Test invalid temperature (negative)
    with pytest.raises(ValueError, match="Invalid temperature value"):
        tool(
            prompt="test",
            model="gpt-3.5-turbo",
            developer_prompt="test",
            reasoning_effort="low",
            temperature=-1
        )