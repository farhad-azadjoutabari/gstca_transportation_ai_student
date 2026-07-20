# Types Of Generative AI Models

Generative AI is a broad family of models. Different model types create different kinds of content and use different training ideas.

This guide focuses on concepts, not specific products.

## Large Language Models

Large language models, or LLMs, generate and process text.

They can:

- Answer questions
- Summarize text
- Draft reports
- Write code
- Classify or extract information from text
- Translate language
- Follow instructions

Example:

```text
Input: Summarize the main safety findings from this table.
Output: A written summary.
```

Many modern LLMs use transformer architectures.

## Transformer Models

Transformers are neural network architectures that are especially good at working with sequences, such as text tokens.

Their key idea is attention. Attention helps the model focus on relevant parts of the input when producing output.

Transformers are used in many modern text, code, vision, audio, and multimodal models.

Example:

```text
The model attends to "high crash risk" and "speed limit" when answering a safety-analysis prompt.
```

## Diffusion Models

Diffusion models are widely used for image generation.

The basic idea:

1. Training data is gradually noised.
2. The model learns how to reverse the noise.
3. During generation, the model starts from noise and denoises toward a new image or other output.

Example:

```text
Input: A prompt describing a transit-oriented street scene.
Output: A generated image.
```

Diffusion models can also be used for audio, video, and other data types.

## Generative Adversarial Networks

Generative Adversarial Networks, or GANs, use two neural networks:

- Generator: creates fake examples.
- Discriminator: tries to tell fake examples from real examples.

The generator improves by trying to fool the discriminator.

Example:

```text
A GAN can learn to generate realistic-looking synthetic images.
```

GANs were especially important in earlier image-generation work, though diffusion and transformer-based systems are now very common.

## Variational Autoencoders

Variational Autoencoders, or VAEs, learn a compressed representation of data and then generate new examples from that representation.

They have two main parts:

- Encoder: compresses input into a lower-dimensional representation.
- Decoder: reconstructs or generates data from that representation.

Example:

```text
A VAE can learn a compact representation of image patterns and generate variations.
```

VAEs are useful for representation learning, anomaly detection, and some generative tasks.

## Autoregressive Models

Autoregressive models generate output one step at a time, where each step depends on previous steps.

For text:

```text
previous tokens -> predict next token -> repeat
```

Many language models generate text this way.

Example:

```text
The model writes a sentence by repeatedly choosing likely next tokens.
```

## Multimodal Models

Multimodal models work with more than one type of input or output.

Examples:

- Text and images
- Text and audio
- Images and video
- Text, tables, and charts

Example:

```text
Input: a crash map image and a question.
Output: a text explanation of visible patterns.
```

Multimodal models are useful when the task combines language, visuals, and structured data.

## Embedding Models

Embedding models convert content into numeric vectors that represent meaning or similarity.

They are not always generative by themselves, but they are often used inside generative AI systems.

Uses:

- Search
- Similarity matching
- Retrieval-augmented generation
- Clustering documents
- Finding related records

Example:

```text
Convert public comments into embeddings, find similar comments, then summarize themes.
```

## Retrieval-Augmented Generation

Retrieval-Augmented Generation, or RAG, combines search with generation.

Typical process:

1. User asks a question.
2. System searches trusted documents.
3. Relevant passages are given to the generative model.
4. Model answers using that context.

Example:

```text
Question: What does the project report say about high-crash intersections?
Search: retrieves relevant report sections.
Generation: writes an answer grounded in those sections.
```

RAG helps reduce hallucinations, but it does not remove the need to verify outputs.

## Fine-Tuned Models

Fine-tuning means adapting a trained model using a smaller, task-specific dataset.

Example:

```text
Fine-tune a model to classify transportation public comments into local planning categories.
```

Fine-tuning can help with style, format, or specialized tasks, but it requires good training examples and careful evaluation.

## Choosing A Generative Model Type

Choose based on the input and output:

- Text in, text out: LLM.
- Text prompt to image: diffusion or multimodal generative model.
- Image plus text question: multimodal model.
- Similarity search over documents: embedding model.
- Answer using local documents: RAG system.
- Specialized repeated task: possibly fine-tuning.

## Common Mistakes

- Calling every AI model a generative model.
- Assuming embeddings generate text by themselves.
- Assuming RAG guarantees correctness.
- Using a text-only model for a visual task.
- Fine-tuning before trying clear prompting or retrieval.
- Focusing on model type before defining the task.

## Useful Links

- IBM, What is Generative AI?: https://www.ibm.com/think/topics/generative-ai
- IBM Research, Foundation Models: https://research.ibm.com/topics/foundation-models
- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course/

