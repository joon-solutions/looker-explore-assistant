results = [{
  "experiment_id": "20250708_183419",
  "timestamp": "2025-07-08 18:34:19.964956 UTC",
  "model_used": "gemini-2.5-pro",
  "input_context_path": "business_context_full.md",
  "input_token_count": "334341",
  "input_context_checksum": "4fb196f8d959df567d7bb97bd9b3b3bd4ec88e743bdfa10a0f9c4babe79a559d",
  "output_context_path": "business_context_distilled_v1.md",
  "output_token_count": "1737",
  "output_context_checksum": "71c08ed592728efe9f3677d2164871769c6c9db337404aa08fdee5316c3de9c9",
  "runtime_seconds": "56.529523",
  "evaluation_notes": "v1 prompt with simple instructions and raw business contexts",
  "status": "SUCCESS",
  "error_details": "{}",
  "generation_parameters": "{}"
},{
  "experiment_id": "20250708_183934",
  "timestamp": "2025-07-08 18:39:34.753383 UTC",
  "model_used": "gemini-2.5-pro",
  "input_context_path": "business_context_full.md",
  "input_token_count": "556527",
  "input_context_checksum": "4fb196f8d959df567d7bb97bd9b3b3bd4ec88e743bdfa10a0f9c4babe79a559d",
  "output_context_path": "business_context_distilled_v2.md",
  "output_token_count": "1554",
  "output_context_checksum": "f17d5ba0b393963100269a274f2f50e28f86ec06fed9ab9b894be91736f2693e",
  "runtime_seconds": "49.860031",
  "evaluation_notes": "v2 prompts : added booking container lookml and suggestions to add hints guiding the future gemini model to frame untrained business concepts",
  "status": "SUCCESS",
  "error_details": "{}",
  "generation_parameters": "{}"
}]


import os


def return_prompt(version: str = "v1") -> str:
    """
    Returns different versions of the distillation prompt.
    """
    v1 = ("""
          
          You are an expert in business documentation, tasked with training yourself.
          Analyze the following business documentation to extract only specialized, non-standard terms, concepts, 
          and key definitions that are unique to the container booking industry.
          **Exclude**:
          - Generic logistics or supply chain terminology
          - Common business terms or general industry knowledge
          - Content meant for onboarding or educating newcomers with baseline knowledge
          These documents often include general information for human readers. You, as a language model, do not need that.
          **Objective**:
          - Produce a concise, high-signal summary of specialized domain knowledge—we’ll call this the "Distilled Business Context".
          - This distilled context will be used to specialize a Gemini 2.5 Pro model in the container booking domain.
          - Start your response directly with the document content.
        """
    )

    # v2 aims to have longer response; adds the actual booking container lookml into play.
    with open('semantic_model.md', 'r') as f:
        lookml_model = f.read()
    v2 = f"""
You are an expert in business documentation. Your task is to **act as your own trainer**.
Analyze the following business documentation to extract only the **special**, **non-standard terms**, **domain-specific concepts**, and **key definitions** that are **unique to the container booking industry**.

#### Exclude:
* Generic logistics, shipping, or supply chain terminology
* Common business or operational terms
* Any content included to educate human readers on general knowledge (e.g., onboarding material)

These documents may contain foundational knowledge, but as a language model, you are assumed to have already been trained on such content.

---

#### Goal:

Produce a **concise, high-signal summary** of **specialized terminology and context**. This output is called the **"Distilled Business Context"**, which will be used to fine-tune a Gemini 2.5 Pro model into a domain specialist for container booking.

---

#### Context: LookML Metadata and Explore Assistant Workflow

The **Distilled Business Context** you generate will support the Gemini model as part of an **explore assistant system**, which uses **semantic LookML models** available in the section below to generate Looker queries based on user input.

This Gemini model relies on:
* The user’s natural language prompt
* The **distilled business context** you provide
* The **semantic metadata model** (LookML)

---

#### Additional Instructions:

* Also extract **terms that are semi-signaling**—phrases whose meaning depends on local context, business conventions, or implicit logic in the system.
* For such terms, include **interpretation hints** that will help a downstream model understand and apply them correctly in Looker query generation or summarization tasks.
* Start your response **directly with the document content**.

The upcoming context will be presented to you in 2 outtermost xml blocks as follow:
```
<LookML Metadata>
...
</LookML Metadata>
<Business Documentation>
...
</Business Documentation>
```
Here is the input:

    {lookml_model}
    """

    if version == "v1":
        return v1
    elif version == "v2":
        return v2
    else:
        raise ValueError(f"Unknown prompt version: {version}")
