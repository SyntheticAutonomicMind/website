# LoRA Model Training

**Fine-tune AI models on your own data for specialized knowledge and behavior.**

SAM lets you train custom LoRA (Low-Rank Adaptation) adapters that specialize local MLX models on specific topics, writing styles, or knowledge domains. Instead of retraining an entire model, LoRA adds small adapter layers that modify the model's behavior using minimal data and compute.

**What you can do:**
- Train a customer support model on your product documentation
- Create a domain expert in medical, legal, or technical fields
- Adapt a model to write in a specific style or voice
- Build a knowledge base assistant for your company or project

**Requirements:**
- macOS with Apple Silicon (for MLX models)
- Local MLX model installed
- Training data in JSONL format

---

## Table of Contents

1. [Understanding LoRA](#understanding-lora)
2. [LoRA vs RAG: When to Use Each](#lora-vs-rag-when-to-use-each)
3. [Training Workflow](#training-workflow)
4. [Preparing Training Data](#preparing-training-data)
5. [Using Trained Adapters](#using-trained-adapters)
6. [Real-World Examples](#real-world-examples)
7. [Troubleshooting](#troubleshooting)

---

## Understanding LoRA

**What is LoRA?**

LoRA (Low-Rank Adaptation) is a technique for fine-tuning AI models efficiently. Instead of updating millions of parameters in the base model, LoRA adds small adapter layers (typically 0.1% of the original model size) that learn to modify the model's behavior.

**Key benefits:**
- **Small file sizes** - Adapters are typically 20-50MB vs multi-GB base models
- **Fast training** - Train on consumer hardware in minutes to hours
- **Minimal data requirements** - Works with dozens to hundreds of examples
- **Reversible** - Keep your base model intact, swap adapters as needed
- **Specialized performance** - Often outperforms general models in specific domains

**How it works:**

1. You provide training examples (conversations or documents)
2. SAM trains an adapter that learns patterns from your data
3. The adapter modifies the base model's attention layers
4. During inference, the base model + adapter = specialized model

**What you need:**
- A local MLX model as the base (Qwen, Llama, Mistral, etc.)
- Training data in JSONL format (SAM can export this for you)
- Time for training (varies by dataset size and parameters)

---

## LoRA vs RAG: When to Use Each

SAM offers two ways to specialize AI behavior: **LoRA training** and **RAG (Retrieval-Augmented Generation)**. Here's when to use each:

### Use LoRA Training When:

✅ **You want the model to internalize knowledge**
- Medical terminology and diagnostic patterns
- Legal precedents and reasoning
- Company-specific jargon and concepts

✅ **You need consistent writing style**
- Brand voice and tone
- Formal vs casual language
- Specific formatting conventions

✅ **You have structured training data**
- Question-answer pairs
- Example conversations
- Documents with clear patterns

✅ **You want fast inference without context overhead**
- No need to retrieve documents on every message
- Adapter is always active
- Lower latency responses

### Use RAG (Memory/Documents) When:

✅ **Information changes frequently**
- Product catalogs
- Current events
- Evolving documentation

✅ **You need source attribution**
- Legal compliance (cite sources)
- Fact verification
- Transparency requirements

✅ **You have large reference libraries**
- Hundreds of documents
- Multi-gigabyte knowledge bases
- Diverse content types

✅ **You want immediate updates**
- Add new information without retraining
- Update facts in real-time
- Easy content management

### Hybrid Approach (Best of Both)

For many use cases, combine LoRA + RAG:

**Example: Customer Support Bot**
- **LoRA** - Train on conversation patterns, company voice, common responses
- **RAG** - Retrieve current product specs, pricing, inventory status

**Example: Medical Assistant**
- **LoRA** - Train on diagnostic reasoning and medical terminology
- **RAG** - Search current research papers and drug databases

**Example: Code Assistant**
- **LoRA** - Train on your team's coding style and patterns
- **RAG** - Retrieve documentation for libraries and APIs

---

## Training Workflow

### Step 1: Prepare Your Training Data

Training data must be in **JSONL format** (JSON Lines), where each line is a conversation example.

**Format:**
```jsonl
{"messages": [{"role": "user", "content": "What is our return policy?"}, {"role": "assistant", "content": "We offer 30-day returns with full refund for unused items."}]}
{"messages": [{"role": "user", "content": "Do you ship internationally?"}, {"role": "assistant", "content": "Yes, we ship to over 100 countries worldwide."}]}
```

**SAM can export training data for you:**

**From Conversations:**
1. In the chat interface, click the conversation menu (three dots)
2. Select **Export as Training Data**
3. Choose PII redaction options
4. Select chat template (Llama, Qwen, Mistral, etc.)
5. Save the JSONL file

**From Documents:**
1. Go to **SAM → Documents**
2. Select one or more documents
3. Click **Export for Training**
4. Choose chunking strategy:
   - **Semantic (Paragraphs)** - Natural paragraph breaks
   - **Fixed Size** - Uniform chunk sizes
   - **Page Aware (PDFs)** - Respect page boundaries
5. Configure PII detection if needed
6. Save the JSONL file

**PII Protection:**

SAM can detect and redact personally identifiable information before training:
- Personal names
- Organization names
- Place names
- Email addresses
- Phone numbers
- Credit card numbers
- Social security numbers
- IP addresses
- URLs

Enable PII redaction to keep sensitive data out of your training datasets.

### Step 2: Configure Training Settings

1. Go to **SAM → Preferences → Model Training**
2. Click the **Train LoRA Adapter** tab

**Select Training Data:**
- Click **Choose JSONL File...**
- Navigate to your prepared training data
- The filename appears when selected

**Select Base Model:**
- Choose an installed MLX model from the dropdown
- The model's family and type are displayed
- Only MLX models support LoRA training currently

**Name Your Adapter:**
- Enter a descriptive name (e.g., "Customer Support Bot")
- This name appears in the model picker

**Configure Training Parameters:**

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| **Rank** | 4-128 | 8 | Adapter capacity (higher = more capacity, larger file) |
| **Learning Rate** | 0.00001-0.01 | 0.0001 | How fast the model learns (lower = more stable) |
| **Epochs** | 1-50 | 3 | Number of passes through the data |
| **Batch Size** | 1-32 | 4 | Examples processed simultaneously (higher = faster, more memory) |

**Recommended settings for beginners:**
- Rank: 8-16 (good balance of capacity and file size)
- Learning Rate: 0.0001 (default is usually good)
- Epochs: 3-10 (start low, increase if needed)
- Batch Size: 4 (adjust based on memory)

### Step 3: Start Training

1. Click **Start Training** button
2. Training begins and shows real-time progress:
   - Current epoch and step
   - Training loss (should decrease over time)
   - Progress percentage

**What to expect:**
- Training takes minutes to hours depending on dataset size
- Loss should decrease steadily (means model is learning)
- You can click **Cancel Training** to stop early
- SAM remains usable during training (background process)

### Step 4: Monitor Results

During training, watch the loss metric:
- **Loss decreasing** ✅ - Model is learning
- **Loss not changing** ⚠️ - May need more epochs or higher learning rate
- **Loss increasing** ❌ - Learning rate too high, or data issues

**Training completes when:**
- All epochs finish
- Loss reaches minimum
- You click Cancel Training

The adapter is automatically saved to:
`~/Library/Application Support/SAM/adapters/`

---

## Using Trained Adapters

### Finding Your Adapter

After training completes, your adapter appears in two places:

**1. Model Picker (In Conversation):**
- Click the model picker dropdown in the chat interface
- Look for adapters prefixed with **"lora/"**
- Example: `lora/Customer Support Bot`

**2. LoRA Adapters Tab (In Preferences):**
- Go to **SAM → Preferences → Model Training**
- Click the **LoRA Adapters** tab
- See all trained adapters with metadata:
  - Adapter name
  - Training dataset filename
  - Creation date
  - Final loss value
  - Training parameters (epochs, steps, learning rate)

### Using an Adapter in Chat

1. Open a conversation (or start a new one)
2. Click the **model picker** in the toolbar
3. Select your adapter (e.g., `lora/Customer Support Bot`)
4. Send your message
5. The model responds using the specialized adapter

**Comparing Base vs Adapter:**

Test the same prompt with the base model and your adapter to see the difference:

**Example:**
```
You: What is our warranty policy?

Base model: I don't have specific information about your warranty policy.

Adapter: We provide a comprehensive 5-year warranty with 24/7 support. 
         The warranty covers manufacturing defects and includes free 
         replacement parts.
```

### Managing Adapters

**Load in Chat:**
- Click **Load in Chat** button in the LoRA Adapters tab
- Opens a new conversation with that adapter selected

**Delete Adapter:**
- Click the **Delete** button (red) next to an adapter
- Confirm deletion
- Adapter is permanently removed from disk

**Adapter Metadata:**

Each adapter stores:
- Adapter name (your chosen name)
- Base model used for training
- Training dataset filename
- Creation date and time
- Final training loss
- Training parameters (rank, epochs, steps, learning rate)

---

## Real-World Examples

### Example 1: Customer Support Bot

**Scenario:** Train a model on your product documentation to answer customer questions accurately.

**Training Data Preparation:**
1. Export your product docs as training data
2. Use **Semantic (Paragraphs)** chunking
3. Enable PII redaction (remove customer names/emails from examples)
4. Choose **Llama 3/4** template

**Training Configuration:**
- Base Model: Qwen 2.5 7B
- Rank: 16 (more capacity for detailed product info)
- Epochs: 5
- Batch Size: 4

**Result:** The adapter learns company terminology, product features, and common questions. It provides accurate, on-brand responses without hallucinating features.

**Use Case:**
- Customer support chat
- FAQ automation
- Internal helpdesk

---

### Example 2: Medical Domain Expert

**Scenario:** Create a specialized medical assistant trained on clinical guidelines and terminology.

**Training Data Preparation:**
1. Collect medical textbooks, guidelines, case studies
2. Export documents using **Page Aware (PDFs)** chunking
3. Enable full PII redaction (patient names, dates, identifiers)
4. Choose template matching your base model

**Training Configuration:**
- Base Model: Llama 3.1 8B
- Rank: 32 (higher capacity for complex medical reasoning)
- Epochs: 10
- Batch Size: 2 (slower but more thorough)

**Result:** The adapter understands medical terminology, diagnostic patterns, and clinical reasoning. It provides more accurate medical information than the base model.

**Use Case:**
- Clinical decision support
- Medical education
- Research assistance

**⚠️ Important:** This is for educational/research purposes only. Never use AI for actual medical diagnosis or treatment without professional supervision.

---

### Example 3: Writing Style Adaptation

**Scenario:** Train a model to write in your company's brand voice and tone.

**Training Data Preparation:**
1. Collect examples of approved marketing copy, blog posts, emails
2. Export as training data with **Semantic (Paragraphs)** chunking
3. No PII redaction needed (public content)
4. Choose appropriate template

**Training Configuration:**
- Base Model: Qwen 2.5 3B (smaller model fine for style)
- Rank: 8 (style doesn't need huge capacity)
- Epochs: 3
- Batch Size: 8 (faster training)

**Result:** The adapter mimics your brand's tone, vocabulary, and formatting conventions. Consistent output across all generated content.

**Use Case:**
- Marketing content generation
- Email drafting
- Blog post writing
- Social media content

---

### Example 4: Code Style Assistant

**Scenario:** Train a model on your team's codebase to follow your coding standards.

**Training Data Preparation:**
1. Export code files with documentation
2. Include examples of code reviews and corrections
3. Use **Fixed Size** chunking for consistent context
4. Choose template for your base model

**Training Configuration:**
- Base Model: Qwen 2.5 Coder 7B
- Rank: 16
- Epochs: 5
- Batch Size: 4

**Result:** The adapter learns your team's naming conventions, architecture patterns, and coding standards. Suggests code that matches your style guide.

**Use Case:**
- Code generation and completion
- Code review assistance
- Architecture suggestions
- Refactoring guidance

---

## Troubleshooting

### Training Issues

**Problem: "No models found" in base model dropdown**

**Solution:**
- Install at least one MLX model first
- Go to **SAM → Preferences → Local Models**
- Download an MLX-format model
- Models should appear in `~/Library/Caches/sam/models/`

---

**Problem: Training loss not decreasing**

**Possible causes:**
- Learning rate too low (try 0.0001 to 0.001)
- Not enough epochs (try 5-10 instead of 3)
- Dataset too small (need at least 20-50 examples)
- Data quality issues (inconsistent examples)

**Solution:**
- Increase epochs first (easiest fix)
- Try slightly higher learning rate
- Add more training examples
- Review data quality

---

**Problem: Training loss increasing or erratic**

**Possible causes:**
- Learning rate too high
- Batch size too large for dataset
- Corrupted training data

**Solution:**
- Lower learning rate (try 0.00005)
- Reduce batch size to 2
- Validate JSONL format (each line must be valid JSON)
- Check for duplicate or contradictory examples

---

**Problem: "Out of memory" during training**

**Solution:**
- Reduce batch size (try 2 or 1)
- Use smaller base model (3B instead of 7B)
- Close other memory-intensive apps
- Reduce rank (try 8 instead of 16)

---

**Problem: Adapter doesn't improve performance**

**Possible causes:**
- Insufficient training (not enough epochs)
- Dataset doesn't match use case
- Rank too low (not enough capacity)
- Base model already good at this task

**Solution:**
- Train for more epochs (10-20)
- Review and improve training data quality
- Increase rank to 16-32
- Try different base model
- Consider if RAG is better fit for this use case

---

### Adapter Usage Issues

**Problem: Adapter not appearing in model picker**

**Solution:**
- Check **SAM → Preferences → Model Training → LoRA Adapters** tab
- Adapter should be listed with metadata
- Try restarting SAM
- Verify adapter files exist in `~/Library/Application Support/SAM/adapters/`

---

**Problem: Adapter responses same as base model**

**Possible causes:**
- Adapter didn't train successfully (check final loss)
- Training data too similar to base model's knowledge
- Not enough training examples
- Adapter not actually loaded (check model picker)

**Solution:**
- Verify adapter is selected in model picker (should show `lora/YourName`)
- Check final training loss (should be < 2.0 for good results)
- Retrain with more examples or more epochs
- Test with queries specific to your training data

---

**Problem: Adapter responses contain training data verbatim**

**Cause:** Overfitting - model memorized examples instead of learning patterns

**Solution:**
- Use more diverse training examples
- Reduce epochs (try 3 instead of 10)
- Lower rank (try 8 instead of 32)
- Add more variation to training data

---

### Best Practices

**For Best Training Results:**

✅ **Quality over quantity** - 50 good examples beat 500 mediocre ones  
✅ **Diverse examples** - Cover different phrasings and scenarios  
✅ **Consistent formatting** - Use same chat template throughout  
✅ **Clean data** - Remove errors, typos, contradictions  
✅ **Start conservative** - Low rank, few epochs, then increase if needed  
✅ **Test incrementally** - Train small, test, adjust, retrain  
✅ **Combine with RAG** - Use LoRA for style/patterns, RAG for facts  

❌ **Avoid these mistakes:**

❌ Mixing different writing styles in training data  
❌ Including PII without redaction  
❌ Training on low-quality or error-filled content  
❌ Using too high learning rate (causes instability)  
❌ Expecting perfect results from tiny datasets  
❌ Training when RAG would be more appropriate  

---

## Next Steps

Now that you understand LoRA training:

1. **Start small** - Try training with 20-30 examples
2. **Experiment** - Test different parameters to see what works
3. **Compare** - Use the same prompts with base model vs adapter
4. **Iterate** - Refine your training data based on results
5. **Combine** - Use LoRA + RAG together for powerful results

**Related Documentation:**
- [Memory and RAG](memory-and-rag.md) - Understand SAM's retrieval system
- [Configuration](../power-user/configuration.md) - Model Training preferences reference
- [Advanced Workflows](../power-user/advanced-workflows.md) - Power-user training tips

**Need Help?**
- Check the [Troubleshooting](#troubleshooting) section above
- Visit the SAM community discussions
- Report bugs on GitHub

---

**LoRA training gives you the power to create specialized AI assistants tailored to your exact needs. Start training today and see the difference.**
