import pytest
from src.planet_generation.probability import Probability, MinMaxSelector, WeightedSelector, ListSelector, ListMultipleSelector, SingleSelector

RANDOM_TEST_RUNS = 10000

@pytest.fixture
def minmax_prob():
    data = {"min": 1, "max": 3}
    return Probability.create(data=data)

@pytest.fixture
def weighted_prob():
    data = {
        "weights": [25, 25, 50],
        "values": [2, {"min": 1, "max": 3}, [1, 2, 3]]
    }
    return Probability.create(data=data)

@pytest.fixture
def list_prob():
    data = [1, 2, 3]
    return Probability.create(data=data)

@pytest.fixture
def list_multiple():
    data = {
        "values": [1, 2, 3],
        "count": 3
    }
    return Probability.create(data=data)

@pytest.fixture
def single_prob():
    data = 1
    return Probability.create(data=data)

def test_init(minmax_prob: Probability, weighted_prob: Probability, list_prob: Probability, single_prob: Probability):
    assert isinstance(minmax_prob.selector, MinMaxSelector)
    assert minmax_prob.selector.min == 1
    assert minmax_prob.selector.max == 3

    assert isinstance(weighted_prob.selector, WeightedSelector)
    assert weighted_prob.selector.weights == [25, 25, 50]
    assert weighted_prob.selector.values[0] == 2
    assert weighted_prob.selector.values[1].selector.min == 1
    assert weighted_prob.selector.values[1].selector.max == 3
    assert weighted_prob.selector.values[2].selector.values == [1, 2, 3]

    assert isinstance(list_prob.selector, ListSelector)
    assert list_prob.selector.values == [1, 2, 3]

    assert isinstance(single_prob.selector, SingleSelector)
    assert single_prob.selector.value == 1

def test_minmax(minmax_prob: Probability):
    for _ in range(RANDOM_TEST_RUNS):
        random_value = minmax_prob.generate()
        assert random_value >= 1
        assert random_value <= 3

def test_weighted(weighted_prob: Probability):
    for _ in range(RANDOM_TEST_RUNS):
        random_value = weighted_prob.generate()
        assert random_value >= 1
        assert random_value <= 3

def test_list(list_prob: Probability):
    for _ in range(RANDOM_TEST_RUNS):
        random_value = list_prob.generate()
        assert random_value in [1, 2, 3]

def test_list_multiple(list_multiple: Probability):
    for _ in range(RANDOM_TEST_RUNS):
        random_values = list_multiple.generate()
        assert set(random_values) == set([1, 2, 3])

def test_single(single_prob: Probability):
    for _ in range(RANDOM_TEST_RUNS):
        random_value = single_prob.generate()
        assert random_value == 1