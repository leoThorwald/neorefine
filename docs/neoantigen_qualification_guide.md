# Neoantigen Qualification Criteria for Cancer Vaccine Development
## A Guide for Researchers at Companies Like Moderna

---

## Executive Summary

When qualifying candidate neoantigens for personalized cancer vaccines, researchers at companies like Moderna evaluate a multi-layered set of criteria that spans molecular, immunological, computational, and clinical dimensions. The goal is to identify the ~1-3% of predicted neoantigens that will actually trigger effective anti-tumor immunity.

**Key Insight:** <60% of predicted neoantigens prove immunogenic in practice. Comprehensive screening is essential.

---

## 1. PRIMARY QUALIFICATION CRITERIA

### A. MHC Binding & Presentation (Foundation)

**HLA-Peptide Binding Affinity**
- **Target:** IC50 < 500 nM (strong binder) or < 5000 nM (weak binder)
- **Tool:** NetMHCpan, MixMHCpred, MHCflurry
- **Critical Note:** Necessary but NOT sufficient for immunogenicity
- **Sweet Spot:** Neither too strong nor too weak
  - Too strong → T cell exhaustion, peripheral tolerance
  - Too weak → Insufficient immune activation

**Binding Stability (pMHC Complex)**
- **Target:** Stable pMHC complex with prolonged half-life
- **Tool:** NetMHCstabpan
- **Rationale:** Persistent surface presentation required for T cell activation
- **Metric:** Binding stability score correlates with immunogenicity (p < 0.001)

**Peptide Presentation Score**
- **Target:** High probability of actual cell surface presentation
- **Tool:** MixMHCpred (presentation mode)
- **Why It Matters:** Many peptides bind MHC but never reach cell surface
- **Integration:** Combine with binding affinity for better prediction

### B. Immunogenicity Prediction (Core Filter)

**T Cell Recognition Potential**
- **Differential Agretopicity Index (DAI)**
  - Compares mutant vs. wild-type peptide binding
  - Higher mutant affinity → Better immunogenicity
  - Controversial but widely used
  - Formula: DAI = (WT_affinity - Mutant_affinity)

**Foreignness / Self-Similarity**
- **Dissimilarity to Self-Proteome (DisToSelf)**
  - Lower similarity to normal proteins → Better immunogenicity
  - Reduces risk of central tolerance
  
- **Similarity to Pathogen Epitopes (SimToIEDB)**
  - Higher similarity to known pathogen epitopes → Better recognition
  - Leverages pre-existing T cell memory from infections

**TCR Recognition Features**
- Hydrophobicity at TCR-exposed positions
- Charge distribution patterns
- Position of mutation within peptide (middle positions = better)
- Peptide length (9-mers for MHC-I, 15-mers for MHC-II)

### C. Tumor Expression & Clonality

**Gene Expression Level**
- **Target:** High tumor-specific expression
- **Metric:** TPM (Transcripts Per Million) or FPKM from RNA-seq
- **Threshold:** Typically > 10 TPM for detectability
- **Why:** Must be expressed to be presented

**Variant Allele Fraction (VAF)**
- **Target:** High VAF (ideally > 0.3-0.5)
- **Indicates:** Clonality - present in all tumor cells vs. subclonal
- **Rationale:** Clonal neoantigens prevent tumor escape
- **Consideration:** Driver mutations are typically clonal

**Mutation Type Preferences**
1. **Missense mutations** (most common, single amino acid change)
2. **Frameshift mutations** (can create novel sequences)
3. **Splice variants** (tumor-specific isoforms)
4. **Gene fusions** (highly immunogenic)
5. **Driver mutations** (KRAS, TP53, etc. - may be shared neoantigens)

---

## 2. SECONDARY QUALIFICATION CRITERIA

### A. Tumor Microenvironment Factors

**Tumor Mutational Burden (TMB)**
- High TMB → More neoantigen candidates
- Correlates with checkpoint inhibitor response
- Threshold: > 10 mutations/megabase (high TMB)

**Antigen Processing Machinery**
- Intact proteasome function
- TAP transporter expression
- Tapasin/chaperone proteins
- Loss of processing machinery = vaccine failure

**HLA Expression & Loss**
- Verify HLA alleles not deleted or silenced
- Check for LOH (Loss of Heterozygosity) at HLA locus
- Epigenetic silencing can eliminate presentation

### B. Structural & Biophysical Properties

