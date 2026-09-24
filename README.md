# AI-Agent---Data-Processing-Pipeline

# Pump Metadata Enrichment with Local LLM

This project explores using a local Hugging Face language model to enrich pump records with short natural-language summaries based on each pump's ID, name, and code.

The current workflow reads a CSV of pump records, sends each row to a small local model, and writes the generated output back into a new CSV file. It is designed as a lightweight personal data-enrichment prototype rather than a production pipeline.

## Project goal

The aim is to turn a raw pump dataset into a more informative dataset by generating fields such as:

- likely use or function
- approximate capacity
- likely location
- general operational notes

This is especially useful when the dataset has sparse descriptive metadata and you want to generate an initial enrichment layer before further analysis.

## Main script

The active project script is:

- `pumps_model_AI.py`

This is the main processing script and the one to use as the repository's core entry point.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── pumps_model_3.py          # main script
├── water_pumps.csv           # source pump CSV
└── .venv/                    # local virtual environment (not usually committed)
```

## How it works

1. A CSV file is loaded.
2. Each pump row is processed one at a time.
3. A prompt is assembled using the pump's ID, name, and code.
4. A local LLM model is used to generate a short summary.
5. The generated summary is appended back into the dataframe.
6. The enriched dataset is exported as a CSV.

## Current script behaviour

The script currently uses:

- model: `LiquidAI/LFM2.5-230M`
- framework: `transformers`
- device: CUDA if available, otherwise CPU

This model was chosen for its lightweight nature, running comfortably on my Intel I5 CPU. The full run however, can take a very long time. 

It expects a CSV containing pump metadata and writes the output as:

- `pumps_with_data.csv`

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

If you want to install the packages manually, the project currently expects:

```powershell
pip install transformers torch pandas
```

## Running the main script

From the repository root:

```powershell
python pumps_model_3.py
```

## Important note about the CSV path

The script currently contains a hardcoded filename:

```python
CSV_FILE = "water_pumps.csv"
```

At the moment, the project folder contains `pumps_raw_crop.csv`, so you will need to either:

- rename the file to `water_pumps.csv`, or
- update the value in `pumps_model_3.py` to match your actual file name

Example:

```python
CSV_FILE = "pumps_raw_crop.csv"
```

## Example output

The script appends a generated text field to the dataframe, such as:

```text
extracted_info
```

This field may contain a model-generated summary like:

> This pump is likely used for water transfer and drainage operations in the region, with a typical capacity in the moderate municipal or industrial range. It is likely located in Zuid-Holland and associated with local water management infrastructure.

## Limitations

This project is a prototype and has a few important limitations:

- it depends on a relatively large local model and may be slow on CPU
- the script is hardcoded to specific filenames and model settings
- the generated text is best treated as a first-pass enrichment, not a verified engineering fact source
- output quality depends heavily on model choice, prompt wording, and dataset quality

## Good use cases

This repo is suitable for:

- personal experimentation
- data enrichment prototypes
- exploratory AI + spreadsheet workflows
- learning how to build a small local LLM pipeline
