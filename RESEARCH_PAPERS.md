# REDREAMER 2025: Research Papers & Resources

This document contains all relevant research papers, datasets, and resources discovered during the 2025 assessment.

---

## Dream-Specific NLP Research

### 1. Dreams are more 'predictable' than you think
**Authors:** Various
**Publication:** Frontiers in Sleep, July 2025
**DOI:** 10.3389/frsle.2025.1625185
**URL:** https://www.frontiersin.org/journals/sleep/articles/10.3389/frsle.2025.1625185/full

**Abstract/Key Points:**
- Examines how language models (GPT-2, OLMo) predict dream reports
- Neural models trained on large text corpora from the web
- Dream reports can significantly differ structurally from other textual transcripts
- Explores perplexity metrics for dream text modeling

**Relevance:** Shows that dream text has distinct linguistic patterns that can be modeled with LLMs.

---

### 2. Dreaming with ChatGPT: Unraveling the Challenges of LLMs Dream Generation
**Authors:** Various
**Publication:** NLP4Science Workshop, ACL 2024, November 2024
**ACL Anthology:** 2024.nlp4science-1.11
**URL:** https://aclanthology.org/2024.nlp4science-1.11.pdf

**Abstract/Key Points:**
- Studies how large language models generate dream descriptions
- Identifies challenges in capturing surreal, non-linear narratives
- Explores dream-specific fine-tuning approaches
- Discusses the unique characteristics of dream language vs. normal text

**Relevance:** Directly addresses LLM-based dream generation, highlighting challenges and opportunities.

---

### 3. Dreamy: A Library for Automatic Analysis and Annotation of Dream Reports
**Authors:** Various
**Publication:** Sleep Medicine, 2024

**Key Points:**
- Automated analysis and annotation of dream reports
- Multilingual large language model support
- Enables processing of dream corpora across languages
- Open-source tool for dream text research

**Relevance:** Provides practical tools for working with dream datasets at scale.

---

### 4. Our Dreams, Our Selves: Automatic Interpretation of Dream Reports
**Publication:** Data Dryad Repository
**DOI:** 10.5061/dryad.qbzkh18fr
**URL:** https://datadryad.org/dataset/doi:10.5061/dryad.qbzkh18fr

**Key Points:**
- 20,000+ dream reports with algorithmic annotations
- Validated NLP tool applied to dreambank.net data
- Structured dataset for dream analysis research

**Relevance:** Large-scale annotated dream dataset available for training/evaluation.

---

## General Neural Text Generation (2024-2025)

### 5. Advances in Neural Text Generation: A Systematic Review (2022-2024)
**Publication:** ResearchGate, 2024
**URL:** https://www.researchgate.net/publication/388794175

**Key Points:**
- Systematic review of artificial neural networks for text generation
- Covers 2022-2024 period (recent advances)
- Popular metrics: BLEU, ROUGE, BERTScore
- Applications: table-to-text, knowledge graph generation, medical text
- Rapid evolution of methods and broadening application areas

**Relevance:** Provides comprehensive overview of modern text generation techniques.

---

### 6. Survey on Latest Advances in Natural Language Processing Applications of GANs
**Authors:** Koç et al.
**Publication:** WIREs Data Mining and Knowledge Discovery, December 2024
**DOI:** 10.1002/widm.70004
**URL:** https://wires.onlinelibrary.wiley.com/doi/full/10.1002/widm.70004

**Key Points:**
- Reviews Generative Adversarial Networks in text generation
- Four key models developed in recent years
- Applications to creative text generation
- Alternative to transformer-based approaches

**Relevance:** GANs as complementary approach to transformers for creative generation.

---

### 7. Beyond the Surface: Stylometric Analysis of GPT-4o's Capacity for Literary Style Imitation
**Publication:** Digital Scholarship in the Humanities, Oxford Academic, May 2025
**DOI:** 10.1093/dsh/article/40/2/587/8118784
**URL:** https://academic.oup.com/dsh/article/40/2/587/8118784

**Key Points:**
- GPT-4o shows impressive linguistic mimicry
- LLMs struggle with capturing full "richness" of human writing
- Human evaluators can frequently distinguish LLM from human text
- Implications for creative writing applications

**Relevance:** Important considerations for evaluating dream generation quality.

---

## Foundational Papers (Essential Reading)

