"""
Input Sources Module
Digital Logic Design - Input Sources

This module provides various input signal sources for digital circuits:
- Power Supply (VCC/VDD)
- Ground (GND)
- Pulse Generators
- Clock Generators
- Manual Switches
- Function Generators
- Pattern Generators
"""

import time
import math
import random
from typing import List, Generator, Union

class PowerSource:
    """
    Power supply source (VCC/VDD)
    Provides constant logic high (1)
    """
    
    def __init__(self, voltage=5.0, name="VCC"):
        """
        Initialize power source
        
        Args:
            voltage (float): Supply voltage in volts
            name (str): Name of the power source
        """
        self.voltage = voltage
        self.name = name
        self.output = 1  # Always logic high
    
    def get_output(self):
        """Get power source output (always 1)"""
        return self.output
    
    def __call__(self):
        """Allow source to be called like a function"""
        return self.get_output()
    
    def __str__(self):
        return f"{self.name}: {self.voltage}V (Logic {self.output})"

class GroundSource:
    """
    Ground source (GND)
    Provides constant logic low (0)
    """
    
    def __init__(self, name="GND"):
        """
        Initialize ground source
        
        Args:
            name (str): Name of the ground source
        """
        self.name = name
        self.output = 0  # Always logic low
    
    def get_output(self):
        """Get ground output (always 0)"""
        return self.output
    
    def __call__(self):
        """Allow source to be called like a function"""
        return self.get_output()
    
    def __str__(self):
        return f"{self.name}: 0V (Logic {self.output})"

class ManualSwitch:
    """
    Manual switch input
    Can be toggled between 0 and 1
    """
    
    def __init__(self, initial_state=0, name="SW"):
        """
        Initialize manual switch
        
        Args:
            initial_state (int): Initial switch state (0 or 1)
            name (str): Name of the switch
        """
        self.state = initial_state
        self.name = name
    
    def toggle(self):
        """Toggle switch state"""
        self.state = 1 - self.state
        return self.state
    
    def set_state(self, state):
        """Set switch to specific state"""
        self.state = 1 if state else 0
        return self.state
    
    def get_output(self):
        """Get current switch state"""
        return self.state
    
    def __call__(self):
        """Allow switch to be called like a function"""
        return self.get_output()
    
    def __str__(self):
        return f"{self.name}: {'ON' if self.state else 'OFF'} (Logic {self.state})"

class PulseGenerator:
    """
    Pulse generator for creating single pulses or pulse trains
    """
    
    def __init__(self, pulse_width=1, pulse_count=1, initial_delay=0, name="PULSE"):
        """
        Initialize pulse generator
        
        Args:
            pulse_width (int): Width of each pulse in time units
            pulse_count (int): Number of pulses to generate (0 = infinite)
            initial_delay (int): Delay before first pulse
            name (str): Name of the pulse generator
        """
        self.pulse_width = pulse_width
        self.pulse_count = pulse_count
        self.initial_delay = initial_delay
        self.name = name
        
        # Internal state
        self.time = 0
        self.pulses_generated = 0
        self.current_output = 0
        self.pulse_start_time = None
    
    def get_output(self, time_step=None):
        """
        Get pulse generator output at current time
        
        Args:
            time_step (int): Optional time step to advance to
            
        Returns:
            int: Current output (0 or 1)
        """
        if time_step is not None:
            self.time = time_step
        
        # Check if we're in initial delay period
        if self.time < self.initial_delay:
            self.current_output = 0
            return self.current_output
        
        # Check if we've generated enough pulses
        if self.pulse_count > 0 and self.pulses_generated >= self.pulse_count:
            self.current_output = 0
            return self.current_output
        
        # Calculate relative time after initial delay
        relative_time = self.time - self.initial_delay
        
        # Determine if we should start a new pulse
        if self.pulse_start_time is None:
            self.pulse_start_time = relative_time
            self.current_output = 1
        
        # Check if current pulse should end
        if relative_time >= self.pulse_start_time + self.pulse_width:
            self.current_output = 0
            self.pulses_generated += 1
            self.pulse_start_time = None
        
        return self.current_output
    
    def step(self):
        """Advance time by one step"""
        self.time += 1
        return self.get_output()
    
    def reset(self):
        """Reset pulse generator to initial state"""
        self.time = 0
        self.pulses_generated = 0
        self.current_output = 0
        self.pulse_start_time = None
    
    def __str__(self):
        return f"{self.name}: Width={self.pulse_width}, Count={self.pulse_count}, Output={self.current_output}"

