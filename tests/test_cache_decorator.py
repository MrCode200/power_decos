from power_decos import Cache

import time
import pytest

@pytest.fixture
def cache():
    """Fixture to provide a fresh Cache instance."""
    return Cache()


def test_get_cached_value_exact_match(cache):
    """Test that get_cached_value returns the correct result for an exact match."""
    # Add a cache entry
    cache.manual_cache('test_func', 'result_1', 1, 2, key='value')

    # Retrieve with exact match
    result = cache.get_cached_value('test_func', 1, 2, key='value')

    assert result == 'result_1', "Expected result_1 but got different result"


def test_get_cached_value_partial_match_args(cache):
    """Test that get_cached_value returns results for partial match on args."""
    # Add multiple cache entries
    cache.manual_cache('test_func', 'result_1', 1, 2, key='value')
    cache.manual_cache('test_func', 'result_2', 3, 4, key='another_value')

    # Retrieve with partial match on args
    results = cache.get_cached_value('test_func', 1, 2, compare_all=False)

    assert results == ['result_1'], "Expected result_1 but got different results"


def test_get_cached_value_partial_match_kwargs(cache):
    """Test that get_cached_value returns results for partial match on kwargs."""
    # Add multiple cache entries
    cache.manual_cache('test_func', 'result_1', 1, 2, key='value')
    cache.manual_cache('test_func', 'result_2', 1, 2, key='another_value')

    # Retrieve with partial match on kwargs
    results = cache.get_cached_value('test_func', compare_all=False, key='value')

    assert results == ['result_1'], "Expected result_1 but got different results"


def test_get_cached_value_no_match(cache):
    """Test that get_cached_value returns None when no match is found."""
    # Add a cache entry
    cache.manual_cache('test_func', 'result_1', 1, 2, key='value')

    # Retrieve with no match
    result = cache.get_cached_value('test_func', True, 3, 4, key='no_match')

    assert result is None, "Expected None but got a result"


def test_clear_cache(cache):
    """Test that clear_cache method empties the cache."""
    # Add cache entries
    cache.manual_cache('test_func1', 'result_1', 1, 2)
    cache.manual_cache('test_func2', 'result_2', 3, 4, key='value')

    # Ensure the cache has entries before clearing
    assert len(cache.cache) == 2, "Cache should have 2 entries before clearing"

    # Clear the cache
    cache.clear_cache()

    # Ensure the cache is empty
    assert len(cache.cache) == 0, "Cache should be empty after clearing"


def test_cache_performance(cache):
    """Test that @cache decorator improves performance by using time.sleep."""

    @cache.cache_func
    def slow_function(x):
        """Simulates a slow function with time.sleep."""
        time.sleep(1)  # Simulates a delay
        return x * x

    # Measure the time taken for the first call (should be slow)
    start_time = time.time()
    slow_function(5)
    end_time = time.time()
    duration_first_call = end_time - start_time

    # Measure the time taken for the second call (should be faster due to caching)
    start_time = time.time()
    slow_function(5)
    end_time = time.time()
    duration_second_call = end_time - start_time

    # Check that the second call was faster than the first call
    assert duration_second_call < duration_first_call, "The second call should be faster than the first call"