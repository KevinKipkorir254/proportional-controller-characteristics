# Motor Response Experiment Documentation

## 1. Experiment Overview

This experiment aims to analyze the response characteristics of a motor system using a step input and evaluate key performance metrics i.e. steady-state behavior, noise filtering, and frequency response.

## 2. Experiment Setup

### Hardware Components

- Motor: [Specify motor model]
- Motor Driver: L298
- Microcontroller: [Specify MCU]
- Power Supply: [Specify voltage and current rating]
- Sensor: [Specify type and model]

### Software Components

- Control Algorithm: [Specify method, e.g., PID, open-loop PWM]
- Sampling Frequency: 100 Hz
- Filtering: Second-order filter
- Data Logging: [Specify software or method used]

## 3. Methodology

1. Apply a step input from 2 rad/s to 3 rad/s.
2. Measure the motor's velocity response using the sensor.
3. Apply a second-order filter to reduce noise.
4. Collect data at 100 Hz sampling rate.
5. Plot the response for visualization.

![Data processed data output](Time_series_data.png)

## 4. Observations & Key Findings

- Steady-State Behavior: [Describe whether the motor reached expected final speed]
- Rise Time Analysis: Not accurately measurable due to sampling limitations.
- Noise & Filtering: [Describe filter effectiveness and any distortions]
- Unexpected Behavior: Observed faster rise times with lower gains, suggesting possible system non-linearity.

![Time series characteristics](Time_series_characteristics.png)

## 5. Challenges & Limitations

- Limited Sampling Rate: 100 Hz is too low for precise transient analysis.
- Voltage Drop in L298: May be affecting torque and acceleration.
- Sensor Noise: Requires filtering, but filtering may impact transient accuracy.

## 6. Future Improvements

- Use a higher-frequency sampling system for transient analysis.
- Test with a MOSFET-based motor driver to reduce voltage drop.
- Compare performance with alternative filtering techniques.
- Investigate the unexpected rise time behavior by modeling system dynamics.

## 7. Conclusion

The experiment provided insights into the motor’s steady-state behavior and filtering effectiveness. However, limitations in sampling rate and motor driver performance affected rise time analysis. Future work will focus on improving hardware and software to obtain more accurate system dynamics.