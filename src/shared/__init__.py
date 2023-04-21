from .paths import *


from enum import Enum, auto


class Aggregator(Enum):
    SUM = "sum"
    AVERAGE = "average"


class Functions(Enum):
    MULTIPLE_DOT_PRODUCT = "multiple_dot_product"
    SIMPLE_DOT_PRODUCT = "simple_dot_product"