class ClockGenerator:
    """
    Clock generator for creating periodic square waves
    """
    
    def __init__(self, frequency=1.0, duty_cycle=0.5, phase=0, name="CLK"):
        """
        Initialize clock generator
        
        Args:
            frequency (float): Clock frequency in Hz
            duty_cycle (float): Duty cycle (0.0 to 1.0)
            phase (float): Phase offset in degrees
            name (str): Name of the clock generator
        """
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.phase = math.radians(phase)
        self.name = name
        
        # Internal state
        self.time = 0.0
        self.current_output = 0
    
    def get_output(self, time_step=None):
        """
        Get clock output at current time
        
        Args:
            time_step (float): Optional time step to advance to
            
        Returns:
            int: Current output (0 or 1)
        """
        if time_step is not None:
            self.time = time_step
        
        # Calculate the phase of the clock signal
        period = 1.0 / self.frequency if self.frequency > 0 else float('inf')
        phase_time = (self.time / period + self.phase / (2 * math.pi)) % 1.0
        
        # Determine output based on duty cycle
        self.current_output = 1 if phase_time < self.duty_cycle else 0
        
        return self.current_output
    
    def step(self, time_increment=0.1):
        """Advance time by specified increment"""
        self.time += time_increment
        return self.get_output()
    
    def reset(self):
        """Reset clock generator to initial state"""
        self.time = 0.0
        self.current_output = 0
    
    def set_frequency(self, frequency):
        """Set new frequency"""
        self.frequency = frequency
    
    def __str__(self):
        return f"{self.name}: {self.frequency}Hz, Duty={self.duty_cycle*100:.1f}%, Output={self.current_output}"

class FunctionGenerator:
    """
    Function generator for creating various waveforms
    """
    
    def __init__(self, waveform='square', frequency=1.0, amplitude=1.0, offset=0.0, name="FUNC"):
        """
        Initialize function generator
        
        Args:
            waveform (str): Waveform type ('square', 'sine', 'triangle', 'sawtooth')
            frequency (float): Frequency in Hz
            amplitude (float): Amplitude
            offset (float): DC offset
            name (str): Name of the function generator
        """
        self.waveform = waveform
        self.frequency = frequency
        self.amplitude = amplitude
        self.offset = offset
        self.name = name
        
        # Internal state
        self.time = 0.0
        self.threshold = 0.5  # Threshold for digital conversion
    
    def get_analog_output(self, time_step=None):
        """Get analog output value"""
        if time_step is not None:
            self.time = time_step
        
        if self.frequency == 0:
            return self.offset
        
        # Calculate angular frequency
        omega = 2 * math.pi * self.frequency
        
        # Generate waveform
        if self.waveform == 'sine':
            value = math.sin(omega * self.time)
        elif self.waveform == 'square':
            value = 1 if math.sin(omega * self.time) >= 0 else -1
        elif self.waveform == 'triangle':
            phase = (self.time * self.frequency) % 1.0
            value = 4 * abs(phase - 0.5) - 1
        elif self.waveform == 'sawtooth':
            phase = (self.time * self.frequency) % 1.0
            value = 2 * phase - 1
        else:
            value = 0
        
        return self.amplitude * value + self.offset
    
    def get_digital_output(self, time_step=None):
        """Get digital output (0 or 1) based on threshold"""
        analog_value = self.get_analog_output(time_step)
        return 1 if analog_value >= self.threshold else 0
    
    def get_output(self, time_step=None):
        """Get digital output (alias for get_digital_output)"""
        return self.get_digital_output(time_step)
    
    def step(self, time_increment=0.1):
        """Advance time by specified increment"""
        self.time += time_increment
        return self.get_output()
    
    def reset(self):
        """Reset function generator to initial state"""
        self.time = 0.0
    
    def __str__(self):
        return f"{self.name}: {self.waveform.title()} {self.frequency}Hz, Output={self.get_output()}"

