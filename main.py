import pandas as pd
import matplotlib.pyplot as plt
from google import genai
import os 

print("--- AI + GRAPHICAL DATA ANALYST STARTING... ---\n")

# SETTING UP GEMINI API KEY 
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
try:
    print("1. LOADING DATA")
    df = pd.read_csv(url)
    
    num_cars = len(df)
    avg_consumption = df["mpg"].mean()
    h_power_country = df.groupby("origin")["horsepower"].mean().sort_values(ascending=False)
    
    # GRAPH
    print("2. Generating graph...")
    plt.figure(figsize=(8, 5)) 
    
    # Bar chart (Modré odstíny)
    h_power_country.plot(kind="bar", color=["#3c00ff", "#001eff", "#00bbff"])
    
    plt.title("Average engine power by country of origin (in horsepower)", fontsize=14, fontweight="bold")
    plt.xlabel("Country of origin", fontsize=12)
    plt.ylabel("Engine power (Horsepower)", fontsize=12)
    plt.xticks(rotation=0) 
    plt.grid(axis="y", linestyle="--", alpha=0.7) 
    
    # Saving graph
    plt.savefig("horsepower_graph.png", dpi=300, bbox_inches="tight")
    plt.close() 
    print("-> Graph successfully saved as 'horsepower_graph.png'")
    
    # 3. PROMPT FOR GEMINI AI (Kompletně v angličtině)
    prompt_ai = f"""
    You are a top-tier business analyst. Analyze this automobile dataset and write a brief,
    professional executive summary report in English for the CEO of our automotive company.
    Mention in the text that you have also generated a chart named 'horsepower_graph.png', 
    which is attached to this report.
    
    Dataset Statistics:
    - Total number of analyzed cars: {num_cars}
    - Fleet average fuel economy: {avg_consumption:.2f} MPG
    - Average horsepower by country of origin:
      * USA: {h_power_country['usa']:.1f} HP
      * Europe: {h_power_country['europe']:.1f} HP
      * Japan: {h_power_country['japan']:.1f} HP
    """
    
    print("3. Sending data to Google Gemini AI...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_ai,
    )
    
    # 4. SAVING THE REPORT
    with open("zivy_manazersky_report.txt", "w", encoding="utf-8") as soubor:
        soubor.write(response.text)
        
    print("\n DONE! English text report and graphical chart successfully created!")

except Exception as e:
    print(f"\nAn error occurred: {e}")

print("\n--------------------------------------------")