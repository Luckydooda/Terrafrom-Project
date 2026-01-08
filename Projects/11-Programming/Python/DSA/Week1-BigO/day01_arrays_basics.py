# Big-O Practice: Analyze Time Complexity
# Day 1 - Arrays Basics

"""
INSTRUCTIONS:
For each function below:
1. Write what you think the time complexity is
2. Explain WHY in one sentence
3. Run the code to verify it works

Example:
def example(arr):
    return arr[0]
# Time: O(1) - Direct array access, doesn't depend on input size
"""

# ==================================================
# PROBLEM 1: Contains Duplicate
# ==================================================

"""
Given an array of integers, return True if any value appears at least twice.

Example:
    Input: [1, 2, 3, 1]
    Output: True
    
    Input: [1, 2, 3, 4]
    Output: False
"""

def contains_duplicate(nums):
    """
    TODO: Implement this function
    
    Your solution here:
    """
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Your complexity analysis:
# Time: O(n) - Why?-we loop through array once
# Space: O(n) - Why?-we store numbers in set


# ==================================================
# PROBLEM 2: Find Maximum in Array
# ==================================================

"""
Find the maximum value in an array of integers.

Example:
    Input: [3, 7, 2, 9, 1]
    Output: 9
"""

def find_max(nums):
    """
    TODO: Implement this function
    
    Your solution here:
    """
    max_num = nums[0]
    for num in nums:
        if num > max_num:
            max_num = num
    return max_num

# Your complexity analysis:
# Time: O(n) - Why?-we loop through array once
# Space: O(1) - Why?-we store maximum number


# ==================================================
# PROBLEM 3: Find Minimum in Array
# ==================================================

"""
Find the minimum value in an array of integers.

Example:
    Input: [3, 7, 2, 9, 1]
    Output: 1
"""

def find_min(nums):
    """
    TODO: Implement this function
    
    Your solution here:
    """
    min_num = nums[0]
    for num in nums:
        if num < min_num:
            min_num = num
    return min_num

# Your complexity analysis:
# Time: O(n) - Why?-we loop through array once
# Space: O(1) - Why?-we store minimum number


# ==================================================
# TEST CASES
# ==================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Your Solutions")
    print("=" * 50)
    
    # Test 1: Contains Duplicate
    print("\nTest 1: Contains Duplicate")
    print(f"Input: [1, 2, 3, 1]")
    print(f"Your output: {contains_duplicate([1, 2, 3, 1])}")
    print(f"Expected: True")
    
    print(f"\nInput: [1, 2, 3, 4]")
    print(f"Your output: {contains_duplicate([1, 2, 3, 4])}")
    print(f"Expected: False")
    
    # Test 2: Find Max
    print("\n" + "=" * 50)
    print("Test 2: Find Maximum")
    print(f"Input: [3, 7, 2, 9, 1]")
    print(f"Your output: {find_max([3, 7, 2, 9, 1])}")
    print(f"Expected: 9")
    
    # Test 3: Find Min
    print("\n" + "=" * 50)
    print("Test 3: Find Minimum")
    print(f"Input: [3, 7, 2, 9, 1]")
    print(f"Your output: {find_min([3, 7, 2, 9, 1])}")
    print(f"Expected: 1")
    
    print("\n" + "=" * 50)
    print("Done! Now analyze your complexity:")
    print("- Ask yourself: How many times do we loop?")
    print("- Does the runtime grow with input size?")
    print("=" * 50)
