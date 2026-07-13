"""Bounded factor sampler for Voter Lab v2."""

import math


def sample_traits(rng, archetype, traits, correlation_model):
    factors = [rng.gauss(0.0, 1.0) for _ in correlation_model["factors"]]
    values = []
    for trait, mean in zip(traits, archetype["means"]):
        loadings = correlation_model["loadings"][trait]
        residual_scale = math.sqrt(max(0.0, 1.0 - sum(value * value for value in loadings)))
        shock = sum(loading * factor for loading, factor in zip(loadings, factors))
        shock += residual_scale * rng.gauss(0.0, 1.0)
        values.append(min(1.0, max(0.0, mean + archetype["sd"] * shock)))
    return values
