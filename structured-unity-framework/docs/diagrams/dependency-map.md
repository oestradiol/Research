# Dependency Map (diagram spec)

**Non-circularity (intent)**

- Structural Phenomenology grounds the epistemic starting point
- Informational Awareness Framework extends structural description without replacing givenness
- Unity Dynamics Framework adds `I`, `C`, `L`, and `U` at explicit `(tau, sigma)`
- Framework Interface keeps claims typed and layered
- Research Program instantiates the route design and methods bundle
- Literature Guide routes source support
- Applications Atlas exposes bounded demonstrated routes and exploratory extension nodes

```mermaid
flowchart TD
  SP[Structural Phenomenology] --> IAF[Informational Awareness Framework]
  IAF --> UDF[Unity Dynamics Framework]
  UDF --> RP[Research Program]
  SP --> FI[Framework Interface]
  IAF --> FI
  UDF --> FI
  LG[Literature Guide] -. supports .-> SP
  LG -. supports .-> IAF
  LG -. supports .-> UDF
  LG -. supports .-> FI
  LG -. supports .-> RP
  RP --> APP[Applications Atlas]
  APP --> DR[Demonstrated Routes]
  APP --> RM[Research Map]
```

**What does not justify what**

- phenomenology literature does not automatically support full operational claims
- methods do not replace layer separation
- applications do not prove universal framework truth
