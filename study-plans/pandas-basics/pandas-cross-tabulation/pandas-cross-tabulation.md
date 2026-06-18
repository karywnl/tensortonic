# <span style="font-size: 20px;">Cross Tabulation</span>

<span style="font-size: 14px;">Cross tabulation (crosstab) computes a frequency table showing how often each combination of two categorical variables occurs. It is the fundamental tool for understanding relationships between categorical variables: what proportion of customers in each region use each payment method, how error types distribute across services, or whether survey responses differ by demographic group.</span>

---

## <span style="font-size: 16px;">The crosstab() Function</span>

```python
pd.crosstab(df['department'], df['gender'])
```

<span style="font-size: 14px;">This produces a matrix where rows are departments, columns are genders, and cells contain the count of rows matching each combination. Unlike `pivot_table()`, `crosstab()` takes Series (not column names), and its default aggregation is count (not mean).</span>

---

## <span style="font-size: 16px;">Basic Frequency Table</span>

```python
ct = pd.crosstab(df['product'], df['region'])
# region      East  North  South  West
# product
# Widget        45     32     28    39
# Gadget        52     41     35    48
# Doohickey     31     25     22    29
```

<span style="font-size: 14px;">Each cell shows how many rows have that (product, region) combination. The total count across all cells equals the number of rows in the original DataFrame (assuming no NaN in the cross-tabulated columns).</span>

---

## <span style="font-size: 16px;">Normalization</span>

<span style="font-size: 14px;">The `normalize` parameter converts counts to proportions:</span>

```python
pd.crosstab(df['product'], df['region'], normalize=True)     # all cells sum to 1
pd.crosstab(df['product'], df['region'], normalize='index')  # rows sum to 1
pd.crosstab(df['product'], df['region'], normalize='columns') # columns sum to 1
```

* <span style="font-size: 14px;">`normalize=True`: Each cell shows its proportion of the grand total.</span>
* <span style="font-size: 14px;">`normalize='index'`: Each row sums to 1. Shows the distribution across regions for each product.</span>
* <span style="font-size: 14px;">`normalize='columns'`: Each column sums to 1. Shows the distribution across products for each region.</span>

---

## <span style="font-size: 16px;">Margins</span>

```python
pd.crosstab(df['product'], df['region'], margins=True, margins_name='Total')
```

<span style="font-size: 14px;">Adds row and column totals. Combined with normalization, margins show marginal probabilities.</span>

---

## <span style="font-size: 16px;">Custom Aggregation</span>

<span style="font-size: 14px;">Like `pivot_table()`, `crosstab()` supports custom aggregation via `values` and `aggfunc`:</span>

```python
pd.crosstab(df['department'], df['quarter'],
            values=df['revenue'], aggfunc='sum')
```

<span style="font-size: 14px;">This computes the sum of revenue for each (department, quarter) combination instead of counting occurrences.</span>

---

## <span style="font-size: 16px;">Multiple Levels</span>

```python
pd.crosstab([df['region'], df['department']], df['quarter'])
```

<span style="font-size: 14px;">Passing a list creates a MultiIndex along that axis. This is useful for nested categorizations.</span>

---

## <span style="font-size: 16px;">crosstab vs. pivot_table vs. value_counts</span>

| Function | Default agg | Input | Best for |
|----------|------------|-------|----------|
| `crosstab()` | count | Series | Frequency tables of two categorical variables |
| `pivot_table()` | mean | DataFrame + column names | General summarization |
| `value_counts()` | count | Series | Frequency of a single variable |

<span style="font-size: 14px;">`crosstab()` is syntactic sugar: `pd.crosstab(s1, s2)` is equivalent to `pd.pivot_table(df, index=s1, columns=s2, aggfunc='size')`. Use whichever reads more clearly.</span>

---

## <span style="font-size: 16px;">Statistical Tests</span>

<span style="font-size: 14px;">Cross tabulations are the input for chi-squared tests of independence:</span>

```python
from scipy.stats import chi2_contingency
ct = pd.crosstab(df['treatment'], df['outcome'])
chi2, p, dof, expected = chi2_contingency(ct)
```

<span style="font-size: 14px;">If $p < 0.05$, the variables are statistically dependent. The expected frequencies from the test can be compared to the observed crosstab to identify which cells deviate most.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**NaN exclusion**: By default, `crosstab()` excludes NaN values. Pass `dropna=False` to include them as a category.</span>
* <span style="font-size: 14px;">**Sparse tables**: If the two variables have many unique values, the crosstab becomes very large with many zeros. Consider binning continuous variables first.</span>
* <span style="font-size: 14px;">**Confusing normalization directions**: `normalize='index'` makes rows sum to 1; `normalize='columns'` makes columns sum to 1. Mixing these up reverses the interpretation.</span>
* <span style="font-size: 14px;">**Input must be Series**: Unlike `pivot_table()`, `crosstab()` takes Series objects, not column names. Pass `df['col']`, not `'col'`.</span>