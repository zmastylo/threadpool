import time
from concurrent.futures import Future

import pytest

from tpool import ThreadPool


@pytest.fixture()
def get_tp(max_workers=None) -> ThreadPool:
    max_workers = max_workers or 1
    return ThreadPool(max_workers=max_workers)


@pytest.fixture()
def get_sleep_func() -> time.sleep:
    return time.sleep


@pytest.fixture()
def get_func():
    return lambda x: x*x


@pytest.mark.parametrize("max_workers, sleep_time", [
    (2, 1), (3, 1), (5, 2), (3, 2), (5, 1)
])
def test_thread_pool_non_busy(get_sleep_func, max_workers, sleep_time):
    tp = ThreadPool(max_workers=max_workers)
    func = get_sleep_func

    tp.submit(func=func, args=(sleep_time, ))
    is_busy = tp.busy()
    assert not is_busy


@pytest.mark.parametrize("max_workers, num_submits, sleep_time", [
    (1, 2, 2), (3, 3, 1)
])
def test_thread_pool_busy(get_sleep_func, max_workers, num_submits, sleep_time):
    tp = ThreadPool(max_workers=max_workers)
    func = get_sleep_func

    for _ in range(num_submits):
        tp.submit(func, sleep_time)

    is_busy = tp.busy()
    assert is_busy


def test_thread_pool_future(get_func, get_sleep_func):
    tp = ThreadPool(max_workers=1)

    func = get_func
    future: Future = tp.submit(func, 3)
    result = future.result()
    assert result == 9

    future = tp.submit(get_sleep_func, 5)
    is_busy = tp.busy()
    assert is_busy

    future.cancel()
    is_busy = tp.busy()
    assert not is_busy

    def f(sleep_time, number):
        get_sleep_func(sleep_time)
        return number*number

    future = tp.submit(f, 2, 5)
    is_busy = tp.busy()
    assert is_busy
    assert not future.done()
    assert not future.cancelled()

    future.cancel()
    assert future.cancelled()
    is_busy = tp.busy()
    assert not is_busy

    future = tp.submit(f, 1, 5)
    assert not future.done()
    get_sleep_func(2)
    assert future.done()
    result = future.result()
    assert result == 25








