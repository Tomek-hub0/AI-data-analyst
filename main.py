import pandas as pd
import matplotlib.pyplot as plt
from google import genai
import os 

print("--- AI + GRAFICKÝ DATOVÝ ANALYTIK SPUŠTĚN ---\n")

# 1. NASTAVENÍ GEMINI API KLÍČE 
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
try:
    print("1. Načítám data o autech...")
    df = pd.read_csv(url)
    
    pocet_aut = len(df)
    prumerna_spotreba = df["mpg"].mean()
    vykon_zeme = df.groupby("origin")["horsepower"].mean().sort_values(ascending=False)
    
    # 2. VYKRESLENÍ A ULOŽENÍ GRAFU
    print("2. Generuji graf výkonu podle zemí...")
    plt.figure(figsize=(8, 5)) # Velikost okna grafu
    
    # Vytvoříme sloupečkový graf (bar) s pěknými barvami
    vykon_zeme.plot(kind="bar", color=["#e74c3c", "#3498db", "#2ecc71"])
    
    plt.title("Průměrný výkon motoru podle země původu (v koních)", fontsize=14, fontweight="bold")
    plt.xlabel("Země původu", fontsize=12)
    plt.ylabel("Výkon (Horsepower)", fontsize=12)
    plt.xticks(rotation=0) # Aby názvy zemí nebyly nakloněné
    plt.grid(axis="y", linestyle="--", alpha=0.7) # Jemná mřížka na pozadí
    
    # Tímto příkazem graf uložíme jako obrázek na disk
    plt.savefig("vykon_aut_graf.png", dpi=300, bbox_inches="tight")
    plt.close() # Zavřeme graf, aby nezabíral paměť
    print("-> Graf úspěšně uložen jako 'vykon_aut_graf.png'")
    
    # 3. PŘÍPRAVA PRO AI
    zadani_pro_ai = f"""
    Jsi špičkový byznysový analytik. Zanalýzuj tato data o automobilech a napiš z nich stručný 
    manažerský report v češtině pro ředitele naší automobilky.
    Mentionuj v textu, že jsi pro něj vygeneroval i graf 'vykon_aut_graf.png', který najde v příloze.
    
    Statistiky z dat:
    - Celkový počet analyzovaných aut: {pocet_aut}
    - Průměrná spotřeba celé flotily: {prumerna_spotreba:.2f} MPG
    - Průměrný výkon motoru podle země původu:
      * USA: {vykon_zeme['usa']:.1f} koní
      * Evropa: {vykon_zeme['europe']:.1f} koní
      * Japonsko: {vykon_zeme['japan']:.1f} koní
    """
    
    print("3. Posílám data do tvého Google Gemini...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=zadani_pro_ai,
    )
    
    # 4. ULOŽENÍ REPORTU
    with open("zivy_manazersky_report.txt", "w", encoding="utf-8") as soubor:
        soubor.write(response.text)
        
    print("\n HOTOVO! Vytvořen textový report i obrázkový graf!")

except Exception as e:
    print(f"\nNastala chyba: {e}")

print("\n--------------------------------------------")