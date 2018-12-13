class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        result = []
        tempList = []
        
        for index, value in enumerate(nums):
            if (len(tempList) == 0):
                tempList.append(target-value)
            else:
                try:
                    targetIndex = tempList.index(value)
                    result = [targetIndex, index]
                    break
                except ValueError:
                    tempList.append(target-value)
                    
                    
        print("Temp List {0}".format(tempList))
                    
        return result
        
print("Hello World")

nums = [2,7,11,15]
target = 26

result = Solution().twoSum(nums, target)
print(result)
