"""
    Utility methods used for creating storage
"""

import re
from typing import List


def get_sub_wildcard_queries(query: str, wildcard: str = '*') -> List[str]:
    """
        This method splits a wildcard query into sub-queries in such a way that
        if it matches an arbitrary string, then all its sub-queries also match
        that string. This is achieved by splitting the query by the wildcard and
        then adding it back as prefix and suffix to the splits.

            :Example:

            .. code-block:: python

                "ab*c" -> ["ab*", "*c"]
                "*a*b" -> ["*a*", "*b"]
                "ab**" -> ["ab*"]

        See unit tests for more examples.

        :param query: wildcard query
        :param wildcard: wildcard char in the query. Default set to '*'
        :returns: list of sub-queries
    """
    # Remove consecutive wildcard duplicates, e.g. ab** -> ab*
    _query = query
    dup_pattern = r"\*\**" if wildcard == '*' else r'{0}{0}*'.format(wildcard)
    for rep in re.findall(dup_pattern, query):
        _query = query.replace(rep, wildcard)

    # Split if wildcard is in query and length of query is greater than 1
    if wildcard in _query and len(_query) > 1:
        # Adjust query start index if wildcard present as first character
        start = 1 if _query[0] == wildcard else 0
        # Adjust query end index if wildcard present as last character
        end = len(_query) - 1 if _query[-1] == wildcard else len(_query)

        # Split adjusted query by wildcard to get sub-queries
        sub_queries = _query[start:end].split(wildcard)

        # Compensate the starting sub-query due to adjusted query
        sub_queries[0] = _query[:start] + sub_queries[0]
        for idx in range(len(sub_queries) - 1):
            # Add wildcard as suffix
            sub_queries[idx] = sub_queries[idx] + wildcard
            # Add wildcard as prefix of the next member
            sub_queries[idx + 1] = wildcard + sub_queries[idx + 1]
        # Compensate the last sub-query due to adjusted query
        sub_queries[-1] = sub_queries[-1] + _query[end:]

        return sub_queries

    return [_query]


def get_all_wildcard_queries(string: str, wildcard: str = '*') -> List[str]:
    """
        This method computes all possible wildcard queries matching given
        string.

            :Example:

            .. code-block:: python

                "a" -> ['a', '*', '*a*', 'a*', '*a']
                "ab" -> ['ab', '*', '*a*', 'a*', '*b', '*b*', '*ab*', 'ab*', '*ab']

        See unit tests for more examples.

        :param string: string for which to obtain queries
        :param wildcard: wildcard char in query. Default set to '*'
        :returns: list of queries
    """
    # Add the string and wildcard char as default queries
    queries = {string: True, wildcard: True}

    # Compute other queries using n-grams
    length = len(string)
    for n_gram in range(length):
        # Compute N-grams
        size = length - n_gram
        span = n_gram + 1
        queries[wildcard + string[:span] + wildcard] = True
        queries[string[:span] + wildcard] = True
        for i in range(1, size - 1):
            queries[wildcard + string[i:i + span] + wildcard] = True
        queries[wildcard + string[size - 1:size - 1 + span]] = True
        queries[wildcard + string[size - 1:size - 1 + span] + wildcard] = True

    return list(queries.keys())
