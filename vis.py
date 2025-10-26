import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import random 
    import pandas as pd
    return mo, pd, random


@app.cell
def _(mo):
    mo.md("""
    # :rocket: Welcome to **NeoRefine**
    A next-generation platform for **peptide generation**.
    """)
    return


@app.cell
def _(mo):
    file_uploader = mo.ui.file(filetypes=[".fastq"], multiple=True, label="Upload your tumor RNA-seq FastQ files:")
    return (file_uploader,)


@app.cell
def _(file_uploader):
    file_uploader
    return


@app.cell
def _(mo):
    txt = mo.md("""
    ### 🧬 The HLA Alleles Are

    HLA-A: A*02:01 / A*24:02  
    HLA-B: B*07:02 / B*15:01  
    HLA-C: C*07:02 / C*03:04
    """)

    txt
    return


@app.cell
def _(generate_synthetic_peptide_data2):
    data = generate_synthetic_peptide_data2()
    return (data,)


@app.cell
def _(data, mo):
    table = mo.ui.table(data)
    return (table,)


@app.cell
def _(mo, table):
    mo.vstack([
        mo.md("## **Data Analysis**"),  # Bigger label
        table
    ])
    return


@app.cell
def _(mo, table):
    mo.md(f"""
    The sequence **{table.value["Peptide_Sequence"].values[0]}** exhibits a dominant hydrophobic core typical of transmembrane or cytosolic proteins processed through the MHC-I pathway. Its strong HLA-A*02:01 binding potential makes it a good immunogenic candidate; however, its hydrophobicity poses formulation challenges. Expect aggregation during lyophilization or storage, requiring carrier conjugation (e.g., KLH or PEG) to maintain solubility. Commercial scaling would need optimized solvent systems and purification gradients.
    """) if table.value["Peptide_Sequence"].values.any() else mo.md("")



    return


@app.cell
def _(pd, random):

    AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY'
    def generate_peptide_sequence(length):
        """Generate a random peptide sequence of specified length."""
        return ''.join(random.choice(AMINO_ACIDS) for _ in range(length))

    def generate_synthetic_peptide_data(num_sequences=100):
        """Generate synthetic peptide data with sequences and abundances."""
        data = {
            'Peptide_Sequence': [],
            'Abundance': [],
            'Length': []
        }
    
        for _ in range(num_sequences):
            # Random length between 8 and 11
            length = random.randint(8, 11)
            sequence = generate_peptide_sequence(length)
            # Generate abundance (log-normal distribution for realistic spread)
            abundance = round(random.lognormvariate(mu=10, sigma=2), 2)
        
            data['Peptide_Sequence'].append(sequence)
            data['Abundance'].append(abundance)
            data['Length'].append(length)
    
        # Create DataFrame
        df = pd.DataFrame(data)
        return df

    return


@app.cell
def _(pd, random):
    AMINO_ACIDS2 = 'ACDEFGHIKLMNPQRSTVWY'
    KYTE_DOITTLE2 = {
        'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8, 'G': -0.4, 'H': -3.2,
        'I': 4.5, 'K': -3.9, 'L': 3.8, 'M': 1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5,
        'R': -4.5, 'S': -0.8, 'T': -0.7, 'V': 4.2, 'W': 0.9, 'Y': -1.3
    }

    # Tissue expression options
    TISSUES = [
        'ubiquitous (low level)', 'ubiquitous (low level)', 'ubiquitous (low level)',
        'thyroid', 'mucosa, keratinocytes', 'mucosa, keratinocytes',
        'testis, prostate', 'testis, prostate'
    ]

    def generate_peptide_sequence2(length):
        """Generate a random peptide sequence of specified length."""
        return ''.join(random.choice(AMINO_ACIDS2) for _ in range(length))

    def calculate_hydrophobicity2(sequence):
        """Calculate average hydrophobicity of a peptide sequence."""
        return round(sum(KYTE_DOITTLE2[aa] for aa in sequence) / len(sequence), 2)

    def generate_synthetic_peptide_data2(num_sequences=100):
        """Generate synthetic peptide data with sequences, abundances, immunogenicity, hydrophobicity, and tissue."""
        data = {
            'Peptide_Sequence': [],
            'Abundance': [],
            'Length': [],
            'Immunogenicity': [],
            'Hydrophobicity': [],
            'Tissue_Expression': []
        }
    
        for _ in range(num_sequences):
            # Random length between 8 and 11
            length = random.randint(8, 11)
            sequence = generate_peptide_sequence2(length)
            # Generate abundance (log-normal distribution)
            abundance = round(random.lognormvariate(mu=10, sigma=2), 2)
            # Immunogenicity: 20% chance of being immunogenic (1), 80% non-immunogenic (0)
            immunogenicity = random.choices([0, 1], weights=[0.8, 0.2])[0]
            # Calculate hydrophobicity
            hydrophobicity = calculate_hydrophobicity2(sequence)
            # Random tissue from provided list
            tissue = random.choice(TISSUES)
        
            data['Peptide_Sequence'].append(sequence)
            data['Abundance'].append(abundance)
            data['Length'].append(length)
            data['Immunogenicity'].append(immunogenicity)
            data['Hydrophobicity'].append(hydrophobicity)
            data['Tissue_Expression'].append(tissue)
    
        # Create DataFrame
        df = pd.DataFrame(data)
        return df
    return (generate_synthetic_peptide_data2,)


if __name__ == "__main__":
    app.run()
