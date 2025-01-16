#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Return a cached dataset. Load the dataset if it hasn't been loaded yet.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Return a dataset indexed by sorting position, starting at 0.
        The dataset is truncated to the first 1000 entries for efficiency.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: truncated_dataset[i] for i in range(len(truncated_dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Return a dictionary with pagination details, accounting for deletions.
        """
        assert isinstance(index, int) and isinstance(page_size, int), (
            "Index and page size must be integers."
        )
        assert 0 <= index < len(self.indexed_dataset()), (
            "Index out of range."
        )

        next_index = index + page_size
        items = []
        current_index = index

        while len(items) < page_size and current_index < len(self.indexed_dataset()):
            if current_index in self.indexed_dataset():
                items.append(self.indexed_dataset()[current_index])
            else:
                next_index += 1
            current_index += 1

        return {
            'next_index': next_index,
            'index': index,
            'page_size': page_size,
            'data': items,
        }
