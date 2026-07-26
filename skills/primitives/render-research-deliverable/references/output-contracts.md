# Research deliverable contracts

Load the shared rules and only the profile requested by the caller.

## Shared truth rules

Every output must:

1. name its source Research Brief and current version;
2. preserve claim strength and uncertainty;
3. distinguish proposed work from completed work;
4. cite inspectable evidence near material claims;
5. expose open decisions, risks, and scope boundaries;
6. avoid invented results, budget, access, approvals, partnerships, or timelines;
7. end with an artifact-specific acceptance or readiness statement.
8. keep the canonical artifact distinct from every audience-formatted export and record export provenance.

Do not force every heading below when the user's institution supplies a template. Map each required function into that template and record the mapping.

## Research Brief validation contract

Purpose: validate the canonical, audience-neutral source contract from which all downstream artifacts derive. Only `$synthesize-research-brief` writes it; the renderer reads this profile but never creates or repairs the brief.

Required functions:

- working title and status;
- one bounded research question;
- importance and intended decision or inference;
- closest literature, evidence IDs, and contribution delta;
- mechanism and serious rivals;
- constructs, units, estimand or prediction target, and hypotheses;
- data requirements, timing, measurement, and identification;
- methods, baselines, diagnostics, and evaluation;
- falsifiers, kill/repair/continue rules, ethics, and reproducibility;
- scope, exclusions, dependencies, and open decisions;
- researcher acceptance.

Completion requires a researchable design, not completed empirical results.

## Academic research plan

Purpose: show that a study is important, coherent, executable, and evaluable.

Required functions:

- executive summary;
- problem, context, and significance;
- questions and objectives;
- literature boundary and contribution;
- conceptual or theoretical framework;
- constructs, hypotheses, or propositions;
- data, sampling, measurement, and identification;
- methods, baselines, robustness, and evaluation;
- workpackages, sequence, milestones, and decision gates;
- falsifiers, risks, contingencies, ethics, and reproducibility;
- expected scholarly and practical outputs;
- references and unresolved dependencies.

Do not invent a calendar. Express duration or dates only when supplied or derived from accepted workpackage estimates.

## Grant or institutional proposal

Purpose: make a fundable case under a named call, institution, or decision process.

First inspect the current call, scoring rubric, page limits, eligibility, budget rules, required attachments, and deadline. Record access date and source.

Required functions:

- call fit and applicant eligibility;
- need and significance;
- objectives and innovation relative to verified literature;
- work plan and methodology;
- feasibility, capabilities, governance, and access;
- milestones, deliverables, and evaluation;
- risks, ethics, data management, and reproducibility;
- impact, dissemination, and sustainability;
- budget rationale tied to activities;
- references and compliance checklist.

Use placeholders for unapproved team members, partners, budget values, facilities, or institutional commitments. `funding-ready` requires every mandatory field, attachment, approval, and rule to be verified.

## Project proposal

Purpose: support a go/no-go, resource, or implementation decision for a research-informed project.

Required functions:

- stakeholder and decision owner;
- problem and evidence;
- target users or beneficiaries;
- objective, scope, and non-goals;
- proposed intervention, service, system, or program;
- alternatives considered and selection rationale;
- work plan, owners, dependencies, resources, and milestones;
- success metrics, baseline, evaluation, and stop rules;
- risks, governance, privacy, ethics, and maintenance;
- cost assumptions and unresolved approvals;
- decision requested.

Do not disguise an untested intervention as an established solution. Link evaluation back to the Research Brief.

## Paper blueprint

Purpose: define a submission-shaped argument before all analyses are complete.

Required functions:

- candidate title and abstract logic;
- introduction argument spine;
- literature and contribution placement;
- theory or conceptual framework;
- data, identification, and methods;
- planned results tables, figures, and falsification tests;
- discussion, limits, implications, and conclusion;
- claim-to-evidence and section-to-artifact pointers.

Label every planned table and result. A complete blueprint is not a complete manuscript.

## Manuscript draft

Purpose: present completed research as a cumulative academic argument.

Required functions normally include title, abstract, introduction, literature and contribution, theory, data, identification and methods, results, robustness or falsification, discussion, limitations, conclusion, references, and appendices.

A `complete-draft` requires:

- executed and registered results;
- exact sample and version provenance;
- uncertainty and negative results;
- citations that entail material claims;
- no placeholder presented as observation;
- internal consistency between text, tables, figures, equations, and appendices.

When these conditions fail, produce an `outline` or `partial` draft and name the blocked sections.