**Peptide-MHC Complex Energy**
- Rosetta energy scoring of pMHC structure
- Lower energy → More stable complex
- Structural modeling reveals TCR-exposed residues

**Hydrophobicity Profile**
- Optimal hydrophobicity at TCR contact positions
- Too hydrophobic → Poor solubility
- Too hydrophilic → Weak TCR binding

**Charge Distribution**
- Balanced positive/negative charges
- Exposed charges can enhance TCR binding energy
- Salt bridges stabilize pMHC complex

**Peptide Flexibility**
- Moderate flexibility preferred
- Too rigid → Poor MHC binding
- Too flexible → Weak TCR recognition

### C. Clinical & Practical Considerations

**Manufacturing Feasibility (for mRNA vaccines)**
- Sequence length (up to 34 neoantigens per vaccine for Moderna)
- GC content (affects mRNA stability)
- RNA secondary structures (avoid complex folding)
- Codon optimization for expression

**Immunodominance Risk**
- Include multiple neoantigens (10-34 per vaccine)
- Reduces risk of tumor escape through antigen loss
- Balances immunodominance effects

**Patient-Specific HLA Typing**
- Accurate HLA genotyping (4-digit resolution minimum)
- Consider all expressed HLA alleles (A, B, C for Class I)
- Include HLA-DRB1, DQB1 for Class II presentation

---

## 3. MODERNA'S mRNA-4157 APPROACH (Case Study)

### Vaccine Design Strategy

**Neoantigen Selection Pipeline:**
1. **Whole Exome Sequencing** of tumor + matched normal
2. **RNA-Seq** for expression validation
3. **Computational Prediction:**
   - Validated neoantigens (experimentally confirmed)
   - Predicted neoepitopes (high-confidence)
   - Driver gene mutations (KRAS, TP53, etc.)

**Vaccine Structure:**
- **Single mRNA construct** encoding up to 34 neoantigens
- **27-mer peptides** (span mutation, allow both MHC-I and MHC-II presentation)
- **Lipid nanoparticle (LNP) delivery** for DC targeting
- **Combination with pembrolizumab** (checkpoint inhibitor)

**Key Results (KEYNOTE-942 Trial):**
- 44% reduction in recurrence risk (melanoma)
- 60% overall immunogenicity rate
- Majority de novo T cell responses (not pre-existing)
- Both CD4+ and CD8+ responses generated
- FDA Breakthrough Designation granted

---

## 4. VALIDATION & PRIORITIZATION WORKFLOW

### Step 1: Computational Screening (Thousands → Hundreds)

**Initial Filters:**
```
✓ MHC binding affinity < 500 nM
✓ Gene expression > 10 TPM
✓ VAF > 0.25
✓ Mutation in expressed HLA allele
✓ Not in germline (tumor-specific)
```

**Immunogenicity Scoring:**
```
Score = f(MHC_binding, Presentation, DAI, Foreignness, Expression)
```

**Output:** Top 100-200 candidates per patient

### Step 2: Structural & Bioinformatics Refinement (Hundreds → Dozens)

**Advanced Filters:**
```
✓ High presentation probability
✓ Optimal peptide position (mutation central)
✓ Good hydrophobicity profile
✓ Clonal mutation (not subclonal)
✓ Processing & proteasomal cleavage predicted
```

**Output:** Top 30-50 high-confidence candidates

### Step 3: Experimental Validation (Dozens → Final Selection)

**Mass Spectrometry (Immunopeptidomics)**
- Directly detect peptide presentation on tumor cells
- Gold standard but technically challenging
- Confirms computational predictions

**T Cell Assays**
- ELISpot (IFN-γ release)
- Tetramer/multimer staining
- In vitro T cell expansion
- Patient-derived TILs or PBMCs

**Functional Testing**
- Tumor cell killing assays
- Cytokine production profiles
- T cell proliferation

**Output:** Final 10-34 validated neoantigens for vaccine

### Step 4: Vaccine Formulation

**Inclusion Criteria:**
- **Validated immunogenic neoantigens** (if available)
- **High-scoring predicted neoantigens** (computational)
- **Driver mutations** (shared potential, clonal)
- **Diverse HLA coverage** (multiple alleles)
- **Both MHC-I and MHC-II epitopes**

---

## 5. KEY DECISION MATRICES

### Matrix 1: Mutation Type Priority

