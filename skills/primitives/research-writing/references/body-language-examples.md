# Academic body and technical companion

Apply these examples to manuscript prose, tables and captions. They illustrate the boundary, not a mandated wording or a ban on scientific detail.

| Leaks implementation into the body | Disciplinary replacement | Technical companion retains |
|---|---|---|
| `prepare_data.py` reads `extra-rows`, calls `dropna()` and writes a CSV. | Monthly exchange rates use the final valid quote of each month; missing daily quotes are excluded without imputation. | Script, parser handling, input/output files, dates and checksums. |
| We regress `r_FX` on `usd_log` using `fit(cov_type='HAC')`. | Currency log returns are regressed on equity log returns, a negative-return indicator and their interaction; inference uses heteroskedasticity and autocorrelation consistent standard errors with six monthly lags. | Column mapping, package/version, estimator call and implementation options. |
| The canonical claim is `verified` after the receipt passes. | The estimated volatility difference is negative, with the reported 95% interval excluding zero. | Claim registry, execution receipt and the checks actually performed. |
| See `05_results/results.json`; eight pytest tests passed. | Table 4 reports the estimate, interval and sample size. | Machine-readable results and the exact scope of implementation tests. |
| `$to-paper` produced a submission-ready paper. | The manuscript reports observed estimates and their limitations. | Actual assistance/discovery/invocation evidence and unresolved review gates; never manufacture a successful invocation. |
| The random seed was frozen in a handoff so the workflow is complete. | The analytical design was fixed before estimation; a diagnostic extension was added only after residual dependence was observed. | Local timestamps, seeds, hashes, changes and the limits of that evidence. |

Keep conventional mathematical notation, defined OLS/HAC abbreviations, bootstrap design, units, sample exclusions and null results. Do not replace them with vague claims that the data were cleaned or a robust model was used. Preserve source-provider identity and APA citations while moving provider column labels and data-file mechanics to the companion.

For a paper whose research object is a programming language, software method or AI workflow, those terms can be legitimate disciplinary content. Review the actual purpose; an explicit `--allow-term` records a narrow exception to the checker, not permission to waive unrelated findings. A separate AI-assistance disclosure can name tools and describe their contribution. It must not imply author verification, native skill invocation or institutional approval without evidence.

Run the checker on the academic manuscript, not the operational checklist or the technical companion. It stops at references or an explicitly titled technical appendix/disclosure and ignores link/image destinations. Check the exported body visually and inspect false negatives manually; do not treat an exit code as proof of academic quality.
