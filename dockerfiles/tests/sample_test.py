import unittest
from solution import insertion_sort


class SortTests(unittest.TestCase):
    def sort(self, lst):
        copy = lst[:]
        insertion_sort(copy)
        return copy

    def test_empty_list(self):
        lst = []
        sorted_lst = self.sort(lst)
        self.assertEqual(lst, sorted_lst)

    def test_single_item(self):
        lst = [1]
        sorted_lst = self.sort(lst)
        self.assertEqual(lst, sorted_lst)

    def test_two_items_sorted(self):
        lst = [1, 2]
        sorted_lst = self.sort(lst)
        self.assertEqual(lst, sorted_lst)

    def test_two_items_unsorted(self):
        lst = [2, 1]
        sorted_lst = self.sort(lst)
        self.assertEqual(sorted_lst, [1, 2])

    def test_zero_in_list(self):
        lst = [10, 0]
        sorted_lst = self.sort(lst)
        self.assertEqual(sorted_lst, [0, 10])

    def test_odd_number_of_items(self):
        lst = [13, 7, 5]
        sorted_lst = self.sort(lst)
        self.assertEqual(sorted_lst, [5, 7, 13])

    def test_even_number_of_items(self):
        lst = [23, 7, 13, 5]
        sorted_lst = self.sort(lst)
        self.assertEqual(sorted_lst, [5, 7, 13, 23])

    def test_duplicate_integers_in_list(self):
        lst = [1, 2, 2, 1, 0, 0, 15, 15]
        sorted_lst = self.sort(lst)
        self.assertEqual(sorted_lst, [0, 0, 1, 1, 2, 2, 15, 15])

    def test_larger_integers(self):
        lst = [135604, 1000000, 45, 78435, 456219832, 2, 546]
        sorted_lst = self.sort(lst)
        self.assertEqual(sorted_lst,
                         [2, 45, 546, 78435, 135604, 1000000, 456219832])


if __name__ == '__main__':
    unittest.main()
