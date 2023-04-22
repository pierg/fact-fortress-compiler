from .risk_score_analysis import multi_dot_product_average


d1 = [
    2,
    1,
    0,
    2,
    1,
    1,
    1,
    2,
]
d2 = [
    27,
    55,
]

d1_shape = (2, 4)
d2_shape = (2, 1)

# Sohould return 109


res = multi_dot_product_average(d1, d1_shape, d2)

print(res)
