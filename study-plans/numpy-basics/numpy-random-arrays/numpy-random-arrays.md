# <span style="font-size: 20px;">Random Array Generation</span>

<span style="font-size: 14px;">Random number generation is essential for initializing neural network weights, creating synthetic datasets, implementing stochastic algorithms, and running Monte Carlo simulations. NumPy's random module provides a comprehensive set of probability distributions and sampling functions. The modern API (`np.random.default_rng()`) uses the PCG64 generator by default, which has excellent statistical properties and performance.</span>

---

## <span style="font-size: 16px;">The Modern Generator API</span>

```python
rng = np.random.default_rng(seed=42)
```

<span style="font-size: 14px;">This creates a `Generator` instance with a specific seed for reproducibility. All random operations should use this generator rather than the legacy `np.random` module functions.</span>

### <span style="font-size: 14px;">Uniform Distribution</span>

```python
rng.random((3, 4))           # uniform [0, 1), shape (3, 4)
rng.uniform(low=2, high=5, size=(3, 4))  # uniform [2, 5)
```

### <span style="font-size: 14px;">Normal (Gaussian) Distribution</span>

```python
rng.standard_normal((3, 4))              # mean=0, std=1
rng.normal(loc=10, scale=2, size=(3, 4)) # mean=10, std=2
```

### <span style="font-size: 14px;">Integer Sampling</span>

```python
rng.integers(low=0, high=10, size=(3, 4))  # integers in [0, 10)
rng.integers(0, 10, size=5, endpoint=True) # integers in [0, 10]
```

---

## <span style="font-size: 16px;">Reproducibility with Seeds</span>

<span style="font-size: 14px;">A seed initializes the random number generator to a specific state, producing the same sequence of numbers every time:</span>

```python
rng1 = np.random.default_rng(42)
rng2 = np.random.default_rng(42)
assert np.array_equal(rng1.random(5), rng2.random(5))  # identical
```

<span style="font-size: 14px;">Seeds are critical for:</span>

* <span style="font-size: 14px;">**Debugging**: Reproduce the exact same random state that caused a bug</span>
* <span style="font-size: 14px;">**Testing**: Deterministic tests that do not depend on randomness</span>
* <span style="font-size: 14px;">**Experiments**: Reproducible results for scientific papers</span>

---

## <span style="font-size: 16px;">Probability Distributions</span>

<span style="font-size: 14px;">NumPy supports a wide range of distributions:</span>

| Distribution | Method | Parameters |
|-------------|--------|------------|
| Uniform | `rng.uniform(a, b)` | $[a, b)$ interval |
| Normal | `rng.normal(mu, sigma)` | Mean $\mu$, std $\sigma$ |
| Exponential | `rng.exponential(scale)` | Rate $1/\lambda$ |
| Poisson | `rng.poisson(lam)` | Rate $\lambda$ |
| Binomial | `rng.binomial(n, p)` | Trials $n$, probability $p$ |
| Beta | `rng.beta(a, b)` | Shape parameters $\alpha, \beta$ |
| Gamma | `rng.gamma(shape, scale)` | Shape $k$, scale $\theta$ |
| Dirichlet | `rng.dirichlet(alpha)` | Concentration $\alpha$ |

---

## <span style="font-size: 16px;">Shuffling and Permutation</span>

```python
a = np.array([1, 2, 3, 4, 5])

rng.shuffle(a)           # in-place shuffle
b = rng.permutation(a)   # returns shuffled copy

# Permutation of integers (useful for index shuffling)
indices = rng.permutation(100)  # random order of 0-99
```

<span style="font-size: 14px;">`shuffle` modifies the array in-place. `permutation` returns a new array. For shuffling training data indices, `permutation` is safer because it does not modify the original.</span>

---

## <span style="font-size: 16px;">Sampling Without Replacement</span>

```python
rng.choice(10, size=3, replace=False)      # 3 unique values from 0-9
rng.choice(['a', 'b', 'c'], size=2, replace=False)  # 2 unique elements
rng.choice(10, size=3, p=[0.5, 0.1, 0.1, 0.1, 0.05, 0.05, 0.03, 0.03, 0.02, 0.02])
```

<span style="font-size: 14px;">The `p` parameter specifies selection probabilities, useful for weighted sampling.</span>

---

## <span style="font-size: 16px;">Machine Learning Applications</span>

### <span style="font-size: 14px;">Weight Initialization</span>

```python
# Xavier/Glorot initialization
fan_in, fan_out = 784, 256
W = rng.normal(0, np.sqrt(2.0 / (fan_in + fan_out)), (fan_in, fan_out))

# He initialization (for ReLU)
W = rng.normal(0, np.sqrt(2.0 / fan_in), (fan_in, fan_out))
```

### <span style="font-size: 14px;">Train/Test Split</span>

```python
n = len(X)
indices = rng.permutation(n)
split = int(0.8 * n)
train_idx, test_idx = indices[:split], indices[split:]
```

### <span style="font-size: 14px;">Data Augmentation</span>

```python
noise = rng.normal(0, 0.01, X.shape)
X_augmented = X + noise
```

---

## <span style="font-size: 16px;">Legacy API vs. Modern API</span>

<span style="font-size: 14px;">The legacy API uses module-level functions:</span>

```python
# Legacy (avoid in new code):
np.random.seed(42)
np.random.rand(3, 4)
np.random.randn(3, 4)
np.random.randint(0, 10, size=5)

# Modern (preferred):
rng = np.random.default_rng(42)
rng.random((3, 4))
rng.standard_normal((3, 4))
rng.integers(0, 10, size=5)
```

<span style="font-size: 14px;">The modern API is preferred because it avoids global state (`np.random.seed` affects all code in the process) and uses a better default algorithm (PCG64 vs. Mersenne Twister).</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Global seed pollution**: `np.random.seed()` sets global state that affects all random operations. Use `default_rng()` for isolated, reproducible generators.</span>
* <span style="font-size: 14px;">**Forgetting the seed**: Without a seed, results change every run, making debugging impossible.</span>
* <span style="font-size: 14px;">**Confusing rand/randn**: Legacy `rand` is uniform [0,1); legacy `randn` is standard normal. The modern API uses clearer names: `random` and `standard_normal`.</span>
* <span style="font-size: 14px;">**Shape as tuple vs. separate args**: Modern API uses `rng.random((3, 4))` with a tuple. Legacy used `np.random.rand(3, 4)` with separate args. Mixing these causes errors.</span>