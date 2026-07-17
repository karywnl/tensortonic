# <span style="font-size: 20px;">Mutation Trap</span>

<span style="font-size: 14px;">NumPy's view mechanism is a powerful performance optimization: slicing an array returns a view that shares memory with the original, avoiding expensive data copies. However, this shared memory means that modifying a view also modifies the original array - a behavior that catches many programmers by surprise. Understanding when NumPy creates views versus copies is essential for writing correct code.</span>

---

## <span style="font-size: 16px;">Views: Shared Memory</span>

<span style="font-size: 14px;">Basic indexing (slicing) returns a view:</span>

```python
a = np.array([1, 2, 3, 4, 5])
b = a[1:4]       # b is a VIEW of a
b[0] = 99        # modifies a[1] as well!
print(a)          # [1, 99, 3, 4, 5]
```

<span style="font-size: 14px;">The view $b$ does not own its data; it points to the same memory as $a$. Any modification to $b$ is immediately visible in $a$.</span>

### <span style="font-size: 14px;">Operations That Return Views</span>

* <span style="font-size: 14px;">**Slicing**: `a[1:4]`, `a[:, 0]`, `a[::2]`</span>
* <span style="font-size: 14px;">**Reshape** (when contiguous): `a.reshape(2, 3)`</span>
* <span style="font-size: 14px;">**Transpose**: `a.T`</span>
* <span style="font-size: 14px;">**ravel** (when contiguous): `a.ravel()`</span>
* <span style="font-size: 14px;">**np.newaxis**: `a[:, np.newaxis]`</span>

---

## <span style="font-size: 16px;">Copies: Independent Memory</span>

<span style="font-size: 14px;">Some operations return copies - independent arrays with their own memory:</span>

* <span style="font-size: 14px;">**Fancy indexing**: `a[[0, 2, 4]]`</span>
* <span style="font-size: 14px;">**Boolean indexing**: `a[a > 3]`</span>
* <span style="font-size: 14px;">**flatten()**: `a.flatten()`</span>
* <span style="font-size: 14px;">**Explicit copy**: `a.copy()`</span>
* <span style="font-size: 14px;">**np.array()**: `np.array(a)`</span>

```python
a = np.array([1, 2, 3, 4, 5])
b = a[[0, 2, 4]]   # copy (fancy indexing)
b[0] = 99           # does NOT modify a
print(a)             # [1, 2, 3, 4, 5] - unchanged
```

---

## <span style="font-size: 16px;">Detecting Views</span>

```python
b = a[1:4]
b.base is a         # True: b is a view of a
b.flags.owndata     # False: b does not own its data

c = a.copy()
c.base is a         # False (or None)
c.flags.owndata     # True: c owns its data
```

---

## <span style="font-size: 16px;">The Row Extraction Trap</span>

<span style="font-size: 14px;">A common pattern that leads to unintended mutation:</span>

```python
data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])

row = data[1]     # VIEW of row 1
row[:] = 0        # modifies data[1] to [0, 0, 0]!
```

<span style="font-size: 14px;">To safely extract a row without affecting the original:</span>

```python
row = data[1].copy()  # independent copy
row[:] = 0            # data[1] unchanged
```

---

## <span style="font-size: 16px;">The Clipping Trap</span>

<span style="font-size: 14px;">`np.clip` with `out` parameter can mutate in-place:</span>

```python
a = np.array([1, 5, 10, 15])
clipped = np.clip(a, 3, 12)      # new array: [3, 5, 10, 12]
np.clip(a, 3, 12, out=a)         # in-place: a is now [3, 5, 10, 12]
```

<span style="font-size: 14px;">Without `out`, clip returns a new array. With `out=a`, it modifies the original. Many NumPy functions support the `out` parameter for in-place operation.</span>

---

## <span style="font-size: 16px;">Function Argument Mutation</span>

<span style="font-size: 14px;">Passing arrays to functions can lead to unintended mutation if the function modifies slices:</span>

```python
def process(arr):
    subset = arr[0:5]   # view!
    subset *= 2          # modifies original arr
    return subset

original = np.arange(10)
result = process(original)
# original is now [0, 2, 4, 6, 8, 5, 6, 7, 8, 9]
```

<span style="font-size: 14px;">Defensive programming: copy inputs at the start of functions that modify data:</span>

```python
def process(arr):
    arr = arr.copy()     # defensive copy
    subset = arr[0:5]
    subset *= 2
    return arr
```

---

## <span style="font-size: 16px;">In-Place Operations</span>

<span style="font-size: 14px;">Augmented assignment operators (`+=`, `*=`, etc.) modify arrays in-place:</span>

```python
a = np.array([1, 2, 3])
b = a            # b points to same array
a += 10          # modifies a IN-PLACE
print(b)          # [11, 12, 13] - b also affected

a = a + 10       # creates NEW array, rebinds a
print(b)          # [11, 12, 13] - b points to old array
```

<span style="font-size: 14px;">`a += 10` modifies the existing array. `a = a + 10` creates a new array and reassigns the variable name. This distinction is subtle but critical.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Slicing returns views**: Any modification to a slice modifies the original. Use `.copy()` when independence is needed.</span>
* <span style="font-size: 14px;">**+= vs. = ... +**: Augmented assignment is in-place; regular assignment creates a new array.</span>
* <span style="font-size: 14px;">**Function arguments**: Arrays passed to functions can be mutated through views. Copy defensively.</span>
* <span style="font-size: 14px;">**Reshape views**: `a.reshape(...)` may return a view. Modifying the reshaped array may modify the original.</span>