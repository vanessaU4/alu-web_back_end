#!/usr/bin/env python3
"""Simple pagination"""

import csv
import math
from typing import List, Dict


def index_range(page: int, page_size: int) -> tuple:
    """
    Return a tuple of size two containing a start index and an
    end index corresponding to the range of indexes to return
    in a list for those particular pagination parameters.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

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

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get the data for a specific page.
        """
        assert isinstance(page, int) and page > 0, (
            "Page must be a positive integer."
        )
        assert isinstance(page_size, int) and page_size > 0, (
            "Page size must be a positive integer."
        )

        start, end = index_range(page, page_size)
        data = self.dataset()

        if start >= len(data):
            return []

        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Get page with hypermedia pagination.
        """
        data = self.dataset()
        page_items = self.get_page(page=page, page_size=page_size)
        total_pages = math.ceil(len(data) / page_size)

        next_page = page + 1 if page + 1 <= total_pages else None
        prev_page = page - 1 if page > 1 else None

        hyper = {
            'page_size': len(page_items),
            'page': page,
            'data': page_items,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages,
        }
        return hyper
