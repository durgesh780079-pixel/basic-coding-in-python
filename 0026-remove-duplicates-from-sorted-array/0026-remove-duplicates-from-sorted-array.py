class Solution:
    def removeDuplicates(self, nums):
        if len(nums) == 0:
            return 0

        idx = 1

        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                nums[idx] = nums[i]
                idx += 1

        return idx