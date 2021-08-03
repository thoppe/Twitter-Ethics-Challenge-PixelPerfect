# Twitter Ethics Challenge: Pixel Perfect
Submission to Twitter's algorithmic bias bounty challenge

## Abstract

## Self-score

+ **Type of Harm**
+ **Damage or impact**
+ **Affected users**
+ **Likelihood only graded for unintentional harms**
+ **Exploitability only graded for intentional harms:**
+ **Justification:**
+ **Clarity of contribution:**

Final score: (TBD)

Images and demographic data provided by Civil Service USA and can be found at the following locations:

+ https://github.com/CivilServiceUSA/us-house
+ https://github.com/CivilServiceUSA/us-senate
+ Additional information for the [117th US Congress](https://www.congress.gov/members?q=%7B%22congress%22%3A%5B%22117%22%5D%7D&pageSize=250&page=1)


Useful links about the submission:
+ [Challenge blog post](https://blog.twitter.com/engineering/en_us/topics/insights/2021/algorithmic-bias-bounty-challenge)
+ [Hacker One entry point](https://hackerone.com/twitter-algorithmic-bias?type=team)
+ [Crop code on github](https://github.com/twitter-research/image-crop-analysis)
+ [arXiv paper](https://arxiv.org/pdf/2105.08667.pdf)

## Lessons

+ Model is easily fooled by typographical attacks
+ Grid discretization is _very_ important when images are similar
+ For this dataset 0.150 of all pairwise combinations fail on the grid [0, 5, 10, 15, 20, 25] from [0, 30] range

Raw win table of "wins" reflect previous results found in Yee et. all: gender plays a strong role (towards females), while the role of ethnicity matters, but in a more subtle way. (p-values are constructed from a two-sided binomial test using the sample mean as the expected value, significance is p<0.01 provided for convenience only).

```
            key        n       k       pct         pvalue
3    white_male  1746180  756856  0.433435   0.000000e+00
1    other_male   357780  187102  0.522953  5.096083e-166
2  white_female   501960  318871  0.635252   0.000000e+00
0  other_female   250980  165621  0.659897   0.000000e+00
```

Reflecting the gender and ethnicity parity in the party structure we see the same result:

```
           key        n       k       pct  pvalue
1  independent    10680    3260  0.305243     0.0
2   republican  1393740  636249  0.456505     0.0
0     democrat  1452480  788941  0.543168     0.0
```


Considering the interaction table, the largest difference is between white males and females. For non-white males the bias still exists, but is less. N reflects not only each pairwise interaction but at all levels of offset.

```
        left_key     right_key       n       k       pct         pvalue    sig
12    white_male  other_female   76845   21488  0.279628   0.000000e+00   True
14    white_male  white_female  153690   47347  0.308068   0.000000e+00   True
4     other_male  other_female   15745    5895  0.374405  1.459034e-243   True
6     other_male  white_female   31490   12577  0.399397  1.563426e-318   True
13    white_male    other_male  109545   45455  0.414944   0.000000e+00   True
8   white_female  other_female   22090   10886  0.492802   4.166236e-05   True
5     other_male    other_male   22110   11100  0.502035   1.764122e-01  False
15    white_male    white_male  533010  269030  0.504737   6.682066e-03   True
10  white_female  white_female   43710   22357  0.511485   4.109529e-02  False
0   other_female  other_female   10810    5559  0.514246   1.124878e-01  False
2   other_female  white_female   22090   11800  0.534178   2.448903e-16   True
7     other_male    white_male  109545   64823  0.591748   0.000000e+00   True
9   white_female    other_male   31490   19510  0.619562   0.000000e+00   True
1   other_female    other_male   15745   10118  0.642617  3.239905e-259   True
11  white_female    white_male  153690  109219  0.710645   0.000000e+00   True
3   other_female    white_male   76845   56482  0.735012   0.000000e+00   True
```

Considering the side, the baseline is 0.15. This means that 15% of the image pairs are exploitable. The breakdown along demographics show that there is a difference with non-white females and white female from this expected 15%. N reflects only the pairwise 

```
           key       n      k       pct        pvalue    sig
2  white_female  100392  14504  0.144474  1.443650e-06   True
1    other_male   71556  10686  0.149338  6.868004e-01  False
3    white_male  349236  52319  0.149810  9.056615e-01  False
0  other_female   50196   8131  0.161985  5.644320e-14   True
```

```
        left_key     right_key       n      k       pct        pvalue    sig
11  white_female    white_male   30738   4048  0.131694  1.091725e-19   True
14    white_male  white_female   30738   4158  0.135272  3.753454e-13   True
5     other_male    other_male    4422    627  0.141791  1.347533e-01  False
6     other_male  white_female    6298    924  0.146713  4.912329e-01  False
13    white_male    other_male   21909   3226  0.147245  2.764780e-01  False
9   white_female    other_male    6298    936  0.148619  7.912084e-01  False
3   other_female    white_male   15369   2305  0.149977  9.729596e-01  False
7     other_male    white_male   21909   3304  0.150806  6.980259e-01  False
12    white_male  other_female   15369   2332  0.151734  5.195537e-01  False
15    white_male    white_male  106602  16473  0.154528  2.334934e-05   True
10  white_female  white_female    8742   1390  0.159003  1.791791e-02  False
1   other_female    other_male    3149    517  0.164179  2.627735e-02  False
4     other_male  other_female    3149    525  0.166720  8.759193e-03   True
0   other_female  other_female    2162    397  0.183626  1.849644e-05   True
2   other_female  white_female    4418    818  0.185152  1.858144e-10   True
8   white_female  other_female    4418    840  0.190131  3.868877e-13   True
```

Need to collapse this table...
