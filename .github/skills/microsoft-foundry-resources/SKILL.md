---
name: microsoft-foundry-resources
description: 'Choose the correct Azure ARM resource provider, type, and kind when writing Bicep, ARM, or Terraform for Microsoft Foundry (formerly Azure AI Foundry) and Azure Machine Learning. Use to pick between the modern Foundry resource (Microsoft.CognitiveServices) and the hub-based/classic or Azure Machine Learning resources (Microsoft.MachineLearningServices), whose providers differ even though the platform brand is shared.'
argument-hint: Describe the Foundry scenario or resource you need the ARM identifier for
---

# Microsoft Foundry Resource Reference

## When to Use

- You are authoring Bicep, ARM, or Terraform that provisions Microsoft Foundry or Azure Machine Learning.
- You need the exact ARM resource provider, type, and `kind` for a Foundry or Azure Machine Learning resource.
- A prompt or doc mixes "Microsoft Foundry" and "Azure AI Foundry" and you need to select the right resource for the scenario.

## Background: One Platform, Two Architectures

**Microsoft Foundry** is Microsoft's platform for building and operating generative-AI applications and agents. It was **renamed from Azure AI Foundry**; the earlier portal and hub-based architecture are now labeled **Foundry (classic)**.

For Infrastructure-as-Code, Foundry can be deployed with **two resource architectures**, and the ARM **resource provider** indicates which one is in use:

- **Foundry resource (default, recommended):** built on the `Microsoft.CognitiveServices` provider. This is the modern, agent-centric architecture and the default for projects in the Foundry portal; new capabilities land here first.
- **Hub-based architecture (Foundry classic):** built on the `Microsoft.MachineLearningServices` provider. Since June 2025 most hub capabilities have been moving to the Foundry resource, though select scenarios (for example, some open-source model deployments) still require a hub.

**Azure Machine Learning** is a separate, traditional ML product that shares the `Microsoft.MachineLearningServices` provider; distinguish it by its `kind`.

## Resource Identifiers

### Foundry resource (default) — provider `Microsoft.CognitiveServices`

| Resource | ARM Resource Type | `kind` |
| --- | --- | --- |
| Foundry account | `Microsoft.CognitiveServices/accounts` | `AIServices` |
| Foundry project | `Microsoft.CognitiveServices/accounts/projects` | — |
| Foundry application | `Microsoft.CognitiveServices/accounts/projects/applications` | — |
| Agent deployment | `Microsoft.CognitiveServices/accounts/projects/applications/agentDeployments` | — |

### Hub-based (Foundry classic) and Azure ML — provider `Microsoft.MachineLearningServices`

| Resource | ARM Resource Type | `kind` |
| --- | --- | --- |
| Foundry hub (classic) | `Microsoft.MachineLearningServices/workspaces` | `Hub` |
| Hub project (classic) | `Microsoft.MachineLearningServices/workspaces` | `Project` |
| Azure Machine Learning workspace | `Microsoft.MachineLearningServices/workspaces` | `Default` |

### Client SDK

| Component | Identifier |
| --- | --- |
| Microsoft Agent SDK (.NET) | NuGet package: `Microsoft.Agents.AI.*` |

## Foundry Resource Hierarchy

In the Foundry resource architecture, resources nest under a Cognitive Services account:

```
Microsoft.CognitiveServices/accounts                                   (kind: AIServices)
└── projects                                                           (Foundry Projects)
    └── applications                                                   (Foundry Applications)
        └── agentDeployments                                           (Agent Deployments)
```

## Key Distinctions

- **Foundry resource** — `Microsoft.CognitiveServices` provider, `kind: AIServices`. The modern, agent-centric Foundry architecture and the default for new projects.
- **Hub-based Foundry (classic)** — `Microsoft.MachineLearningServices` provider, `kind: Hub` or `kind: Project`. The earlier Azure AI Foundry architecture, retained for select scenarios.
- **Azure Machine Learning** — `Microsoft.MachineLearningServices` provider, `kind: Default`. A separate, traditional ML workspace for model training and MLOps.
- The two Foundry architectures share one platform brand but differ in ARM provider, resource kinds, APIs, and deployment patterns, so the provider and `kind` — not the product name — determine the template shape.

## How to Choose

1. **Read the resource provider, then the `kind`.** `Microsoft.CognitiveServices/accounts` (`kind: AIServices`) is the modern Foundry resource. `Microsoft.MachineLearningServices/workspaces` is either hub-based Foundry (`kind: Hub`/`Project`) or Azure Machine Learning (`kind: Default`).
2. **Prefer the Foundry resource for new work.** It is the default for projects in the Foundry portal, and new capabilities land there first.
3. **Build nested resources** in hierarchy order: account → project → application → agent deployment.
4. **Use a hub only when the scenario requires it** (for example, some open-source model deployments); check whether a migration path to a Foundry project applies before starting new hub work.
5. **Don't conflate Azure Machine Learning with Foundry.** Both use `Microsoft.MachineLearningServices/workspaces`; only `kind: Default` is traditional Azure Machine Learning.
6. **Treat the provider and `kind` as authoritative** over the product name in a doc or prompt, since they determine the Bicep/ARM/Terraform shape, APIs, and deployment pattern.

## References

- [Choose a resource type for Foundry](https://learn.microsoft.com/en-us/azure/foundry-classic/concepts/resource-types)
- [Migrate from hub-based to Foundry projects](https://learn.microsoft.com/en-us/azure/foundry-classic/how-to/migrate-project)
- [ARM/Bicep reference: `Microsoft.CognitiveServices/accounts/projects`](https://learn.microsoft.com/en-us/azure/templates/microsoft.cognitiveservices/accounts/projects)
