
import openai
import json
import sys

def run_code_migration_and_tests(json_file_path, source_lang, target_lang, api_key):
    # Load the JSON file
    with open(json_file_path, 'r') as file:
        code_snippets = json.load(file)

    # Set the OpenAI API key
    openai.api_key = api_key

    # Initialize statistics
    total_snippets = len(code_snippets)
    passed_tests = 0

    # Iterate through each code snippet
    for snippet in code_snippets:
        # Build the code migration prompt
        prompt = f"Translate this {source_lang} code to {target_lang}:\n\n{snippet['code']}"

        # Use ChatGPT for code migration
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or use "text-davinci-004" or other suitable engine
            prompt=prompt,
            max_tokens=150
        )
        migrated_code = response.choices[0].text.strip()

        # Run test cases
        for test_case in snippet['test_cases']:
            # Build the test case prompt
            test_prompt = f"Run this test case on the following {target_lang} code:\nCode:\n{migrated_code}\nTest Case:\n{test_case['input']}\nExpected Output:\n{test_case['expected_output']}"

            # Use ChatGPT to run the test case
            test_response = openai.Completion.create(
                engine="text-davinci-003",  # Or use "text-davinci-004" or other suitable engine
                prompt=test_prompt,
                max_tokens=150
            )
            test_result = test_response.choices[0].text.strip()

            # Check the test result
            if test_result == test_case['expected_output']:
                passed_tests += 1

    # Calculate pass rate
    pass_rate = passed_tests / total_snippets
    print(f"Code Migration Pass Rate: {pass_rate * 100:.2f}%")

if __name__ == "__main__":
    json_file_path = sys.argv[1]  # Path to the JSON file
    source_lang = sys.argv[2]    # Source language
    target_lang = sys.argv[3]    # Target language
    api_key = sys.argv[4]        # OpenAI API key

    run_code_migration_and_tests(json_file_path, source_lang, target_lang, api_key)
