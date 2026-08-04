class Solution:
    def moveZeroes(self, nums):
        idx = 0

        for i in range(len(nums)):
            if nums[i] != 0:
                nums[idx], nums[i] = nums[i], nums[idx]
                idx += 1