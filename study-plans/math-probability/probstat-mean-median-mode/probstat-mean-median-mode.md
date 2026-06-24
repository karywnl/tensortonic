## <span style="font-size: 20px;">Mean, Median, and Mode</span>

The three **measures of central tendency** summarize a dataset with a single representative value. Each captures a different notion of "center," and choosing the right one depends on data distribution and the problem at hand.

---

## Definitions and Formulas

**Mean (Arithmetic Average):**

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

The mean is the balance point of the data - if the dataset were placed on a number line, the mean is where it would balance perfectly. It uses every data point, making it sensitive to all values.

**Median:**

The median is the middle value when data is sorted. For $n$ observations:

$$\text{median} = \begin{cases} x_{(n+1)/2} & \text{if } n \text{ is odd} \\ \frac{x_{n/2} + x_{n/2+1}}{2} & \text{if } n \text{ is even} \end{cases}$$

The median divides the sorted data into two equal halves. It depends only on rank order, not magnitude, making it robust to outliers.

**Mode:**

The mode is the value that appears most frequently:

$$\text{mode} = \arg\max_{v} \text{count}(x_i = v)$$

A dataset can be unimodal (one mode), bimodal (two modes), or multimodal. The mode is the only measure applicable to categorical data.

---

## Intuition: When to Use Each

| Measure | Best for | Weakness |
|---------|----------|----------|
| Mean | Symmetric, outlier-free data | Pulled by extreme values |
| Median | Skewed data, ordinal scales | Ignores magnitude of values |
| Mode | Categorical data, finding peaks | May not exist or be unique |

Consider household incomes: a few billionaires inflate the mean dramatically, but the median remains stable. This is why economic reports often prefer the median.

---

## Relationship in Skewed Distributions

For unimodal distributions, the three measures relate to skewness:

- **Right-skewed** (positive skew): $\text{mode} < \text{median} < \text{mean}$
- **Symmetric**: $\text{mean} = \text{median} = \text{mode}$
- **Left-skewed** (negative skew): $\text{mean} < \text{median} < \text{mode}$

An empirical approximation (Pearson's rule) states: $\text{mean} - \text{mode} \approx 3(\text{mean} - \text{median})$.

---

## Properties

- The mean minimizes the sum of squared deviations: $\bar{x} = \arg\min_c \sum(x_i - c)^2$
- The median minimizes the sum of absolute deviations: $\text{median} = \arg\min_c \sum|x_i - c|$
- The mean is a linear operator: $\text{mean}(ax + b) = a \cdot \text{mean}(x) + b$
- Adding a constant shifts all three measures by that constant
- Multiplying by a constant scales all three measures by that constant

---

## Applications in Machine Learning

**Data Exploration:** Comparing mean and median reveals skewness without plotting - a large gap suggests outliers or heavy tails.

**Imputation of Missing Values:** Mean imputation preserves the overall average but can distort variance. Median imputation is preferred for skewed features. Mode imputation is standard for categorical columns.

**Feature Engineering:** Replacing raw values with deviations from the mean (centering) is a prerequisite for PCA and many linear models. Group-level means or medians serve as powerful aggregate features.

**Loss Functions:** Mean Squared Error (MSE) minimization yields the conditional mean. Mean Absolute Error (MAE) minimization yields the conditional median - more robust for noisy targets. The mode corresponds to the maximum of the predicted density.

**Anomaly Detection:** Observations far from the median (in terms of MAD - median absolute deviation) are candidate anomalies. This is more robust than using mean and standard deviation.

**Weighted Variants:** In many ML contexts, observations carry different weights. The weighted mean is $\bar{x}_w = \sum w_i x_i / \sum w_i$. This arises naturally in kernel density estimation, attention mechanisms, and boosting algorithms where misclassified samples receive higher weight.

---

## Common Pitfalls

- **Mean of ratios vs ratio of means:** $\text{mean}(a_i/b_i) \neq \text{mean}(a_i)/\text{mean}(b_i)$. This distinction matters when averaging percentages, rates, or normalized metrics across groups of different sizes.
- **Simpson's paradox:** A trend that appears in several groups can reverse when the groups are combined. Always check whether aggregation obscures group-level patterns.
- **Multimodal data:** When data has multiple clusters, none of the three measures may represent any cluster well. Always visualize before summarizing.