### 8. Attention Is All You Need
**Authors:** Vaswani et al.
**Publication:** NeurIPS 2017
**arXiv:** 1706.03762
**URL:** https://arxiv.org/abs/1706.03762

**Key Points:**
- Introduced the Transformer architecture
- Self-attention mechanism
- Foundation for all modern LLMs
- Replaced RNN/LSTM for sequence modeling

**Relevance:** The architecture that replaced LSTMs (used in original REDREAMER).

---

### 9. Language Models are Few-Shot Learners (GPT-3)
**Authors:** Brown et al.
**Publication:** NeurIPS 2020
**arXiv:** 2005.14165
**URL:** https://arxiv.org/abs/2005.14165

**Key Points:**
- 175B parameter model
- Few-shot learning capabilities
- Strong performance on creative writing tasks
- Foundation for modern instruction-following models

**Relevance:** Demonstrates transformer potential for creative text generation.

---

### 10. LoRA: Low-Rank Adaptation of Large Language Models
**Authors:** Hu et al.
**Publication:** ICLR 2022
**arXiv:** 2106.09685
**URL:** https://arxiv.org/abs/2106.09685

**Key Points:**
- Parameter-efficient fine-tuning method
- Train only 0.1-1% of parameters
- Maintains model quality
- Enables fine-tuning on consumer GPUs

**Relevance:** Makes fine-tuning large models practical for REDREAMER 2025.

---

### 11. LLaMA: Open and Efficient Foundation Language Models
**Authors:** Touvron et al. (Meta AI)
**Publication:** arXiv 2023
**arXiv:** 2302.13971
**URL:** https://arxiv.org/abs/2302.13971

**Key Points:**
- Open-source LLM family (7B-65B parameters)
- Efficient training and inference
- Strong performance on creative tasks
- LLaMA 2 allows commercial use

**Relevance:** Recommended base model for production REDREAMER 2025.

---

## Datasets

### DreamBank Corpus
**Source:** dreambank.net
**HuggingFace:** gustavecortal/DreamBank-annotated
**GitHub:** remrama/dreambank, DxELab/dreambank

**Statistics:**
- 27,000+ dream narratives
- Primarily English
- Hall-Van de Castle annotations
- Publicly available

**Citation:**
```
Domhoff, G. W., & Schneider, A. (2008). Studying dream content
using the archive and search engine on DreamBank.net.
Consciousness and Cognition, 17(4), 1238-1247.
```

**Access:**
```python
from datasets import load_dataset
dataset = load_dataset("gustavecortal/DreamBank-annotated")
```

---

### Dream Decoder Dataset (2024)
**Source:** dreamdecoder.me/research/dream-report-2024
**Type:** Community-collected, modern dream submissions

**Features:**
- Contemporary dream language
- Diverse demographics
- Emotional content annotations
- Statistical analysis framework

**Access:** Via Dream Decoder platform

---

### Dryad Dream Repository
**DOI:** 10.5061/dryad.qbzkh18fr
**Size:** 20,000+ dreams
**Annotations:** Algorithmic NLP annotations

---

## Code Repositories & Tools

### HuggingFace Transformers
**URL:** https://github.com/huggingface/transformers
**Description:** State-of-the-art NLP library
**Stars:** 120K+
**License:** Apache 2.0

---

### PEFT (Parameter-Efficient Fine-Tuning)
**URL:** https://github.com/huggingface/peft
**Description:** LoRA, QLoRA, and other efficient fine-tuning methods
**Stars:** 13K+
**License:** Apache 2.0

---

### DreamBank Python Tools
**URL:** https://github.com/remrama/dreambank
**Description:** Easy access to DreamBank dataset
**License:** MIT

**Usage:**
```python
import dreambank
dreams = dreambank.download()
```

---

## Tutorials & Learning Resources

### 1. PyTorch Official Transformer Tutorial
**URL:** https://pytorch.org/tutorials/beginner/transformer_tutorial.html
**Updated:** 2024
**Topics:** Building transformers from scratch, language modeling

---

### 2. HuggingFace NLP Course
**URL:** https://huggingface.co/learn/nlp-course
**Free:** Yes
**Topics:**
- Transformer models fundamentals
- Fine-tuning and training
- Datasets and tokenizers
- Deployment

---

### 3. Text Generation with Transformers (2024)
**URL:** https://debuggercafe.com/text-generation-with-transformers/
**Date:** September 2024
**Topics:** Practical PyTorch text generation, DistilGPT-2 fine-tuning

