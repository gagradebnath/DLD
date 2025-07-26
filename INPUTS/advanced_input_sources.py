"""
Advanced Input Sources Module
Digital Logic Design - Advanced Input Sources

This module provides advanced input signal sources:
- Multi-phase Clock Generators
- Burst Generators
- Ramp Generators
- Noise Generators
- Signal Multiplexers
- Analog-to-Digital Converters
"""

import math
import random
from typing import List, Dict, Any
from input_sources import ClockGenerator, PowerSource, GroundSource

class MultiPhaseClockGenerator:
    """
    Multi-phase clock generator for creating multiple clock signals with phase shifts
    """
    
    def __init__(self, frequency=1.0, phases=[0, 90, 180, 270], duty_cycle=0.5, name="MULTI_CLK"):
        """
        Initialize multi-phase clock generator
        
        Args:
            frequency (float): Base frequency in Hz
            phases (List[float]): List of phase shifts in degrees
            duty_cycle (float): Duty cycle for all phases
            name (str): Name of the generator
        """
        self.frequency = frequency
        self.phases = phases
        self.duty_cycle = duty_cycle
        self.name = name
        
        # Create individual clock generators for each phase
        self.clocks = {}
        for i, phase in enumerate(phases):
            self.clocks[f"Phase{i}"] = ClockGenerator(
                frequency=frequency,
                duty_cycle=duty_cycle,
                phase=phase,
                name=f"{name}_PH{i}"
            )
        
        self.time = 0.0
    
    def get_outputs(self, time_step=None):
        """
        Get all phase outputs
        
        Args:
            time_step (float): Optional time step
            
        Returns:
            Dict[str, int]: Dictionary of phase outputs
        """
        if time_step is not None:
            self.time = time_step
        
        outputs = {}
        for phase_name, clk in self.clocks.items():
            outputs[phase_name] = clk.get_output(self.time)
        
        return outputs
    
    def step(self, time_increment=0.1):
        """Advance time and get outputs"""
        self.time += time_increment
        return self.get_outputs()
    
    def reset(self):
        """Reset all phase clocks"""
        self.time = 0.0
        for clk in self.clocks.values():
            clk.reset()
    
    def __str__(self):
        outputs = self.get_outputs()
        output_str = ', '.join([f"{k}={v}" for k, v in outputs.items()])
        return f"{self.name}: {self.frequency}Hz, [{output_str}]"

class BurstGenerator:
    """
    Burst generator for creating bursts of pulses
    """
    
    def __init__(self, burst_length=5, burst_period=10, pulse_frequency=10.0, name="BURST"):
        """
        Initialize burst generator
        
        Args:
            burst_length (int): Number of pulses in each burst
            burst_period (int): Time between burst starts
            pulse_frequency (float): Frequency of pulses within burst
            name (str): Name of the generator
        """
        self.burst_length = burst_length
        self.burst_period = burst_period
        self.pulse_frequency = pulse_frequency
        self.name = name
        
        # Internal state
        self.time = 0
        self.current_burst_start = 0
        self.pulses_in_current_burst = 0
        self.pulse_clock = ClockGenerator(frequency=pulse_frequency)
    
    def get_output(self, time_step=None):
        """Get burst generator output"""
        if time_step is not None:
            self.time = time_step
        
        # Check if we should start a new burst
        time_in_period = self.time % self.burst_period
        burst_duration = self.burst_length / self.pulse_frequency
        
        if time_in_period < burst_duration:
            # We're in a burst period
            burst_time = time_in_period
            return self.pulse_clock.get_output(burst_time)
        else:
            # We're in the quiet period between bursts
            return 0
    
    def step(self, time_increment=0.1):
        """Advance time"""
        self.time += time_increment
        return self.get_output()
    
    def reset(self):
        """Reset burst generator"""
        self.time = 0
        self.pulse_clock.reset()
    
    def __str__(self):
        return f"{self.name}: {self.burst_length} pulses @ {self.pulse_frequency}Hz, period={self.burst_period}, Output={self.get_output()}"

