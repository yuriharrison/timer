<span style="float:right;">[[source code]](https://github.com/yuriharrison/connect-four-lab/blob/master/connectFourLab/game/timer.py#L86)</span>
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

<span style="float:right;">[[source code]](https://github.com/yuriharrison/connect-four-lab/blob/master/connectFourLab/game/timer.py#L6)</span>
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