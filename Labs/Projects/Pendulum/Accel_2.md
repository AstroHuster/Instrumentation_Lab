# 
- [Link](https://stackoverflow.com/questions/34319469/stepper-motor-linear-acceleration)

> Something faintly like this

``` python
accel = 20.0  # steps/sec/sec
time_passed = 0.000
steps_done = 0
cur_speed = 0  # steps/sec
time_for_next_step = 0.0

while (steps_done < steps_needed):
    if (time_passed >= time_for_next_step): 
        self.oneStep(direction, stepstyle)
        steps_done += 1
        time_for_next_step = time_passed + 1.0/cur_speed
    time.sleep(1);  # 1 millisecond, I assume
    time_passed += 0.001
    cur_speed += accel/1000.0
```