class RampGenerator:
    """
    Ramp generator for creating sawtooth or triangle ramps
    """
    
    def __init__(self, ramp_time=10, ramp_type='sawtooth', amplitude=1.0, threshold=0.5, name="RAMP"):
        """
        Initialize ramp generator
        
        Args:
            ramp_time (float): Time for one complete ramp cycle
            ramp_type (str): 'sawtooth' or 'triangle'
            amplitude (float): Peak amplitude
            threshold (float): Threshold for digital conversion
            name (str): Name of the generator
        """
        self.ramp_time = ramp_time
        self.ramp_type = ramp_type
        self.amplitude = amplitude
        self.threshold = threshold
        self.name = name
        
        self.time = 0.0
    
    def get_analog_output(self, time_step=None):
        """Get analog ramp output"""
        if time_step is not None:
            self.time = time_step
        
        if self.ramp_time <= 0:
            return 0
        
        # Calculate position in ramp cycle (0 to 1)
        cycle_position = (self.time % self.ramp_time) / self.ramp_time
        
        if self.ramp_type == 'sawtooth':
            # Linear ramp from 0 to amplitude
            value = cycle_position * self.amplitude
        elif self.ramp_type == 'triangle':
            # Triangle wave
            if cycle_position < 0.5:
                value = 2 * cycle_position * self.amplitude
            else:
                value = 2 * (1 - cycle_position) * self.amplitude
        else:
            value = 0
        
        return value
    
    def get_digital_output(self, time_step=None):
        """Get digital output based on threshold"""
        analog_value = self.get_analog_output(time_step)
        return 1 if analog_value >= self.threshold else 0
    
    def get_output(self, time_step=None):
        """Get digital output (alias)"""
        return self.get_digital_output(time_step)
    
    def step(self, time_increment=0.1):
        """Advance time"""
        self.time += time_increment
        return self.get_output()
    
    def reset(self):
        """Reset ramp generator"""
        self.time = 0.0
    
    def __str__(self):
        analog = self.get_analog_output()
        digital = self.get_digital_output()
        return f"{self.name}: {self.ramp_type.title()}, Analog={analog:.2f}, Digital={digital}"

class NoiseGenerator:
    """
    Noise generator for creating random noise signals
    """
    
    def __init__(self, noise_type='white', amplitude=1.0, frequency=1.0, threshold=0.0, seed=None, name="NOISE"):
        """
        Initialize noise generator
        
        Args:
            noise_type (str): Type of noise ('white', 'pink', 'digital')
            amplitude (float): Noise amplitude
            frequency (float): Update frequency for digital noise
            threshold (float): Threshold for digital conversion
            seed (int): Random seed
            name (str): Name of the generator
        """
        self.noise_type = noise_type
        self.amplitude = amplitude
        self.frequency = frequency
        self.threshold = threshold
        self.name = name
        
        if seed is not None:
            random.seed(seed)
        
        self.time = 0.0
        self.last_update_time = 0.0
        self.current_value = 0.0
    
    def get_analog_output(self, time_step=None):
        """Get analog noise output"""
        if time_step is not None:
            self.time = time_step
        
        if self.noise_type == 'white':
            # White noise - new random value each call
            self.current_value = (random.random() - 0.5) * 2 * self.amplitude
        elif self.noise_type == 'digital':
            # Digital noise - update at specified frequency
            update_period = 1.0 / self.frequency if self.frequency > 0 else float('inf')
            if self.time - self.last_update_time >= update_period:
                self.current_value = (random.random() - 0.5) * 2 * self.amplitude
                self.last_update_time = self.time
        elif self.noise_type == 'pink':
            # Simplified pink noise (just reduced amplitude white noise)
            self.current_value = (random.random() - 0.5) * self.amplitude * 0.5
        
        return self.current_value
    
    def get_digital_output(self, time_step=None):
        """Get digital noise output"""
        analog_value = self.get_analog_output(time_step)
        return 1 if analog_value >= self.threshold else 0
    
    def get_output(self, time_step=None):
        """Get digital output (alias)"""
        return self.get_digital_output(time_step)
    
    def step(self, time_increment=0.1):
        """Advance time"""
        self.time += time_increment
        return self.get_output()
    
    def reset(self):
        """Reset noise generator"""
        self.time = 0.0
        self.last_update_time = 0.0
        self.current_value = 0.0
    
    def __str__(self):
        return f"{self.name}: {self.noise_type.title()}, Output={self.get_output()}"

