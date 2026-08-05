class Solution(object):
    def rotate(self, nums, k):
     
  
        n = len(nums)
        k = k % n

        nums.reverse()

        left = 0
        right = k - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

        left = k
        right = n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1