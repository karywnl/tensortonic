# <span style="font-size: 20px;">Arange and Linspace</span>

<span style="font-size: 14px;">Generating sequences of evenly spaced numbers is a fundamental operation in scientific computing. NumPy provides two complementary functions: `np.arange()` generates values with a fixed step size, while `np.linspace()` generates a fixed number of values between endpoints. Choosing the right one depends on whether you care about the step size or the number of points.</span>

---

## <span style="font-size: 16px;">np.arange()</span>

<span style="font-size: 14px;">`np.arange()` is the NumPy equivalent of Python's `range()`. Unlike `range()`, it accepts floating-point arguments. The output dtype is inferred from the inputs: if all of `start`, `stop`, `step` are integers the result is `int64`; if any is a float the result is `float64`. Pass `dtype=` to force a specific type.</span>

```python
np.arange(5)           # [0, 1, 2, 3, 4] - start defaults to 0
np.arange(2, 10)       # [2, 3, 4, 5, 6, 7, 8, 9] - stop is exclusive
np.arange(0, 1, 0.1)   # [0. , 0.1, 0.2, ..., 0.9] - floating-point step
np.arange(10, 0, -2)   # [10, 8, 6, 4, 2] - negative step counts down
```

### <span style="font-size: 14px;">Signature: arange([start,] stop[, step], dtype=None)</span>

* <span style="font-size: 14px;">`start`: Beginning of the interval (default 0)</span>
* <span style="font-size: 14px;">`stop`: End of the interval (exclusive)</span>
* <span style="font-size: 14px;">`step`: Spacing between values (default 1)</span>

<span style="font-size: 14px;">The number of elements is $\lceil(\texttt{stop} - \texttt{start}) / \texttt{step}\rceil$.</span>

### <span style="font-size: 14px;">Floating-Point Warning</span>

<span style="font-size: 14px;">With floating-point steps, the number of elements can be unpredictable due to rounding:</span>

```python
len(np.arange(0, 1, 0.3))    # 4: [0.0, 0.3, 0.6, 0.9]
len(np.arange(0, 1.0, 0.1))  # might be 10 or 11 depending on platform
```

<span style="font-size: 14px;">Because $0.1$ cannot be represented exactly in binary floating point, the accumulated sum may or may not reach $1.0$. For this reason, `np.linspace()` is preferred when you need a specific number of points in an interval.</span>

---

## <span style="font-size: 16px;">np.linspace()</span>

<span style="font-size: 14px;">`np.linspace()` generates a specified number of evenly spaced points between two endpoints. It always returns `float64` by default, regardless of the input types, so no explicit `dtype=` is needed for floating-point output:</span>

```python
np.linspace(0, 1, 5)      # [0.0, 0.25, 0.5, 0.75, 1.0] - 5 points
np.linspace(0, 1, 11)     # [0.0, 0.1, 0.2, ..., 1.0] - 11 points
np.linspace(0, 2*np.pi, 100)  # 100 points around a circle
```

### <span style="font-size: 14px;">Signature: linspace(start, stop, num=50, endpoint=True)</span>

* <span style="font-size: 14px;">`start`: Beginning of the interval</span>
* <span style="font-size: 14px;">`stop`: End of the interval</span>
* <span style="font-size: 14px;">`num`: Number of points (default 50)</span>
* <span style="font-size: 14px;">`endpoint`: Whether to include `stop` (default True)</span>

<span style="font-size: 14px;">The step size is computed as:</span>

$$\texttt{step} = \frac{\texttt{stop} - \texttt{start}}{\texttt{num} - 1} \quad \text{(when endpoint=True)}$$

$$\texttt{step} = \frac{\texttt{stop} - \texttt{start}}{\texttt{num}} \quad \text{(when endpoint=False)}$$

### <span style="font-size: 14px;">Getting the Step Size</span>

```python
values, step = np.linspace(0, 1, 5, retstep=True)
# values: [0.0, 0.25, 0.5, 0.75, 1.0], step: 0.25
```

---

## <span style="font-size: 16px;">arange vs. linspace</span>

| Feature | `arange()` | `linspace()` |
|---------|-----------|-------------|
| Controls | Step size | Number of points |
| Endpoint | Excluded | Included (by default) |
| Floating-point safe | No (rounding issues) | Yes |
| Best for | Integer sequences, known step | Continuous intervals, plotting |

<span style="font-size: 14px;">Rule of thumb: use `arange` for integer sequences and `linspace` for floating-point ranges.</span>

---

## <span style="font-size: 16px;">Logarithmic Spacing: np.logspace()</span>

<span style="font-size: 14px;">`np.logspace()` generates points evenly spaced on a logarithmic scale:</span>

```python
np.logspace(0, 3, 4)   # [1, 10, 100, 1000] = 10^[0, 1, 2, 3]
np.logspace(-2, 2, 5)  # [0.01, 0.1, 1, 10, 100]
```

<span style="font-size: 14px;">This is essential for hyperparameter searches (learning rates, regularization strengths) where the search space spans several orders of magnitude.</span>

---

## <span style="font-size: 16px;">Geometric Spacing: np.geomspace()</span>

```python
np.geomspace(1, 1000, 4)  # [1, 10, 100, 1000]
```

<span style="font-size: 14px;">Similar to `logspace` but takes actual start/stop values instead of exponents. More intuitive when you know the endpoint values.</span>

---

## <span style="font-size: 16px;">Practical Applications</span>

### <span style="font-size: 14px;">Plotting Smooth Curves</span>

```python
x = np.linspace(-5, 5, 1000)
y = np.sin(x) / x  # sinc function
```

### <span style="font-size: 14px;">Grid Generation for Contour Plots</span>

```python
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))
```

### <span style="font-size: 14px;">Time Series Timestamps</span>

```python
t = np.arange(0, 10, 0.01)  # 10 seconds at 100 Hz sampling rate
signal = np.sin(2 * np.pi * 5 * t)  # 5 Hz sine wave
```

### <span style="font-size: 14px;">Hyperparameter Grid</span>

```python
learning_rates = np.logspace(-5, -1, 20)  # 20 rates from 1e-5 to 0.1
```

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**arange with float step**: The number of elements is unpredictable. Use `linspace` instead.</span>
* <span style="font-size: 14px;">**arange stop is exclusive**: `np.arange(0, 5)` gives $[0, 1, 2, 3, 4]$, not $[0, 1, 2, 3, 4, 5]$.</span>
* <span style="font-size: 14px;">**linspace stop is inclusive**: `np.linspace(0, 5, 6)` gives $[0, 1, 2, 3, 4, 5]$. This is different from arange.</span>
* <span style="font-size: 14px;">**logspace base**: Default base is 10. For base-2 logarithmic spacing, pass `base=2`.</span>