# Pulse 02: Bounded Correlated Agents

## Result

Implemented a factor sampler with explicit residual variance and zero-to-one
clipping. All 14 traits match the V1 schema, all loading sums remain within unit
variance, seeds reproduce, and declared signs pass on 30,000 validation draws.

V2 changes within-archetype dependence without changing mixture labels or
weights. It generates no protected-group attributes.
