# Research Brief: Finite-Speed or Diffusive?

- Status: partial
- Version: 0.1
- Date: 2026-07-26

## Research question

Does a constrained graph telegraph model provide distinguishable and out-of-sample useful evidence of finite-speed global equity volatility transmission relative to graph diffusion and standard time-series baselines?

## Why the answer matters

Connectedness measures quantify directional statistical spillovers and classify modeled net transmitters and receivers. This study asks whether the temporal dynamics contain finite-speed inertia that creates a usable warning interval, or whether delayed diffusion and ordinary persistence explain the same observations.

## Closest literature and contribution delta

The project sits between volatility connectedness, global spillover networks, telegraph-process finance, and graph dynamics. Claim C005 is blocked until the reproducible boundary search is executed, so the contribution is provisional:

> Turn finite-speed versus diffusive propagation into competing spectral, arrival-time, and forecast restrictions rather than a physical metaphor.

## State variable and graph

Separate each market's slowly varying baseline and the contemporaneous global mode:

\[
\mathbf u(t)
=\boldsymbol\mu(t)+g(t)\mathbf 1+\mathbf z(t),
\qquad
\mathbf 1^\top\mathbf z(t)=0.
\]

Define

\[
\mathbf P=\mathbf I-\frac{1}{N}\mathbf 1\mathbf 1^\top,
\qquad
g(t)=\frac{1}{N}\mathbf 1^\top
\bigl[\mathbf u(t)-\boldsymbol\mu(t)\bigr],
\qquad
\mathbf z(t)=\mathbf P
\bigl[\mathbf u(t)-\boldsymbol\mu(t)\bigr].
\]

Here \(\mathbf z(t)\) is the cross-market propagation field, \(g(t)\) is a separately modeled common shock, and \(L\) is the symmetric Laplacian of a fixed, ex ante, connected market-distance graph. This projection prevents a persistent common component from being mislabeled as network equilibrium.

## Competing dynamics

Diffusion:

\[
\dot{\mathbf z}(t)
=-\kappa L\mathbf z(t)+\mathbf P\boldsymbol\varepsilon(t),
\qquad \kappa>0.
\]

Damped graph propagation:

\[
\ddot{\mathbf z}(t)
+\gamma\dot{\mathbf z}(t)
=-c^2L\mathbf z(t)+\mathbf P\boldsymbol\varepsilon(t),
\qquad \gamma,c>0.
\]

For \(L\boldsymbol\phi_k=\lambda_k\boldsymbol\phi_k\) and
\(a_k(t)=\boldsymbol\phi_k^\top\mathbf z(t)\), diffusion implies

\[
a_k(t)=a_k(0)e^{-\kappa\lambda_k t},
\]

whereas the damped model implies

\[
\ddot a_k+\gamma\dot a_k+c^2\lambda_k a_k=0
\]

with roots

\[
r_{k,\pm}
=\frac{-\gamma\pm\sqrt{\gamma^2-4c^2\lambda_k}}{2}.
\]

Oscillation is possible only for modes satisfying
\(\gamma^2<4c^2\lambda_k\). A generic second lag is therefore insufficient evidence; estimated modal timing must cohere with \(\lambda_k\) and the ex ante distance.

The long-run boundary is:

\[
\dot{\mathbf z}
=\ddot{\mathbf z}=0
\quad\Rightarrow\quad
L\mathbf z=0.
\]

For a connected graph, \(\ker L=\operatorname{span}\{\mathbf 1\}\). Together with \(\mathbf 1^\top\mathbf z=0\), the boundary implies \(\mathbf z=0\): cross-market residual differences dissipate, while the separately modeled common mode \(g(t)\) need not vanish. It does not imply that raw market volatilities become equal.

## Identification

Required evidence:

1. simulation recovery under diffusion, damped propagation, delayed diffusion, and flexible VAR data-generating processes;
2. UTC-aligned information sets and separate overnight/intraday measures;
3. ex ante primary distance;
4. first-response and peak-response estimates whose timing increases with distance;
5. modal restrictions tied to graph eigenvalues;
6. out-of-sample comparison with VAR, graph autoregression, and connectedness baselines.

## Falsifiers

Kill or radically reframe the finite-speed claim if:

- aligned data eliminate the distance-arrival relation;
- a delayed-diffusion or unrestricted VAR baseline reproduces every proposed signature;
- modal frequencies do not relate to graph eigenvalues;
- parameter recovery fails under realistic noise and missing-market calendars;
- forecast gains disappear under a common evaluation window;
- the literature search finds the same empirical test already established.

## Scope

The first paper tests model separation in global equity volatility. It does not forecast price direction, claim a universal physical law, or introduce a separate observable Laplace regime.

## Readiness

Conditional. Work may proceed only through the literature, data, and simulation tracer packages. A full empirical paper is blocked until C005 and the sampling-frequency decision are resolved.
