two sum :
[2,7,11,15] target = 9
{}
loop: 
2
9-2 = 7
if 7 in {} : return index of 7 and 2
add 2 to {} with index as value


buy and sell stock

price = [7,1,5,3,6,4]
output = 5

b, s = 0,1
max_profit = 0
while s < len(price):
    if price[b]<price[s]:
        p = price[s]-price[b]
        max_profit = max(max_profit,p)
    else:    
        b = s
    s += 1
    
 return max_profit
 
 
contains duplicate:
length of set of array compared with length of normal array
if true means no duplicate
else false

product of array except self:
nums = [1,2,3,4] output = [24,12,8,6]
prefix_product = start multiply from 1st array and store it in new array
i.e. = [1,2,6,24]
prosfix_product = product of array from last and store the values in new array
i.e = [24,24,12,4]
then take the product of before index from prefix and after index from postfix
eg - 3 index : 2*4 = 8
for all = [24,12,8,6]

or 

take an array of same length as of nums[]
res = [1]*len(nums)

take a prefix =1 and start before 1st array
prefix = 1

loop through the len(nums)
1st store the prefix value to the 1st index of res[] (as for the 1st index we dont need  to multiple the 1st index value so we keep it as 1) 
and then multiple the prefix with the 1st element of nums[]

now take a postfix =1 and start from last of array
postfix = 1
loop through the len(nums)
1st multiple the postfix value to the last index of res[] (as for the last index we dont need  to multiple the last index value so we multiple it with 1) 
and then multiple the postfix with the last element of nums[]
return res
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1]*(len(nums))
        prefix = 1
        for i in range(len(nums)):
            res[i] = prefix
            prefix *=nums[i]
        postfix = 1
        for i in range(len(nums)-1,-1,-1):
            res[i] *=postfix
            postfix *=nums[i]
        return res



    def maxSubArray(self, nums: list[int]) -> int:
        cur = curMax = nums[0]

        for num in nums[1:]:
            cur = max(num, cur + num)
            curMax = max(curMax, cur)
        
        return curMax