---

### 4. Fine-tuning Transformers in PyTorch
**URL:** https://gmihaila.github.io/tutorial_notebooks/finetune_transformers_pytorch/
**Topics:** Step-by-step fine-tuning guide, best practices

---

## Blog Posts & Case Studies

### Warpland 2.0: Creative Writing with Neural Networks
**Date:** August 2024
**URL:** https://cssh.northeastern.edu/nulab/black-neural-network-text-generation/
**Topics:**
- GPT-2/GPT-3 for poetry generation
- Fine-tuning on literary corpora
- Creative applications

---

### More-than-Human Storytelling with GenAI
**Paper:** arXiv 2505.23780v1
**Date:** 2024
**Topics:**
- "Makoto" elderly storyteller character
- Dream-based narrative generation
- Longitudinal storytelling engagement
- User tells dreams → AI generates stories

---

## Related Projects

### GPT-2 for Creative Writing
**GitHub:** ADGEfficiency/creative-writing-with-gpt2
**Description:** Fine-tune GPT-2 with favorite authors
**Relevance:** Template for domain-specific fine-tuning

---

### T5 Fine-tuning for Text Generation
**GitHub:** Shivanandroy/T5-Finetuning-PyTorch
**Description:** Fine-tune T5 transformer using PyTorch
**Relevance:** Alternative architecture to GPT-style models

---

## Evaluation Metrics & Tools

### BERTScore
**Paper:** Zhang et al., ICLR 2020
**GitHub:** Tiiiger/bert_score
**Description:** Semantic similarity metric using BERT embeddings
**Use:** More accurate than BLEU for creative text

---

### ROUGE
**Description:** Recall-Oriented Understudy for Gisting Evaluation
**Use:** Compare generated text to reference summaries
**Python:** `pip install rouge-score`

---

### Perplexity
**Description:** Measure of how well model predicts text
**Use:** Lower perplexity = better language modeling
**Calculation:** `exp(cross_entropy_loss)`

---

## Community & Forums

### HuggingFace Forums
**URL:** https://discuss.huggingface.co/
**Topics:** Model troubleshooting, fine-tuning help

---

### r/MachineLearning (Reddit)
**URL:** https://www.reddit.com/r/MachineLearning/
**Topics:** Latest research, discussions

---

### Papers with Code
**URL:** https://paperswithcode.com/task/text-generation
**Description:** Research papers + implementation code
**Leaderboards:** Benchmarks for text generation tasks

---

## Cloud Computing Platforms (2025)

### GPU Options for Training

| Platform | GPU | Price/hour | Best For |
|----------|-----|------------|----------|
| **Google Colab Pro** | A100 40GB | ~$10/month | Quick experiments |
| **RunPod** | A100 80GB | $1.89/hr | Cost-effective training |
| **Lambda Labs** | A100 40GB | $1.10/hr | Dedicated instances |
| **Modal** | Various | Pay-per-use | Serverless deployment |
| **HuggingFace Spaces** | CPU/GPU | Free/Pro | Demo hosting |

---

## Recommended Reading Order

### For Beginners:
1. HuggingFace NLP Course (foundations)
2. PyTorch Transformer Tutorial (architecture)
3. Text Generation with Transformers tutorial (practical)
4. REDREAMER 2025 Implementation Guide (this repo)

### For Researchers:
1. "Attention Is All You Need" (Vaswani et al.)
2. "Dreams are more 'predictable' than you think" (2025)
3. "Dreaming with ChatGPT" (2024)
4. "LoRA" paper (Hu et al.)
5. Latest NeurIPS/ICLR/ACL papers on text generation

### For Practitioners:
1. REDREAMER 2025 Implementation Guide (this repo)
2. HuggingFace documentation
3. PEFT documentation (LoRA)
4. Fine-tuning tutorials
5. Deployment guides (FastAPI, Gradio)

---

## Citation Template

If you use this research for your own work:

```bibtex
@misc{redreamer2025,
  title={REDREAMER 2025: Modern Dream Generation with Transformers},
  author={[Your Name]},
  year={2025},
  url={https://github.com/lfhvn/REDREAMER},
  note={Modernization of original REDREAMER project using transformer architectures}
}
```

---

**Last Updated:** November 4, 2025
**Maintained By:** REDREAMER 2025 Project
**License:** MIT
