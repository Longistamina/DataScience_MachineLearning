'''
Callback into the Python Interpreter from within JIT'ed code using ``objmode``.

There are rare but real cases when a ``nopython``-mode function needs to callback
into the Python interpreter to invoke code that Numba cannot compile.

Common use cases include:
+ Logging progress for long-running JIT'ed functions.
+ Using data structures not currently supported by Numba (e.g., complex custom classes, certain Pandas operations).
+ Debugging inside JIT'ed code using the Python debugger (pdb).

WARNING: Callbacks are EXPENSIVE. They require:
1. Acquiring the GIL (Global Interpreter Lock).
2. Converting native C-types back to Python objects.
3. Executing the Python code.
4. Converting return values back to native C-types.
5. Releasing the GIL.
=> Do NOT use ``objmode`` on performance-critical inner loops!
'''

from numba import njit, objmode, types
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


# =========================================================================================
# 1. The Core Concept: Basic Callback
# =========================================================================================
'''
Sometimes you just want to execute standard Python code, like printing a formatted
string or interacting with an unsupported library, without needing to return
new variables back to the nopython scope.
'''

def python_only_function(text):
    """A pure Python function that Numba cannot compile."""
    print(f"[Python Interpreter] {text}")

@njit
def basic_callback_example():
    x = 10
    y = 20
    # Enter object mode
    with objmode():
        python_only_function(f"Calculating sum of {x} and {y}...")

    return x + y

print("--- 1. Basic Callback ---")
res = basic_callback_example()
print(f"Result from nopython mode: {res}\n")
# --- 1. Basic Callback ---
# [Python Interpreter] Calculating sum of 10 and 20...
# Result from nopython mode: 30


# =========================================================================================
# 2. Returning Values & Type Annotation (String & Types)
# =========================================================================================
'''
If the Python code generates data that you need back in your fast ``nopython`` code,
you must declare the output variables and their expected Numba types as keyword
arguments to ``objmode()``.

Types can be specified as:
1. Strings representing the type (e.g., 'float64', 'intp[:]')
2. Compile-time bound global/nonlocal variables (e.g., numba.types.intp[:])
'''

def bar(x):
    """A pure Python function using unsupported operations (list reversal)."""
    # This code is executed by the interpreter.
    return np.asarray(list(reversed(x.tolist())))

# Output type as a global variable (read at compile time)
out_ty = types.intp[:]

@njit
def returning_values_example():
    x = np.arange(5, dtype=np.intp)
    y = np.zeros_like(x)

    # Annotate return types for 'y' and 'z'
    # The variable names inside objmode() MUST match the local variables you want to overwrite/create.
    with objmode(y='intp[:]', z=out_ty):
        # this region is executed by object-mode.
        y += bar(x)
        z = y * 2  # Create a new variable 'z' to return to nopython mode

    # Back in nopython mode, y and z are native fast arrays
    return y, z

print("--- 2. Returning Values ---")
res_y, res_z = returning_values_example()
print(f"y: {res_y}")
print(f"z: {res_z}\n")
# --- 2. Returning Values ---
# y: [4 3 2 1 0]
# z: [8 6 4 2 0]


# =========================================================================================
# 3. Real-World Use Case: Logging Progress
# =========================================================================================
'''
A very common use case for ``objmode`` is logging the progress of a long-running
simulation or loop without breaking out of the JIT-compiled function.
'''

# 1. Move the logging logic to a pure Python function
def log_progress(i, steps, acc):
    pct = (i / steps) * 100
    # The f-string with format specifiers lives here, safely away from Numba's parser
    logging.info(f"Simulation {pct:.0f}% complete. Current acc: {acc:.2f}")

@njit
def long_running_simulation(steps):
    acc = 0.0
    for i in range(steps):
        # Heavy math (simulated)
        acc += np.sqrt(i)

        # Log progress every 20%
        if i % (steps // 5) == 0 and i > 0:
            with objmode():
                # Numba only sees a standard function call here, which is fully supported.
                # Numba will automatically convert 'i', 'steps', and 'acc' back to
                # Python objects before passing them to log_progress.
                log_progress(i, steps, acc)

    return acc

print("--- 3. Logging Progress ---")
# Note: In a real scenario, steps would be much larger.
final_acc = long_running_simulation(1000000)

# This f-string is OUTSIDE the @njit function, so it is executed by normal Python
# and will not trigger the Numba bytecode error.
print(f"Final accumulated value: {final_acc:.2f}\n")
# INFO: Simulation 20% complete. Current acc: 59628702.80
# INFO: Simulation 40% complete. Current acc: 168655124.56
# INFO: Simulation 60% complete. Current acc: 309839054.79
# INFO: Simulation 80% complete. Current acc: 477028282.21
# --- 3. Logging Progress ---
# Final accumulated value: 666666166.46


# =========================================================================================
# 4. Limitations & Performance Warning
# =========================================================================================
'''
KNOWN LIMITATIONS of the ``with objmode():`` block:
1. Cannot use incoming Python `list` or `dict` objects directly from nopython scope.
2. Cannot use incoming Python function objects.
3. Cannot use control flow that exits the block immediately (`yield`, `break`, `return`, `raise`).
4. Cannot contain nested `with` statements.
5. Random Number Generator (RNG) states do NOT synchronize between nopython and object mode.

PERFORMANCE OVERHEAD DEMONSTRATION:
Calling ``objmode`` inside a tight loop will destroy performance due to GIL acquisition
and type conversion overhead.
'''

@njit
def bad_performance_example(N):
    acc = 0
    for i in range(N):
        # TERRIBLE IDEA: Calling objmode inside a tight loop!
        # with objmode():
        #     acc += i  # This would be incredibly slow
        acc += i # Fast nopython way
    return acc

print("--- 4. Performance Note ---")
print("Never put `with objmode():` inside a tight inner loop.")
print("Only use it for outer-loop logging, setup, or teardown phases.")
