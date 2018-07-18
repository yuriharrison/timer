"""Timer"""
import time
import functools
from threading import Thread


class Chronometer:
    """Simple chronometer with context manager support

    # Properties
        partial: float, current couting in seconds
        running: boolean, chronometer current state

    # Example

    ```python
    import time

    chr = Chronometer()
    chr.start()
    time.sleep(5)
    print('Partial:', chr.partial)
    chr.stop()
    assert not chr.running
    chr.reset()

    # or use with the context manager

    with Chronometer() as chr:
        assert chr.running
        time.sleep(5)
        print('Partial:', chr.partial)
    ```
    """
    def __init__(self):
        self.__running = False
        self.__start = None
        self.__end = None
        self.__stop_partial = 0
    
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *i):
        self.stop()

    def start(self):
        """Starts the chronometer or resume the latest stop"""
        if self.__running == True:
            return

        self.__running = True
        self.__start = time.clock()

    def reset(self):
        """Call Chronometer.stop(reset=True)"""
        self.stop(reset=True)

    def stop(self, reset=False):
        """Stops the chronometer
        
        # Arguments
            reset: optional, boolean, default `False`
                - `True` - Reset the chronometer to zero
                - `False` - Maintain the current count
        """
        if reset:
            self.__stop_partial = 0
        else:
            self.__stop_partial = self.partial

        self.__running = False

    @property
    def partial(self):
        if self.__running:
            return time.clock() - self.__start + self.__stop_partial
        else:
            return self.__stop_partial
    
    @property
    def running(self):
        return self.__running


class ChronometerDecorator(Chronometer):
    """Chronometer Decorator

    Use this decorator to measure time when executing functions
    or methods.

    # Example

    ```
    import time


    @ChronometerDecorator()
    def foo(msg):
        print(msg)
        time.sleep(3)

    @ChronometerDecorator(print_sum=True)
    def bar():
        time.sleep(1)

    class baz:
        def __init__(self):
            self.message = 'Works on methods as well!'
            
        @ChronometerDecorator(method=True)
        def qux(self):
            time.sleep(3)
            print(self.message)

    foo('Starting ChronometerDecorator test!')
    for _ in range(3): bar()
    baz().qux()

    ''' Result example:
    Starting ChronometerDecorator test!
    [ChronometerDecorator]: Function foo > Time: 2.9994740292006554
    [ChronometerDecorator]: Function bar > Time: 1.000767622853573 - Total: 1.000767622853573
    [ChronometerDecorator]: Function bar > Time: 0.9999331681037802 - Total: 2.000700790957353
    [ChronometerDecorator]: Function bar > Time: 0.9999622418665695 - Total: 3.0006630328239225
    Works on methods as well!
    [ChronometerDecorator]: Method qux > Time: 3.0000543717121673
    '''

    ```
    """
    
    def __init__(self, method=False, print_sum=False):
        self.time_ls = []
        self.method = method
        self.print_sum = print_sum
        super().__init__()
        
    def __call__(self, function=None):
        self._function = function
        self.func_name = function.__name__
        
        if self.method:
            return functools.partialmethod(ChronometerDecorator.method_call, self)
        else:
            return self.function_call
        
    def function_call(self, *a, **kw):
        self.start()
        self._function(*a, **kw)
        self.stop()
        self.register()

    @staticmethod
    def method_call(func_self, self, *a, **kw):
        self.start()
        self._function(func_self, *a, **kw)
        self.stop()
        self.register()
        
    def register(self):
        self.time_ls.append(self.partial)
        
        msg_sum = ''
        if self.print_sum:
            msg_sum = ' - Total: {}'.format(sum(self.time_ls))
            
        msg_func_name = 'Method' if self.method else 'Function' 
        msg_func_name += ' {} >'.format(self.func_name)
        msg = '[ChronometerDecorator]: {} Time: {}{}'\
            .format(msg_func_name, self.partial, msg_sum)
        print(msg)
        self.reset()


class Timer(Chronometer):
    """Countdown Timer with callback

    Timer inherit from [Chronometer](#chronometer-class)

    # Arguments
        time: int, required
            - Start of the countdown in seconds
        callback: function, optional, default `None`
            - Function to be triggered when the countdown hits zero

    # Properties
        time_left: float, time left in seconds

    # Example

    ```python
    import time

    def time_out():
        print('Time out!')

    timer = Timer(30, callback=time_out)

    with timer:
        assert timer.running
        print('Burning 10 seconds...')
        time.sleep(10)

    assert not timer.running

    print('Time left:', timer.time_left)
    print('Waiting without running the clock...')
    time.sleep(10)
    print('Time left:', timer.time_left)

    with timer:
        print('Running the clock till timeout')
        while timer.running:
            print('> + 15 seconds...')
            time.sleep(15)

    print('Finished!')
    ```
    """
    def __init__(self, time, callback=None):
        super().__init__()
        self.time_limit = time
        self.callback = callback
        self.time_out = False

    def __copy__(self):
        """Custom copy to clean the `callback` function"""
        new = type(self)(None, None)
        new.__dict__.update(self.__dict__)
        new.callback = None
        return self

    def __deepcopy__(self, memo):
        return self.__copy__()

    def start(self):
        """Starts the countdown and starts the thread (`_time_out` method)
        which will trigger the `callback`
        """
        if self.time_out:
            self.reset()

        super().start()
        Thread(target=self._time_out).start()

    def stop(self, **i):
        """Stops the countdown and stops the running thread"""
        super().stop(**i)

    def reset(self):
        super().reset()
        self.time_out = False

    @property
    def time_left(self):
        time_left = self.time_limit - self.partial
        time_left = time_left if time_left > 0 else 0
        return time_left

    def _time_out(self):
        """Asynchronous method that trigger the `callback` function
        when the `time_left` is zero
        """
        while True:
            if self.running:
                if self.time_left > 0:
                    time.sleep(.3)
                else:
                    self.stop()
                    self.time_out = True
                    if self.callback:
                        self.callback()
                    break
            else:
                break