class PatternGenerator:
    """
    Pattern generator for creating custom bit patterns
    """
    
    def __init__(self, pattern: List[int], repeat=True, name="PATTERN"):
        """
        Initialize pattern generator
        
        Args:
            pattern (List[int]): List of 0s and 1s defining the pattern
            repeat (bool): Whether to repeat the pattern
            name (str): Name of the pattern generator
        """
        self.pattern = pattern
        self.repeat = repeat
        self.name = name
        
        # Internal state
        self.index = 0
        self.finished = False
    
    def get_output(self):
        """Get current pattern output"""
        if self.finished:
            return 0
        
        if not self.pattern:
            return 0
        
        output = self.pattern[self.index]
        return output
    
    def step(self):
        """Advance to next pattern element"""
        if self.finished:
            return 0
        
        if not self.pattern:
            return 0
        
        output = self.get_output()
        self.index += 1
        
        if self.index >= len(self.pattern):
            if self.repeat:
                self.index = 0
            else:
                self.finished = True
        
        return output
    
    def reset(self):
        """Reset pattern generator to beginning"""
        self.index = 0
        self.finished = False
    
    def set_pattern(self, pattern: List[int]):
        """Set new pattern"""
        self.pattern = pattern
        self.reset()
    
    def __str__(self):
        pattern_str = ''.join(map(str, self.pattern))
        return f"{self.name}: [{pattern_str}] Index={self.index}, Output={self.get_output()}"

class RandomGenerator:
    """
    Random bit generator
    """
    
    def __init__(self, probability=0.5, seed=None, name="RANDOM"):
        """
        Initialize random generator
        
        Args:
            probability (float): Probability of generating 1 (0.0 to 1.0)
            seed (int): Random seed for reproducibility
            name (str): Name of the random generator
        """
        self.probability = probability
        self.name = name
        
        if seed is not None:
            random.seed(seed)
    
    def get_output(self):
        """Get random output"""
        return 1 if random.random() < self.probability else 0
    
    def __call__(self):
        """Allow generator to be called like a function"""
        return self.get_output()
    
    def set_probability(self, probability):
        """Set new probability"""
        self.probability = max(0.0, min(1.0, probability))
    
    def __str__(self):
        return f"{self.name}: P(1)={self.probability:.2f}, Output={self.get_output()}"

class DebounceSwitch:
    """
    Debounced switch with realistic mechanical switch behavior
    """
    
    def __init__(self, debounce_time=3, initial_state=0, name="DB_SW"):
        """
        Initialize debounced switch
        
        Args:
            debounce_time (int): Debounce time in time units
            initial_state (int): Initial switch state
            name (str): Name of the switch
        """
        self.debounce_time = debounce_time
        self.stable_state = initial_state
        self.raw_state = initial_state
        self.output_state = initial_state
        self.name = name
        
        # Debounce state
        self.change_time = 0
        self.time = 0
        self.state_stable = True
    
    def press(self):
        """Press the switch (change to opposite state)"""
        new_state = 1 - self.raw_state
        self._change_raw_state(new_state)
    
    def set_state(self, state):
        """Set switch to specific state"""
        self._change_raw_state(1 if state else 0)
    
    def _change_raw_state(self, new_state):
        """Internal method to change raw state"""
        if self.raw_state != new_state:
            self.raw_state = new_state
            self.change_time = self.time
            self.state_stable = False
    
    def step(self):
        """Advance time and update debounced output"""
        self.time += 1
        
        # Check if debounce time has elapsed
        if not self.state_stable:
            if self.time - self.change_time >= self.debounce_time:
                self.output_state = self.raw_state
                self.stable_state = self.raw_state
                self.state_stable = True
        
        return self.output_state
    
    def get_output(self):
        """Get current debounced output"""
        return self.output_state
    
    def __str__(self):
        return f"{self.name}: Raw={self.raw_state}, Output={self.output_state}, Stable={self.state_stable}"
