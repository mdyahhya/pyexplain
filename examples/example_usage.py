"""
PyExplain Basic Usage Examples

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import pyexplain


def example_1_decode_traceback():
    """Example 1: Decode a raw traceback string."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Decoding a Traceback String")
    print("="*70)
    
    traceback_text = """Traceback (most recent call last):
  File "calculator.py", line 15, in calculate
    result = numerator / denominator
ZeroDivisionError: division by zero"""
    
    result = pyexplain.decode_traceback(traceback_text)
    
    print(f"\n🔴 Error Type: {result['error_type']}")
    print(f"📝 Original Message: {result['original_message']}")
    print(f"\n💡 Simple Explanation:\n{result['simple_explanation']}")
    print(f"\n🔧 Fix Suggestion:\n{result['fix_suggestion']}")
    print(f"\n📍 Location: Line {result['line_number']} in {result['file_name']}")
    print(f"\n{result['branding']}")


def example_2_decode_exception():
    """Example 2: Decode an exception object directly."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Decoding an Exception Object")
    print("="*70)
    
    try:
        number = int("not_a_number")
    except Exception as e:
        result = pyexplain.decode_exception(e)
        
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
    
    result = pyexplain.safe_run(code)
    
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
print(my_list[10])
"""
    
    result = pyexplain.safe_run(code)
    
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
        data = {"name": "Alice", "age": 30}
        print(data["email"])
    except Exception as e:
        result = pyexplain.decode_exception(e)
        formatted = pyexplain.format_decoded_output(result, include_technical=True, color=False)
        print(formatted)


def example_6_version_info():
    """Example 6: Get version information."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Version Information")
    print("="*70)
    
    print(f"\nVersion: {pyexplain.__version__}")
    print(f"Author: {pyexplain.__author__}")
    print(f"Company: {pyexplain.__company__}")
    print(f"License: {pyexplain.__license__}")


def main():
    """Run all examples."""
    print("\n" + "🌟"*35)
    print("   PyExplain - Complete Usage Examples")
    print("🌟"*35)
    
    examples = [
        example_1_decode_traceback,
        example_2_decode_exception,
        example_3_safe_run_success,
        example_4_safe_run_with_error,
        example_5_formatted_output,
        example_6_version_info
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
