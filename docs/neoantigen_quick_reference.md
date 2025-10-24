# Neoantigen Qualification: Quick Reference for Moderna-Style Researchers

## The 10 Critical Parameters (In Order of Importance)

### 1. **MHC-I Binding Affinity** ⭐⭐⭐⭐⭐
- **Target:** IC50 < 500 nM (strong) or < 5000 nM (weak)
- **Tool:** NetMHCpan 4.0+
- **Note:** Necessary but not sufficient (~51% predictive alone)

### 2. **Presentation Probability** ⭐⭐⭐⭐⭐
- **Target:** High probability of surface presentation
- **Tool:** MixMHCpred
- **Why:** Many peptides bind MHC but never reach cell surface

### 3. **Tumor Expression Level** ⭐⭐⭐⭐⭐
- **Target:** > 10 TPM (Transcripts Per Million)
- **Source:** RNA-seq data
- **Critical:** Not expressed = not presented

### 4. **Clonality (Variant Allele Fraction)** ⭐⭐⭐⭐
- **Target:** VAF > 0.3-0.5 (present in all tumor cells)
- **Why:** Prevents tumor escape through antigen loss
- **Bonus:** Driver mutations are typically clonal

### 5. **Differential Agretopicity (DAI)** ⭐⭐⭐⭐
- **Target:** Mutant peptide binds stronger than wild-type
- **Formula:** DAI = WT_affinity - Mutant_affinity
- **Why:** Better differential recognition by T cells

### 6. **Dissimilarity to Self (Foreignness)** ⭐⭐⭐⭐
- **Target:** Low similarity to normal human proteome
- **Tool:** DisToSelf algorithm
- **Why:** Avoids central tolerance, enhances recognition

### 7. **pMHC Binding Stability** ⭐⭐⭐
- **Target:** Stable, prolonged half-life
- **Tool:** NetMHCstabpan
- **Why:** Persistent presentation needed for T cell priming

### 8. **Mutation Position** ⭐⭐⭐
- **Target:** Central position in peptide (positions 4-6 for 9-mers)
- **Why:** Better exposed to TCR, not anchor positions
- **Avoid:** Mutations at positions 2, 9 (MHC anchors)

### 9. **Similarity to Pathogens** ⭐⭐⭐
- **Target:** Similar to known pathogen epitopes
- **Tool:** SimToIEDB
- **Why:** Cross-reactivity with memory T cells

### 10. **HLA Expression Verification** ⭐⭐⭐
- **Check:** HLA allele not deleted, mutated, or silenced
- **Source:** RNA-seq, WES copy number
- **Critical:** No HLA = no presentation

---

## The Moderna mRNA-4157 Formula

**Input:** Tumor + matched normal sequencing  
**Process:**
1. Identify ~10,000 non-synonymous mutations
2. Filter to ~200-300 with good MHC binding
3. Refine to ~50-80 with high immunogenicity scores
4. Select **10-34 final neoantigens** including:
   - Validated immunogenic neoantigens
   - High-scoring predicted neoantigens
   - Driver gene mutations (KRAS, TP53, etc.)

**Vaccine Design:**
- Single mRNA construct (up to 34 neoantigens)
- 27-mer peptides (both MHC-I and MHC-II presentation)
- Lipid nanoparticle delivery
- Combination with pembrolizumab (checkpoint inhibitor)

**Results (KEYNOTE-942):**
- 44% reduction in melanoma recurrence risk
- 60% immunogenicity rate
- FDA Breakthrough Designation

---

## Qualification Workflow (3 Stages)

### Stage 1: Computational Screening (10,000 → 200)
```
Filters:
✓ Tumor-specific (not germline)
✓ Expressed (> 10 TPM)
✓ MHC binding < 500 nM
✓ Matches patient HLA alleles
✓ VAF > 0.25

Output: 200-300 candidates
Time: 1-2 days
```

### Stage 2: Bioinformatics Refinement (200 → 50)
```
Advanced Scoring:
✓ High presentation probability
✓ Good DAI (differential binding)
✓ Low self-similarity
✓ Central mutation position
✓ Clonal (not subclonal)
✓ Predicted proteasome processing

Output: 50-80 top candidates
Time: 3-5 days
```

### Stage 3: Experimental Validation (50 → 10-34)
```
Testing:
✓ Mass spectrometry (if available)
✓ T cell assays (ELISpot, tetramers)
✓ Manufacturing feasibility
✓ Diversity check (multiple HLA alleles)

Output: 10-34 final neoantigens
Time: 2-4 weeks (if validation done)
```

---

## Critical Success Factors

