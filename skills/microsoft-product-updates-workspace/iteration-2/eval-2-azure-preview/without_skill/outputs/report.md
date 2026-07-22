# eval-2 azure-preview — WITHOUT skill / baseline (agent it2-e2-without, 299s)

18 preview-stage Azure updates since 2026-06-22 (modified ge filter); all public preview; excluded GA.
Includes 5 Microsoft Agent Framework items (564071, 563566, 563561, 563556, 563551) that the with-skill run missed, plus the same set otherwise.

## Sources used
- https://relcomms-prod-...azurefd.net/api/v2/azure?$count=true&includeFacets=true&top=100&skip=0&filter=modified%20ge%202026-06-22T00:00:00Z&orderby=modified%20desc
- exploratory: https://www.microsoft.com/releasecommunications/api/v2/azure/rss

## Ambiguities
- 567787, 565480: preview/status signals but GA lifecycle/title → excluded.
- 567651, 563331, 566948: status=Launched but preview lifecycle → included.
