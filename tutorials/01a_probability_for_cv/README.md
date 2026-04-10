# 01a: Probability for Computer Vision

Extracted from `../01a_probability_for_computer_vision.ipynb`. Each part is a paired `.md` (theory) + `.py` (runnable code) file covering one concept in the distribution chain: Bernoulli → Binomial → Poisson → Normal → CLT → full sensor model.

## Parts

| File pair | Description |
|-----------|-------------|
| `part0_what_is_a_distribution` | Why averages are not enough; PMF vs PDF; histogram convergence; parameter compression |
| `part1_bernoulli` | The Bernoulli trial as the atom of randomness; QE as a Bernoulli probability |
| `part2_binomial` | Counting successes in n trials; PMF built term by term; shape vs n and p; Monte Carlo validation |
| `part3_poisson` | Binomial limit as n→∞, p→0; shot noise derivation; σ=√λ property; three noise regimes introduction |
| `part4_normal` | The bell curve and its two parameters; Poisson→Normal convergence as λ grows |
| `part5_clt` | Central Limit Theorem: any distribution becomes Gaussian when summed; KS convergence rate |
| `part6_putting_it_together` | Full sensor simulation (photons→ADC); signal chain visualization; three noise regimes; gradient image capture |
| `exercises` | Four practice problems: Binomial/Poisson convergence rate, Anscombe transform, noise budget, CLT skewness |

## Running

Each `.py` file is standalone:

```bash
python part0_what_is_a_distribution.py
python part1_bernoulli.py
python part2_binomial.py
python part3_poisson.py
python part4_normal.py
python part5_clt.py
python part6_putting_it_together.py
python exercises.py   # stub — complete the exercises first
```

The cameraman image path is set relative to this folder:
`../../DIP3E_Original_Images_CH02/Fig0222(b)(cameraman).tif`