### Must-Haves (Deal Breakers)
1. **Tumor-specific** (not in germline)
2. **Expressed in tumor** (RNA-seq evidence)
3. **MHC-I binding** (< 500 nM threshold)
4. **Patient HLA-matched** (correct allele)
5. **Manufacturing feasible** (mRNA design)

### Strong Preferences
6. **Clonal mutation** (VAF > 0.3)
7. **High presentation** (MixMHCpred score)
8. **Good DAI** (better than WT)
9. **Multiple neoantigens** (10-34 per vaccine)
10. **Experimentally validated** (if time permits)

### Nice-to-Haves
11. Low self-similarity
12. High pathogen similarity
13. Driver mutation
14. Good structural features
15. No HLA loss in tumor

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Binding Affinity Only
Using MHC binding as the sole criterion has only ~51% accuracy for predicting immunogenicity.

**Solution:** Integrate presentation, expression, and TCR recognition features.

### ❌ Mistake 2: Ignoring Expression
A neoantigen with perfect binding that isn't expressed is useless.

**Solution:** Always check RNA-seq expression (> 10 TPM minimum).

### ❌ Mistake 3: Subclonal Mutations
Mutations in only 10-20% of tumor cells allow easy escape.

**Solution:** Prioritize clonal mutations with VAF > 0.3.

### ❌ Mistake 4: Single Neoantigen
Immunodominance means only 1-2 neoantigens may work.

**Solution:** Include 20-34 diverse neoantigens per vaccine.

### ❌ Mistake 5: Not Checking HLA Expression
Tumor can lose or silence HLA alleles.

**Solution:** Verify HLA expression via RNA-seq or flow cytometry.

---

## Quick Decision Tree

```
Does peptide bind MHC-I < 500nM? 
  NO → REJECT
  YES ↓

Is it expressed in tumor > 10 TPM?
  NO → REJECT
  YES ↓

Is mutation tumor-specific (not germline)?
  NO → REJECT
  YES ↓

Does patient have this HLA allele?
  NO → REJECT
  YES ↓

Is VAF > 0.25 (reasonably clonal)?
  NO → Lower priority
  YES ↓

High presentation probability?
  NO → Lower priority
  YES ↓

Good DAI (better than WT)?
  NO → Consider
  YES → HIGH PRIORITY CANDIDATE ✓

Multiple high-priority candidates (10-34)?
  NO → Keep screening
  YES → PROCEED TO MANUFACTURING
```

---

## Benchmarks & Expectations

### Typical Conversion Rates
- Non-synonymous mutations → 10,000
- MHC binding candidates → 200-300 (2-3%)
- High immunogenicity score → 50-80 (0.5-0.8%)
- **Final vaccine neoantigens → 10-34 (0.1-0.3%)**

### Clinical Performance (Moderna)
- **Immunogenicity rate:** ~60% of neoantigens
- **Clinical efficacy:** 44% reduction in recurrence (melanoma)
- **Response type:** Mostly de novo (not pre-existing)
- **T cell type:** Both CD4+ and CD8+ activated
- **Safety:** Grade 1-2 adverse events, manageable

### Timeline (Per Patient)
- Sequencing & analysis: 2-4 weeks
- Neoantigen selection: 1 week
- mRNA manufacturing: 4-8 weeks
- **Total time to treatment:** 7-13 weeks

---

## Tools Summary

| Purpose | Tool | Note |
|---------|------|------|
| MHC binding | NetMHCpan 4.0+ | Industry standard |
| Presentation | MixMHCpred | Critical addition |
| Stability | NetMHCstabpan | Newer metric |
| Immunogenicity | PRIME, DeepImmuno | ML models |
| Pipeline | pVACtools, Vaxrank | End-to-end |
| Validation | Mass spec, ELISpot | Experimental |

---

## One-Page Summary

**Goal:** Identify 10-34 neoantigens per patient that will trigger effective anti-tumor immunity.

**Core Criteria (Top 5):**
1. MHC binding < 500 nM
2. High presentation probability
3. Tumor expression > 10 TPM
4. Clonal (VAF > 0.3)
5. Better than wild-type (DAI)

**Process:**
- Start with ~10,000 mutations
- Filter to ~200 with good binding
- Refine to ~50 with high scores
- Select 10-34 for vaccine

**Success Rate:**
- 60% of neoantigens immunogenic
- 44% reduction in recurrence
- Both CD4+ and CD8+ responses

**Key Insight:**
Less than 1% of predicted neoantigens make it to the final vaccine. Multi-parameter screening with experimental validation is essential.

---

**Remember:** It's not just about finding neoantigens—it's about finding the RIGHT neoantigens that will actually work in patients.