| Mutation Type | Priority | Rationale |
|---------------|----------|-----------|
| Clonal driver mutations | ★★★★★ | Present in all cells, shared antigens possible |
| Clonal passenger mutations | ★★★★☆ | Patient-specific, prevents escape |
| Frameshift indels | ★★★★☆ | Creates novel sequences, highly foreign |
| Gene fusions | ★★★★☆ | Highly immunogenic, tumor-specific |
| Splice variants | ★★★☆☆ | Alternative processing, specific |
| Subclonal mutations | ★★☆☆☆ | Risk of tumor escape, lower priority |

### Matrix 2: Immunogenicity Feature Weighting

| Feature | Weight | Notes |
|---------|--------|-------|
| MHC binding affinity | 0.20 | Necessary threshold |
| Presentation probability | 0.20 | Critical for surface display |
| Expression level | 0.15 | Must be transcribed |
| DAI (foreignness vs WT) | 0.15 | Differential recognition |
| Clonality (VAF) | 0.10 | Prevents escape |
| Structural stability | 0.10 | Persistent presentation |
| Similarity to pathogens | 0.10 | Cross-reactive T cells |

### Matrix 3: Filtering Cascade

```
Initial candidates:        ~10,000 non-synonymous mutations
↓ [Expressed in tumor]     ~1,000 mutations
↓ [MHC binding < 500nM]    ~200-300 peptides
↓ [High presentation]      ~100-150 peptides
↓ [Immunogenicity score]   ~50-80 peptides
↓ [Clonality + DAI]        ~30-40 peptides
↓ [Experimental validation] ~10-34 final neoantigens
```

---

## 6. COMMON PITFALLS & SOLUTIONS

### Pitfall 1: Over-Reliance on Binding Affinity
**Problem:** 51% AUC for predicting immunogenicity from binding alone
**Solution:** Integrate presentation, expression, and TCR recognition features

### Pitfall 2: Ignoring Central Tolerance
**Problem:** High similarity to self → T cell deletion during development
**Solution:** Prioritize neoantigens dissimilar to normal proteome

### Pitfall 3: Subclonal Mutations
**Problem:** Only present in subset of tumor cells → escape variants
**Solution:** Focus on clonal mutations with high VAF

### Pitfall 4: HLA Loss
**Problem:** Tumor loses HLA expression → no presentation
**Solution:** Verify HLA expression via RNA-seq or flow cytometry

### Pitfall 5: Immunodominance
**Problem:** T cells respond to only 1-2 of many neoantigens
**Solution:** Include 20-34 diverse neoantigens, expect ~60% response rate

### Pitfall 6: Peptide Processing Failures
**Problem:** Peptide never cleaved from protein or transported
**Solution:** Predict proteasomal cleavage, TAP transport efficiency

---

## 7. ADVANCED TOOLS & PLATFORMS

### Bioinformatics Pipelines
- **pVACtools** (comprehensive suite)
- **Vaxrank** (ranking and selection)
- **MuPeXI** (mutation → epitope prediction)
- **TSNAD** (tumor-specific neoantigen detection)
- **NeoaPred** (deep learning immunogenicity)

### Machine Learning Models
- **PRIME** (logistic regression immunogenicity)
- **DeepImmuno** (deep learning fine-tuning)
- **DeepHLApan** (pan-HLA immunogenicity)
- **BigMHC** (transfer learning on immunogenicity)
- **NUCC** (CNN+FCNN with stability features)

### Experimental Platforms
- **Mass spectrometry** (direct peptide detection)
- **MHC multimer assays** (T cell binding)
- **Single-cell RNA-seq** (TCR identification)
- **Patient-derived organoids** (functional testing)

---

## 8. QUALITY CONTROL METRICS

### Pre-Manufacturing QC
```
✓ Minimum 10 neoantigens selected
✓ At least 50% predicted immunogenic
✓ Coverage of multiple HLA alleles
✓ No overlap with normal tissue expression
✓ Manufacturing feasibility confirmed
```

### Post-Vaccination Monitoring
```
✓ Vaccine-specific T cell responses (ELISpot)
✓ T cell expansion in blood (tetramer+)
✓ Cytokine profiles (IFN-γ, TNF-α)
✓ Clinical response (imaging)
✓ Tumor biopsy (on-treatment, if feasible)
```

---

## 9. COMBINATION STRATEGIES

### Synergistic Approaches

**With Checkpoint Inhibitors (Standard)**
- PD-1/PD-L1 blockade (pembrolizumab, nivolumab)
- Enhances T cell activation and persistence
- 44% improvement in RFS (Moderna data)

**With Chemotherapy**
- Increases tumor mutation burden
- Induces immunogenic cell death
- Creates new neoantigens

