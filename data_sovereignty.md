# Data Sovereignty and Earth Data Science

**Read this before starting the tutorial.**

## The Data You Will Use Describes Indigenous Lands
Every dataset in this tutorial covers the lands of the Oglala Lakota Nation and other
Oceti Sakowin Nations where appropriate. That fact carries responsibilities.

This document introduces four frameworks that guide responsible use of data
about Indigenous Peoples and their lands. These are not bureaucratic checkboxes.
They are expressions of the rights and authority of Indigenous communities over
information that describes their homelands, their environments, and their futures.

## OCAP® (Ownership, Control, Access, Possession)
**Reference:** https://fnigc.ca/ocap-training/

OCAP® was developed by the First Nations Information Governance Centre and
asserts that Tribal Nations have the right to:

- **Own** data about their communities and territories
- **Control** how that data is collected, used, and shared
- **Access** data that exists about them
- **Possess** data physically and administratively

**What this means for this tutorial:**
The federal data used here (MODIS, gridMET, Census) was collected by federal
agencies without Tribal authority to control the collection. It is a proxy, or
an outside view of Tribal lands. It does not replace Tribal knowledge, Tribal
data, or Tribal authority over the land and environment it describes.

Any analysis you produce using this tutorial should:
- Be clear about what federal data can and cannot show
- Never substitute federal data for Tribal knowledge or Tribal-collected data
- Be shared first with the Tribal communities your analysis describes

## CARE Principles (Collective Benefit, Authority to Control, Responsibility, Ethics)
**Reference:** https://www.gida-global.org/care

The CARE Principles for Indigenous Data Governance were developed by the
Global Indigenous Data Alliance. They complement FAIR (see below) by
addressing the ethical obligations that FAIR alone does not cover.

| Principle | What it means for your analysis |
|---|---|
| **Collective Benefit** | Does your analysis benefit the Tribal community it describes? |
| **Authority to Control** | Does the Tribal community have authority over how results are used? |
| **Responsibility** | Are you accountable to the community, not just to your institution? |
| **Ethics** | Does your work respect Indigenous values and rights throughout? |

**A question to ask yourself before publishing any analysis:**
*"Who benefits from this work, and does the community I am analyzing have
authority over how these results are used?"*

## FAIR Principles (Findable, Accessible, Interoperable, Reusable)
**Reference:** https://www.go-fair.org/fair-principles/

FAIR principles govern technical data management practices. Data should be:
- **Findable**: has a persistent identifier and rich metadata
- **Accessible**: retrievable through open, standard protocols
- **Interoperable**: uses standard formats and vocabularies
- **Reusable**: has clear licensing and provenance

FAIR is the technical floor. CARE and OCAP® are the ethical layer that FAIR
does not address. A dataset can be fully FAIR and still violate Indigenous
data sovereignty.

## IEEE 2890-2025 (Provenance of Indigenous Peoples' Data)
**Reference:** https://standards.ieee.org/ieee/2890/10318/
Published in November 2025, IEEE 2890 is the first international standard
for the provenance of Indigenous Peoples' data. It establishes:
- Common parameters for describing where Indigenous Peoples' data came from
- How data should be connected to people and place
- How governance responsibilities travel with data through transformations
- Controlled vocabulary for provenance metadata

**What this means for data cubes:**
When you build a data cube that includes data about Tribal lands, the
provenance of that cube (where the data came from, whose land it describes,
what label it carries) should travel with the cube. Notebook 06 demonstrates
how to embed provenance metadata in your xarray datasets.

## The Satellite Does Not Know What It Is Looking At
This is the most important thing to understand about remote sensing data:
A satellite measures reflected light. It does not know that the grassland
it is measuring has been managed by Oglala Lakota land stewards for generations.
It does not know that a "low NDVI" pixel might reflect a deliberate traditional
burning practice rather than land degradation. It does not know that the
"drought" it is recording is being experienced differently by an Elder rancher
and a BIA administrator.

Data cubes built from satellite data are powerful tools. They can reveal
patterns across time and space that no human observer could see alone.
But they are not complete. The knowledge that gives those patterns meaning
comes from the people who live on and steward the land.

Build your cubes with humility. Use them in partnership with, not in place of,
Tribal knowledge and Tribal expertise.

## Resources
- OCAP® Training: https://fnigc.ca/ocap-training/
- CARE Principles: https://www.gida-global.org/care
- FAIR Principles: https://www.go-fair.org/fair-principles/
- IEEE 2890-2025: https://standards.ieee.org/ieee/2890/10318/
- Local Contexts TK Labels: https://localcontexts.org/
- Global Indigenous Data Alliance: https://www.gida-global.org/
- Collaboratory for Indigenous Data Governance: https://indigenousdatalab.org/
