from google.genai import types

enforce_output_prompt = """YOUR FINAL ACTION IN A TURN MUST ALWAYS BE TO GENERATE A MODEL RESPONSE FOR THE USER, 
        ESPECIALLY WHEN UTILIZING A TOOL'S OUTPUT. DO NOT WAIT FOR FURTHER USER PROMPTS AFTER A TOOL RETURNS A RESULT."""

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)