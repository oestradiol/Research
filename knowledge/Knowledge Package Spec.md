# Knowledge Package Spec

## 1. Purpose

This document is the control spec for `Research/knowledge/`.

It defines a public, Obsidian-first knowledge atlas founded on SUF and structured for navigation, study, and later growth.

## 2. Core contract

`Research/knowledge/` must be:

- public and package-ready
- Obsidian-friendly and graph-friendly
- study-first rather than publication-formalized
- broader than SUF where that improves the atlas
- typed in its cross-links
- typed in both cluster-to-node and node-to-cluster directions
- scaffolded by SUF without becoming captive to SUF

## 3. SUF role

SUF should act here as:

- a layered scaffold for the broad cluster order
- one route-building and comparison lens
- one source of optional study hooks between nodes

SUF should **not** be treated as the mandatory voice inside every node. Each note should be able to guide its own study, combine other frameworks, or move beyond SUF entirely.

## 4. Package skeleton

```text
Research/knowledge/
├─ README.md
├─ Knowledge Package Spec.md
├─ CONTRIBUTING.md
├─ CHANGELOG.md
├─ CITATION.cff
├─ LICENSE
├─ suf-relationship.md
├─ studying-and-teaching-with-suf.md
├─ _indexes/
│  ├─ knowledge-index.md
│  ├─ cluster-index.md
│  ├─ node-index.md
│  ├─ study-routes-index.md
│  └─ relation-tags-index.md
├─ _templates/
│  ├─ cluster-template.md
│  ├─ domain-template.md
│  ├─ subdomain-template.md
│  └─ study-route-template.md
├─ _relations/
│  ├─ grounds.md
│  ├─ formalizes.md
│  ├─ constrains.md
│  ├─ emerges-from.md
│  ├─ scaffolds.md
│  ├─ requires.md
│  ├─ supports.md
│  ├─ implements.md
│  ├─ interprets.md
│  └─ feeds-back.md
├─ map/
│  ├─ README.md
│  ├─ 00-meta-foundations/README.md
│  ├─ 01-formal-structure/README.md
│  ├─ 02-physical-sciences/README.md
│  ├─ 03-life-sciences/README.md
│  ├─ 04-mind-and-behavior/README.md
│  ├─ 05-culture-and-history/README.md
│  ├─ 06-social-and-institutional-systems/README.md
│  ├─ 07-applied-design-and-intervention/README.md
│  └─ 08-integrative-and-reflexive/README.md
└─ study-routes/
   ├─ README.md
   ├─ suf-guided-orientation-route.md
   ├─ measurement-and-inference-route.md
   ├─ organization-and-coordination-route.md
   ├─ mind-life-interface-route.md
   ├─ sustainability-and-governance-route.md
   └─ framework-comparison-and-knowledge-organization-route.md
```

## 5. Cluster model

The current gateway clusters are:

- `00-meta-foundations`
- `01-formal-structure`
- `02-physical-sciences`
- `03-life-sciences`
- `04-mind-and-behavior`
- `05-culture-and-history`
- `06-social-and-institutional-systems`
- `07-applied-design-and-intervention`
- `08-integrative-and-reflexive`

This order is a scaffold for navigation, not a claim that knowledge is a rigid staircase.

## 6. Current instantiated node program

The current scaffold instantiates the original 70-node seed program:

- `00-meta-foundations` = 9 nodes
- `01-formal-structure` = 14 nodes
- `02-physical-sciences` = 5 nodes
- `03-life-sciences` = 7 nodes
- `04-mind-and-behavior` = 4 nodes
- `05-culture-and-history` = 5 nodes
- `06-social-and-institutional-systems` = 6 nodes
- `07-applied-design-and-intervention` = 13 nodes
- `08-integrative-and-reflexive` = 7 nodes

Each seed node should link:

- upward to its cluster gateway through `emerges-from`
- laterally to related nodes through typed relation links
- outward to neighboring clusters or routes when useful

Each cluster gateway should link:

- downward to its member nodes through `scaffolds`
- sideways to adjacent clusters through typed relation links

Each route note should link:

- to other routes through `requires` and `supports`
- to its key nodes in the body, not only in properties
- back into the cluster-node graph so routes remain first-class in Graph view

The goal is one connected graph rather than isolated directory islands.

## 7. Required note behavior

Cluster, domain, and subdomain notes should normally include:

- frontmatter with at least `tags`, `kind`, and `status`
- study purpose
- key questions
- canonical or starter anchors
- typed links
- typed relation opportunities
- an optional `SUF hook / route note`
- current status
- route links where route travel is genuinely useful

They should **not** require a full SUF application block in every note.

Deepened hub nodes may also include:

- `suf_role`
- selective `aliases`
- `related_routes`
- expanded anchor families
- fuller outbound links and route pointers

## 8. Required package behavior

- `_indexes/` should make the package navigable in folder view and graph view.
- `_templates/` should keep note types consistent.
- `_relations/` should keep lateral links typed.
- cluster gateways should expose their members through typed scaffold links.
- `_indexes/node-index.md` should list the full instantiated 70-node program in one place.
- `study-routes/` should allow guided traversals through clusters or mixed-framework study paths.
- route-to-route links should be explicit enough to show dependency structure in Graph view.
- `map/` should hold the broad knowledge-cluster gateways.
- `studying-and-teaching-with-suf.md` should explain one honest pedagogical use of SUF as scaffold rather than universal curriculum.
- `../using-this-research-with-human-assistants-and-reasoning-agents.md` should remain the umbrella guidance note for collaborative use, reasoning agents, and accessibility-supported navigation.

## 9. Anti-rules

Do not let this package:

- collapse into the SUF applications atlas
- become a dump of disconnected notes
- overlink so aggressively that the graph becomes noise
- treat SUF as the only legitimate framework
- mistake scaffold order for proof of metaphysical or disciplinary hierarchy

## 10. Obsidian alignment

This package should stay aligned with current official Obsidian guidance:

- safe filenames
- explicit internal links as the graph backbone
- Markdown body links for portability
- lightweight properties for filtering, grouping, and route metadata
- tags used as grouping aids rather than substitutes for links

## 11. Migration note

This document replaces the older `Applications Layer Population Spec` role.

That older framing was tied to public applications work. The current document is for a public sibling project instead:

- broader
- more graph-native
- more Obsidian-native
- explicitly crosslinked with SUF
