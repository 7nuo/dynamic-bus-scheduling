#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2016 Eleftherios Anagnostopoulos for Ericsson AB (EU FP7 CityPulse Project)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


def quicksort(list_to_be_sorted, comparison_list, low, high):
    if low < high:
        p = partition(list_to_be_sorted=list_to_be_sorted, comparison_list=comparison_list, low=low, high=high)
        quicksort(list_to_be_sorted=list_to_be_sorted, comparison_list=comparison_list, low=low, high=p-1)
        quicksort(list_to_be_sorted=list_to_be_sorted, comparison_list=comparison_list, low=p+1, high=high)


def partition(list_to_be_sorted, comparison_list, low, high):
    pivot = comparison_list[high]
    i = low

    for j in range(low, high):
        if comparison_list[j] <= pivot:
            swap(l=list_to_be_sorted, first=i, second=j)
            swap(l=comparison_list, first=i, second=j)
            i += 1

    swap(l=list_to_be_sorted, first=i, second=high)
    swap(l=comparison_list, first=i, second=high)
    return i


def swap(l, first, second):
    temp = l[first]
    l[first] = l[second]
    l[second] = temp
