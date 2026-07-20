# Generative AI

Generative AI is AI that creates new content.

The content can be:

- Text
- Images
- Code
- Audio
- Video
- Tables
- Synthetic data
- Summaries
- Explanations

Traditional predictive ML often answers:

```text
What number or category should this row have?
```

Generative AI often answers:

```text
What new content should be produced from this input?
```

## Simple Examples

Text generation:

```text
Prompt: Summarize this crash analysis in plain language.
Output: A written summary.
```

Image generation:

```text
Prompt: Create an illustration of a protected bike lane.
Output: A generated image.
```

Code generation:

```text
Prompt: Write Python code to calculate crash rate by road segment.
Output: A code snippet.
```

Synthetic data generation:

```text
Prompt or conditions: Generate example road-segment records for a classroom exercise.
Output: A synthetic table.
```

## How Generative AI Differs From Classification And Regression

Regression predicts a number.

Classification predicts a category.

Generative AI creates content.

Example:

Regression:

```text
Predict speed ratio = 0.73
```

Classification:

```text
Predict congestion class = high
```

Generative AI:

```text
Generate a paragraph explaining why several roads may be congested.
```

## What Is A Foundation Model?

A foundation model is a large model trained on broad data that can be adapted to many tasks.

Examples of tasks:

- Answering questions
- Summarizing documents
- Writing code
- Extracting information
- Classifying text
- Generating images
- Understanding images and text together

The same foundation model may support many different applications through prompting, fine-tuning, retrieval, or tool use.

## What Is A Large Language Model?

A large language model, or LLM, is a generative AI model trained to work with text or token sequences.

LLMs learn patterns in language. A simplified explanation is:

```text
Given the previous tokens, predict likely next tokens.
```

By repeating this process, the model can generate paragraphs, answers, code, tables, or structured text.

## What Is A Prompt?

A prompt is the input given to a generative model.

Example:

```text
Explain the difference between regression and classification using a road safety example.
```

Prompts can include:

- A question
- Instructions
- Context
- Examples
- Data
- Desired output format

Clear prompts usually produce better outputs.

## What Is Inference In Generative AI?

Inference means using a trained model to produce output.

For generative AI:

```text
prompt -> trained generative model -> generated content
```

The model is not being fully retrained every time it answers. It is applying what it learned during training.

## Generative AI Can Be Wrong

Generative AI can produce fluent output that is incorrect. This is sometimes called a hallucination.

Examples:

- Making up a source
- Giving a wrong formula
- Stating a false fact confidently
- Misreading a table
- Inventing details that are not in the provided data

Because of this, generative AI output should be checked, especially for technical, legal, financial, medical, or safety-related work.

## Generative AI In Transportation Projects

Helpful uses:

- Draft plain-language summaries.
- Explain model results to nontechnical audiences.
- Convert rough notes into a structured report.
- Help write code, with human review.
- Generate example scenarios for teaching.
- Extract themes from public comments, with validation.

Risky uses:

- Making final engineering decisions without review.
- Inventing facts about crash locations.
- Summarizing data without checking calculations.
- Treating generated citations as real without verifying them.
- Using private or sensitive data in tools without permission.

## Common Mistakes

- Assuming generated text is always true.
- Confusing confident language with evidence.
- Using generative AI output without checking against source data.
- Asking vague prompts and expecting precise results.
- Treating generative AI as a replacement for domain expertise.
- Forgetting privacy and data-governance rules.

## Useful Links

- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course/
- IBM, What is Generative AI?: https://www.ibm.com/think/topics/generative-ai
- IBM Research, Foundation Models: https://research.ibm.com/topics/foundation-models

