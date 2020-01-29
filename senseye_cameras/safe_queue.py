import queue
import logging

log = logging.getLogger(__name__)

class SafeQueue(queue.Queue):
    """
    Class that extends Python Queue to safely handle exceptions from Queue
    accessor methods.
    """

    def __init__(self, maxsize=0, module='Generic'):
        super().__init__(maxsize=maxsize)

        # Information on where the queue is being used for debug information
        self.module = module

    def put(self, item, block=True, timeout=None, force=False):
        """
        Attempt to insert an item into the queue, handling the Full exception if
        it arises. Return True if item is successfully enqueued. If a force was
        required, return the dequeued item.
        """
        ret = True
        try:
            if self.full() and force:
                # When force is enabled, do a blocking dequeue
                ret = self.get()

            super().put(item=item, block=block, timeout=timeout)
        except queue.Full:
            log.debug(f'Queue module {self.module} is full. {item} not inserted')
            return False
        return ret

    def put_nowait(self, item, force=False):
        """
        Non-blocking put with exception handling.
        """
        return self.put(item, block=False, force=force)

    def get(self, block=True, timeout=None):
        """
        Attempt to retrieve an element from the queue, handling the Empty
        exception if it arises. Returns the item or None if dequeue is
        unsuccessful.

        Note: It is possible that a None object was enqueued. Checking for a
        None value on a get() call will be ambiguous in this case. It may mean
        the original item was None or that the queue is empty.
        """
        try:
            return super().get(block=block, timeout=timeout)
        except queue.Empty:
            log.debug(f'Queue module {self.module} is empty. Capacity is {self.maxsize}')
            return None

    def get_nowait(self):
        """
        Non-blocking get with exception handling.
        """
        return self.get(block=False)

    def to_list(self):
        """
        Converts queue to a list.
        """
        ret_list = []
        with self.mutex:
            ret_list = list(self.queue)
        return ret_list

    def remove_existing(self, num_elements=None):
        """
        Pops items from self queue and appends to a list.
        Mutates self queue by removing qsize elements.

        Note: If you force an item to be input into the queue during this
        operation, you may clobber data. For example:
        - SafeQueue size is 10 when remove_existing() is called
        - SafeQueue maxsize is 10
        - SafeQueue.put_nowait(an_item, force=True)
        - The first item is forced off, and may not have been grabbed into the
        list.
        - Using a mutex here may cause a deadlock.
        """
        outgoing = []
        # Attempt to remove passed number of elements, with all elements
        # being the default.
        #
        # If number requested is more than number of elements, remove all
        # elements
        size = num_elements
        if not num_elements or size > self.qsize():
            size = self.qsize()

        for i in range(0,size):
            outgoing.append(self.get_nowait())

        return outgoing

    def __str__(self):
        """
        Outputs readable version of items in queue by using list representation.
        """
        return self.to_list().__str__()
