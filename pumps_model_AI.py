##  csv integration loop 

import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "LiquidAI/LFM2.5-230M"
CSV_FILE = "water_pumps.csv"  
OUTPUT_CSV = "pumps_with_data.csv"
MAX_NEW_TOKENS = 500


# setup device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading model on {device}...")

# load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)

# load csv
df = pd.read_csv(CSV_FILE)
print(f"Loaded {len(df)} pumps.")

# new lsit for restults 
extracted_data = []

# loop through each row 

# new list for results 
extracted_data = []

# loop through each row 
for index, row in df.iterrows():
    pump_id = row.get('id', 'Unknown')
    pump_name = row.get('naam', 'Unknown')
    pump_code = row.get('code', 'Unknown')

    # create prompt for the model (INDENTED)
    messages = [
        {"role": "system", "content": "You are a precise data extraction assistant. Given a pump ID and name, provide a short summary of its likely function, location (Zuid-Holland), and any operational details based on general knowledge."},
        {"role": "user", "content": f"Pump ID: {pump_id}, Name: {pump_name}, Code: {pump_code}. What is this pump used for? What is its maximum capacity? Where is it located? Provide a concise summary."}
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(device)

    outputs = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)

    # decode only the generated part (INDENTED)
    response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
        
    extracted_data.append(response)
    print(f"Processed {index+1}/{len(df)}: {pump_name}")

# Outside the loop: save to CSV
df['extracted_info'] = extracted_data
df.to_csv(OUTPUT_CSV, index=False)
print(f"Done! Results saved to {OUTPUT_CSV}")