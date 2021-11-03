import logging
import threading
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock

from typing import Callable


class SafeCounter:
    """Simple thread-safe counter"""

    def __init__(self, initial_value: int = 0):
        self.value = initial_value
        self.lock = Lock()

    def add(self, value: int = 1):
        with self.lock:
            self.value += value
            return self.value

    def sub(self, value: int = 1):
        with self.lock:
            self.value -= value
            return self.value

    def zero(self):
        with self.lock:
            self.sub(self.value)

    def get_value(self):
        with self.lock:
            return self.value


class ThreadPool:
    """Thread pool allowing to check busy status"""

    def __init__(self, callback: Callable = None, max_workers=None,
                 thread_name_prefix='', initializer=None, initargs=(),
                 enable_logging=False):
        self.callback = callback
        self.counter = SafeCounter(0)
        self.cv = threading.Condition()
        self.enable_logging = enable_logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tp = ThreadPoolExecutor(max_workers, thread_name_prefix, initializer, initargs)

    def submit(self, func, *args, **kwargs):
        with self.cv:
            while self.busy():
                self.cv.wait()
            return self.submit_(func, *args, **kwargs)

    def submit_(self, func, *args, **kwargs):
        self.counter.add()
        future = self.tp.submit(func, *args, **kwargs)
        future.add_done_callback(self.callback_)
        return future

    def callback_(self, future: Future):
        if self.enable_logging:
            self.logger.info(self.info("callback"))
        if future.done():
            if self.callback:
                self.callback(future)
            with self.cv:
                self.counter.sub()
                self.cv.notify()

    def busy(self):
        """Check if thread pool is busy i.e. all worker threads busy.
        Accessing protected member tp._max_workers, which is not ideal, and, I am
        not happy about it. However, if we decide to keep separate max_workers
        in ThreadPool we complicate things as there is a specific logic to adjust
        worker thread count: _adjust_thread_count"""
        return self.counter.value == self.tp._max_workers

    def set_logger(self, logger: logging.Logger):
        if not logger:
            raise AttributeError("logger must not be null")
        self.logger = logger

    def info(self, msg):
        thread_name = threading.current_thread().getName()
        return f"{thread_name} {msg}"





