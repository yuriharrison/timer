<span style="float:right;">[[source code]](https://github.com/yuriharrison/connect-four-lab/blob/master/connectFourLab/game/timer.py#L177)</span>
## Timer

```python
connectFourLab.game.timer.Timer(time, callback=None)
```

Countdown Timer with callback

Timer inherit from [Chronometer](#chronometer-class)

__Arguments__

- `time` -  int, required
    - Start of the countdown in seconds
- `callback` -  function, optional, default `None`
    - Function to be triggered when the countdown hits zero

__Properties__

- `time_left` -  float, time left in seconds

__Example__


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


---
## Timer methods

### start


```python
start()
```


Starts the countdown and starts the thread (`_time_out` method)
which will trigger the `callback`


---
### stop


```python
stop()
```


Stops the countdown and stops the running thread

----

<span style="float:right;">[[source code]](https://github.com/yuriharrison/connect-four-lab/blob/master/connectFourLab/game/timer.py#L7)</span>
## Chronometer

```python
connectFourLab.game.timer.Chronometer()
```

Simple chronometer with context manager support

__Properties__

- `partial` -  float, current couting in seconds
- `running` -  boolean, chronometer current state

__Example__


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


---
## Chronometer methods

### start


```python
start()
```


Starts the chronometer or resume the latest stop

---
### stop


```python
stop(reset=False)
```


Stops the chronometer

__Arguments__

- `reset` -  optional, boolean, default `False`
    - `True` - Reset the chronometer to zero
    - `False` - Maintain the current count


---
### reset


```python
reset()
```


Call Chronometer.stop(reset=True)

----

<span style="float:right;">[[source code]](https://github.com/yuriharrison/connect-four-lab/blob/master/connectFourLab/game/timer.py#L87)</span>
## ChronometerDecorator

```python
connectFourLab.game.timer.ChronometerDecorator(method=False, print_sum=False)
```

Chronometer Decorator

Use this decorator to measure time when executing functions
or methods.

__Example__


```python
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