**With Radiation**
- Abscopal effect
- Enhanced antigen release
- Immunogenic cell death

**With Adjuvants**
- Poly-ICLC (most common in trials)
- GM-CSF (sargramostim)
- TLR agonists
- Enhances DC activation

---

## 10. REGULATORY & CLINICAL CONSIDERATIONS

### FDA Requirements
- Breakthrough designation criteria (Moderna achieved this)
- Personalized medicine considerations
- CMC (Chemistry, Manufacturing, Controls) for individualized products
- Potency assays for immune response
- Safety monitoring for autoimmunity

### Clinical Trial Design
- Patient selection criteria:
  - High TMB preferred
  - Intact immune system
  - No active autoimmune disease
  - Sufficient tumor tissue for sequencing
  
- Timeline constraints:
  - Sequencing → Analysis: 2-4 weeks
  - Manufacturing: 4-8 weeks
  - Treatment window critical

### Success Metrics
- **Immunogenicity:** 60% response rate (Moderna benchmark)
- **Clinical efficacy:** 44% reduction in recurrence (melanoma)
- **Safety:** Low grade adverse events acceptable
- **Duration:** Durable responses (12-23+ months)

---

## 11. FUTURE DIRECTIONS

### Emerging Technologies
- **AI/ML models** with structural features
- **AlphaFold** for pMHC structure prediction
- **Single-cell multi-omics** for TCR-epitope mapping
- **CRISPR screens** for neoantigen validation
- **In silico patient avatars** for personalized prediction

### Expanded Targets
- **Shared neoantigens** (driver mutations across patients)
- **Endogenous retroelements** (viral-like sequences)
- **Tumor-specific splicing** (neo-junctions)
- **Post-translational modifications** (phosphorylation, glycosylation)
- **MHC-II neoantigens** (CD4+ T cell activation)

---

## 12. PRACTICAL CHECKLIST FOR RESEARCHERS

### Essential Qualification Criteria
```
□ MHC-I binding affinity < 500 nM (NetMHCpan)
□ High presentation probability (MixMHCpred)
□ Tumor-specific expression > 10 TPM
□ Clonal mutation (VAF > 0.3)
□ Differential binding vs WT (DAI > 0)
□ Low self-similarity (DisToSelf)
□ Patient HLA-matched
□ Processable by proteasome
□ Stable pMHC complex
□ Experimentally validated (if possible)
□ Manufacturing compatible
□ Multiple neoantigens per vaccine (10-34)
```

### Red Flags (Disqualifiers)
```
✗ Germline mutation (not tumor-specific)
✗ Not expressed (TPM < 1)
✗ HLA allele deleted/silenced in tumor
✗ Identical to normal proteome
✗ Poor manufacturing feasibility
✗ Subclonal with VAF < 0.1
✗ No detectable T cell response in validation
```

---

## 13. SUMMARY: THE QUALIFICATION PYRAMID

```
                    CLINICAL EFFICACY
                   (10-34 neoantigens)
                  ↑
              EXPERIMENTAL VALIDATION
            (Mass spec + T cell assays)
           (30-50 candidates)
          ↑
      BIOINFORMATICS REFINEMENT
    (Structure, processing, clonality)
   (100-200 candidates)
  ↑
COMPUTATIONAL SCREENING
(MHC binding, expression, immunogenicity)
(1,000-10,000 mutations)
```

**Bottom Line:** Less than 3% of predicted neoantigens are truly immunogenic. Comprehensive multi-parameter screening with experimental validation is essential for successful personalized cancer vaccine development.

---

## 14. RECOMMENDED READING

### Key Publications
1. Wells et al. (2020) Cell - TESLA consortium key parameters
2. Sahin et al. (2017) Nature - Moderna/BioNTech melanoma trial
3. Hu et al. (2021) Nat Med - mRNA cancer vaccines review
4. Richman et al. (2019) Cell - Neoantigen dissimilarity
5. Łuksza et al. (2017) Nature - Neoantigen fitness model

### Resources
- IEDB (Immune Epitope Database)
- TumorAgDB (tumor neoantigen database)
- TESLA database (consortium data)
- NetMHCpan tools suite
- pVACtools documentation

---

**Document Version:** 1.0  
**Last Updated:** October 2025  
**Intended Audience:** Researchers at pharmaceutical/biotech companies developing personalized neoantigen vaccines

---

For questions or updates, this represents current best practices as of late 2025 based on published clinical trials and computational approaches.
