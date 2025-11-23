"""
pyDecode Basic Usage Examples

This script demonstrates all the main features of pyDecode with practical examples.

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import pydecode


def example_1_decode_traceback():
    """Example 1: Decode a raw traceback string."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Decoding a Traceback String")
    print("="*70)
    
    # Simulate a traceback string
    traceback_text = """Traceback (most recent call last):
  File "calculator.py", line 15, in calculate
    result = numerator / denominator
ZeroDivisionError: division by zero"""
    
    # Decode the traceback
    result = pydecode.decode_traceback(traceback_text)
    
    # Display the results
    print(f"\n🔴 Error Type: {result['error_type']}")
    print(f"📝 Original Message: {result['original_message']}")
    print(f"\n💡 Simple Explanation:\n{result['simple_explanation']}")
    print(f"\n🔧 Fix Suggestion:\n{result['fix_suggestion']}")
    print(f"\n📍 Location: Line {result['line_number']} in {result['file_name']}")
    print(f"🏷️  Tags: {', '.join(result['tags'])}")
    print(f"📂 Category: {result['category']}")
    print(f"\n{result['branding']}")


def example_2_decode_exception():
    """Example 2: Decode an exception object directly."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Decoding an Exception Object")
    print("="*70)
    
    try:
        # This will raise a ValueError
        number = int("not_a_number")
    except Exception as e:
        # Decode the exception
        result = pydecode.decode_exception(e)
        
        print(f"\n{result['emoji']} Error: {result['error_type']}")
        print(f"\n💡 What happened?\n{result['simple_explanation']}")
        print(f"\n🔧 How to fix:\n{result['fix_suggestion']}")
        print(f"\n{result['branding']}")


def example_3_safe_run_success():
    """Example 3: Run code safely (successful execution)."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Safe Run - Successful Execution")
    print("="*70)
    
    code = """
x = 10
y = 5
result = x + y
print(f"The sum of {x} and {y} is {result}")
"""
    
    result = pydecode.safe_run(code)
    
    if result['success']:
        print("\n✅ Code executed successfully!")
        print(f"\n📤 Output:\n{result['output']}")
        print(f"\n{result['branding']}")


def example_4_safe_run_with_error():
    """Example 4: Run code safely (with error)."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Safe Run - Error Handling")
    print("="*70)
    
    code = """
my_list = [1, 2, 3, 4, 5]
print("List contents:", my_list)
print("Accessing index 10...")
print(my_list[10])  # This will cause IndexError
"""
    
    result = pydecode.safe_run(code)
    
    if not result['success']:
        print(f"\n❌ Error occurred: {result['error_type']}")
        print(f"\n📤 Output before error:\n{result['output']}")
        print(f"\n💡 Explanation:\n{result['simple_explanation']}")
        print(f"\n🔧 Solution:\n{result['fix_suggestion']}")
        print(f"\n{result['branding']}")


def example_5_formatted_output():
    """Example 5: Use formatted output for pretty printing."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Formatted Output")
    print("="*70)
    
    try:
        # Intentional error
        data = {"name": "Alice", "age": 30}
        print(data["email"])  # KeyError
    except Exception as e:
        result = pydecode.decode_exception(e)
        
        # Format with colors and technical details
        formatted = pydecode.format_decoded_output(
            result,
            include_technical=True,
            color=False  # Set to True if terminal supports colors
        )
        
        print(formatted)


def example_6_multiple_errors():
    """Example 6: Handle multiple different error types."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Multiple Error Types")
    print("="*70)
    
    errors_to_test = [
        ("x = 10 / 0", "ZeroDivisionError"),
        ("print(undefined_variable)", "NameError"),
        ("'string' + 5", "TypeError"),
        ("[1, 2, 3][100]", "IndexError"),
        ("{'a': 1}['b']", "KeyError"),
    ]
    
    for code, expected_error in errors_to_test:
        result = pydecode.safe_run(code)
        if not result['success']:
            print(f"\n📝 Code: {code}")
            print(f"🔴 Error: {result['error_type']} {result['emoji']}")
            print(f"💬 {result['simple_explanation'][:80]}...")


def example_7_using_decode_shortcut():
    """Example 7: Use the convenient decode() function."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Using decode() Shortcut")
    print("="*70)
    
    # Works with both strings and exception objects
    traceback_str = "NameError: name 'x' is not defined"
    result1 = pydecode.decode(traceback_str)
    print(f"\nFrom string: {result1['error_type']}")
    
    try:
        x = [1, 2, 3]
        print(x[10])
    except Exception as e:
        result2 = pydecode.decode(e)
        print(f"From exception: {result2['error_type']}")
        print(f"Explanation: {result2['simple_explanation'][:100]}...")


def example_8_extract_utilities():
    """Example 8: Use utility functions for custom processing."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Utility Functions")
    print("="*70)
    
    traceback_text = """Traceback (most recent call last):
  File "app.py", line 42, in process_data
    value = int(user_input)
ValueError: invalid literal for int() with base 10: 'abc'"""
    
    # Extract specific information
    error_type = pydecode.extract_error_type(traceback_text)
    error_msg = pydecode.extract_error_message(traceback_text)
    line_num = pydecode.extract_line_number(traceback_text)
    file_name = pydecode.extract_file_name(traceback_text)
    func_name = pydecode.extract_function_name(traceback_text)
    category = pydecode.categorize_error(error_type)
    
    print(f"\n📊 Extracted Information:")
    print(f"   Error Type: {error_type}")
    print(f"   Message: {error_msg}")
    print(f"   Line: {line_num}")
    print(f"   File: {file_name}")
    print(f"   Function: {func_name}")
    print(f"   Category: {category}")


def example_9_without_branding():
    """Example 9: Decode without branding footer."""
    print("\n" + "="*70)
    print("EXAMPLE 9: Without Branding")
    print("="*70)
    
    code = "x = 10 / 0"
    result = pydecode.safe_run(code, add_branding=False)
    
    if not result['success']:
        print(f"\nError: {result['error_type']}")
        print(f"Explanation: {result['simple_explanation']}")
        print(f"Branding: {result['branding']}")  # Will be None


def example_10_version_info():
    """Example 10: Get version information."""
    print("\n" + "="*70)
    print("EXAMPLE 10: Version Information")
    print("="*70)
    
    print(f"\nVersion: {pydecode.__version__}")
    print(f"Author: {pydecode.__author__}")
    print(f"Company: {pydecode.__company__}")
    print(f"License: {pydecode.__license__}")
    
    # Print full version info
    print("\n" + "-"*70)
    pydecode.print_version_info()


def main():
    """Run all examples."""
    print("\n" + "🌟"*35)
    print("   pyDecode - Complete Usage Examples")
    print("🌟"*35)
    
    examples = [
        example_1_decode_traceback,
        example_2_decode_exception,
        example_3_safe_run_success,
        example_4_safe_run_with_error,
        example_5_formatted_output,
        example_6_multiple_errors,
        example_7_using_decode_shortcut,
        example_8_extract_utilities,
        example_9_without_branding,
        example_10_version_info
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n⚠️  Example failed: {e}")
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
