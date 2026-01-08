# DSA Day 2: Reinforcement Practice
# Topics: Arrays, Counter, HashMap patterns

"""
PROBLEM 1: Frequency Counter - Top K Frequent Elements
=======================================================

Given an array of integers, return the K most frequent elements.

Examples:
    Input: nums = [1, 1, 1, 2, 2, 3], k = 2
    Output: [1, 2]  (1 appears 3x, 2 appears 2x)
    
    Input: nums = [7, 7, 7, 8, 8, 9, 9, 9, 9], k = 2
    Output: [9, 7]  (9 appears 4x, 7 appears 3x)

HINTS:
- Use Counter to count frequencies
- Use most_common(k) to get top k
- Return just the elements, not counts

Time Complexity Goal: O(n log k)
"""

from collections import Counter

def top_k_frequent(nums, k):
    """
    Return the k most frequent elements in nums.
    
    TODO: Implement this function
    """
    count = Counter(nums)
    return [x[0] for x in count.most_common(k)]


# ==================================================
# PROBLEM 2: Two Sum (Using HashMap)
# ==================================================

"""
Given an array of integers and a target sum, return the INDICES 
of the two numbers that add up to the target.

Examples:
    Input: nums = [2, 7, 11, 15], target = 9
    Output: [0, 1]  (nums[0] + nums[1] = 2 + 7 = 9)
    
    Input: nums = [3, 2, 4], target = 6
    Output: [1, 2]  (nums[1] + nums[2] = 2 + 4 = 6)
    
    Input: nums = [3, 3], target = 6
    Output: [0, 1]  (nums[0] + nums[1] = 3 + 3 = 6)

HINTS:
- Use a dict to store {number: index}
- For each number, check if (target - number) exists in dict
- This is O(n) instead of O(n²)!

SRE Connection: Like finding matching request-ID pairs in logs!
"""

def two_sum(nums, target):
    """
    Return indices of two numbers that add up to target.
    
    TODO: Implement this function
    """
    dict_values = {}
    for i,num in enumerate(nums):
        diff = target - num
        if diff in dict_values:
            return [dict_values[diff],i]
        dict_values[num] = i    
    return []
   


# ==================================================
# TEST CASES
# ==================================================

if __name__ == "__main__":
    print("=" * 50)
    print("DSA Day 2: Reinforcement Practice")
    print("=" * 50)
    
    # Test Problem 1: Top K Frequent
    print("\n📊 Problem 1: Top K Frequent Elements")
    print("-" * 40)
    
    test1_1 = top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    print(f"Input: [1,1,1,2,2,3], k=2")
    print(f"Your output: {test1_1}")
    print(f"Expected: [1, 2] (order may vary)")
    
    test1_2 = top_k_frequent([7, 7, 7, 8, 8, 9, 9, 9, 9], 2)
    print(f"\nInput: [7,7,7,8,8,9,9,9,9], k=2")
    print(f"Your output: {test1_2}")
    print(f"Expected: [9, 7] (order may vary)")
    
    # Test Problem 2: Two Sum
    print("\n" + "=" * 50)
    print("📊 Problem 2: Two Sum (HashMap)")
    print("-" * 40)
    
    test2_1 = two_sum([2, 7, 11, 15], 9)
    print(f"Input: [2,7,11,15], target=9")
    print(f"Your output: {test2_1}")
    print(f"Expected: [0, 1]")
    
    test2_2 = two_sum([3, 2, 4], 6)
    print(f"\nInput: [3,2,4], target=6")
    print(f"Your output: {test2_2}")
    print(f"Expected: [1, 2]")
    
    test2_3 = two_sum([3, 3], 6)
    print(f"\nInput: [3,3], target=6")
    print(f"Your output: {test2_3}")
    print(f"Expected: [0, 1]")
    
    print("\n" + "=" * 50)
    print("Complexity Analysis:")
    print("-" * 40)
    print("Problem 1: O(n) to count + O(k log n) to get top k")
    print("Problem 2: O(n) single pass with HashMap lookup O(1)")
    print("=" * 50)
