def insertion_sort(nums):
    # assume the first element is sorted
    for i in range(1, len(nums)):
        item_to_insert = nums[i]
        # keep the index of the previous element
        j = i - 1
        # move all preceding items forward if the item to insert is smaller
        while j >= 0 and nums[j] > item_to_insert:
            nums[j + 1] = nums[j]
            j -= 1
        # insert the item
        nums[j + 1] = item_to_insert