class SignalMultiplexer:
    """
    Signal multiplexer for selecting between multiple input sources
    """
    
    def __init__(self, sources: List[Any], select_bits=2, name="MUX"):
        """
        Initialize signal multiplexer
        
        Args:
            sources (List): List of input source objects
            select_bits (int): Number of select bits
            name (str): Name of the multiplexer
        """
        self.sources = sources
        self.select_bits = select_bits
        self.max_inputs = 2 ** select_bits
        self.name = name
        
        # Pad sources list if needed
        while len(self.sources) < self.max_inputs:
            self.sources.append(GroundSource(f"GND_{len(self.sources)}"))
        
        # Truncate if too many sources
        self.sources = self.sources[:self.max_inputs]
        
        # Select control
        self.select_value = 0
    
    def set_select(self, select_value):
        """Set the select control value"""
        self.select_value = select_value % self.max_inputs
    
    def get_output(self, time_step=None):
        """Get multiplexer output"""
        if 0 <= self.select_value < len(self.sources):
            source = self.sources[self.select_value]
            if hasattr(source, 'get_output'):
                # Try with time_step first, fallback to no parameters
                try:
                    if time_step is not None:
                        return source.get_output(time_step)
                    else:
                        return source.get_output()
                except TypeError:
                    # Source doesn't accept time_step parameter
                    return source.get_output()
            elif callable(source):
                return source()
            else:
                return 0
        return 0
    
    def step(self, time_increment=0.1):
        """Step all sources and get output"""
        # Step sources that support it
        for source in self.sources:
            if hasattr(source, 'step'):
                source.step(time_increment)
        
        return self.get_output()
    
    def reset(self):
        """Reset all sources"""
        for source in self.sources:
            if hasattr(source, 'reset'):
                source.reset()
    
    def __str__(self):
        source_name = type(self.sources[self.select_value]).__name__ if self.select_value < len(self.sources) else "None"
        return f"{self.name}: Select={self.select_value}, Source={source_name}, Output={self.get_output()}"

class AnalogToDigitalConverter:
    """
    Simple analog-to-digital converter simulation
    """
    
    def __init__(self, resolution=8, vref=5.0, name="ADC"):
        """
        Initialize ADC
        
        Args:
            resolution (int): ADC resolution in bits
            vref (float): Reference voltage
            name (str): Name of the ADC
        """
        self.resolution = resolution
        self.vref = vref
        self.name = name
        self.max_value = (2 ** resolution) - 1
        
        # Input
        self.analog_input = 0.0
    
    def set_input(self, voltage):
        """Set analog input voltage"""
        self.analog_input = max(0.0, min(self.vref, voltage))
    
    def get_digital_output(self):
        """Get digital output value"""
        # Convert analog to digital
        normalized = self.analog_input / self.vref
        digital_value = int(normalized * self.max_value)
        return digital_value
    
    def get_binary_output(self):
        """Get binary representation as list of bits (MSB first)"""
        digital_value = self.get_digital_output()
        binary = []
        for i in range(self.resolution - 1, -1, -1):
            bit = (digital_value >> i) & 1
            binary.append(bit)
        return binary
    
    def get_output(self):
        """Get digital output (alias)"""
        return self.get_digital_output()
    
    def __str__(self):
        digital = self.get_digital_output()
        binary = ''.join(map(str, self.get_binary_output()))
        return f"{self.name}: {self.analog_input:.2f}V -> {digital} (0b{binary})"
