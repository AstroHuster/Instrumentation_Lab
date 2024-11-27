# Acceleration/deceleration profile
Use microstepping mode.

To accelerate a stepper from a starting speed to a desired
target speed, the current speed just needs to be changed
at periodic intervals. Most engineers use microcontrollers
to achieve stepper control. The most common 
implementation uses only two timers. The first is a 
steps-per-second (SPS) timer used to generate an accurate 
timing function
for the stepping rate. The second is an acceleration timer
used to alter the first timer on a periodic basis. Since the
speed is being changed at timely intervals, in essence the
angular velocity with respect to time (dv/dt) is being
derived. This derivation is called acceleration, or how
speed changes across time. Figure 2 shows an enlarged
view of a typical microcontroller-based acceleration profile
and what is happening as the stepper is accelerated
towards a target speed.

The SPS is the desired number of steps per second, or
the stepping rate, at which the motor should move. The
SPS timer must be programmed to issue pulses at this
rate. Depending on the timer’s oscillator frequency, a
typical equation is
$$
SPS_{timer register} = \frac{timer_{oscillator}}{SPS}
$$
where SPS_timer_register is a 16-bit number that tells the
timer how long it takes to generate subsequent STEP
pulses, and timer_oscillator is a constant of how fast the
timer is running in megahertz.

This equation is stored in a function because it is used
quite frequently. To see how it works, assume that the timer
oscillator is running at 8 MHz and the desired stepping
rate for the motor is 200 SPS. According to the equation,
the program code makes the value of SPS_timer_register
equal to 40,000. So every 40,000 timer clicks, a STEP pulse
is generated. This results in a timer-based output of 200
pulses per second and a shaft rotation equal to 200 SPS.

Every time such an event takes place, an interrupt is
generated and the timer is cleared. The timing of the rising
edge at the STEP input is crucial to the microstepping
driver’s accuracy, but the falling edge can happen at
almost any time as long as it is well before the next STEP
rising edge.

Two parameters are needed to define the acceleration
curve: (1) how often to change the SPS value, and (2) by
how much. The acceleration curve is directly proportional
to both parameters; that is, the more often the SPS value
is updated and the higher its value, the steeper will be the
acceleration curve. The acceleration timer handles both
parameters: The timer function fires as many times per
second as is desired to change the SPS value, and the
timer’s interrupt-service routine (ISR) determines what
the new speed is by incrementing the current SPS by a
predetermined factor.

The acceleration rate is measured in steps per second
per second (SPSPS), or by how many times per second
the current SPS rate is changed. If the SPS value is changed
by adding a one, the acceleration timer’s ISR must be called
(triggered) for each change in the acceleration rate. For
example, with an acceleration rate of 1000 SPSPS, the
motor speed can be started at 200 SPS and incremented
by one until it reaches 1200 SPS. The acceleration timer’s
ISR would then need to be called 1000 times

