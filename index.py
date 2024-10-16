import streamlit as st
import math

# Constants for calculations
ENERGY_PER_USE_GPT4 = 0.04845  # kWh
ENERGY_PER_USE_GPT4_MINI = 0.0004845  # kWh
PUE = 1.125
CARBON_INTENSITY = 0.5  # kg CO2 per kWh (example value, adjust as needed)
PHONE_CHARGE_ENERGY = 0.00963  # kWh
LED_BULB_POWER = 0.007  # kW
GOOGLE_SEARCH_ENERGY = 0.0003  # kWh per search
CAR_EFFICIENCY = 0.2  # kWh per km (example value, adjust as needed)

def calculate_co2(prompts, model, generation_type, complexity, months):
    # Adjust energy based on model and complexity
    energy_per_use = ENERGY_PER_USE_GPT4 if model == 'ChatGPT-4' else ENERGY_PER_USE_GPT4_MINI
    if complexity == 'Medium':
        energy_per_use *= 1.5
    elif complexity == 'Høj':
        energy_per_use *= 2

    # Adjust for image generation if applicable
    if generation_type == 'Billedgenerering':
        energy_per_use *= 2  # Assume image generation uses twice the energy

    # Calculate total energy and CO2
    total_energy = prompts * energy_per_use * PUE * months
    total_co2 = total_energy * CARBON_INTENSITY

    # Calculate equivalent metrics
    phone_charges = math.floor(total_energy / PHONE_CHARGE_ENERGY)
    led_hours = math.floor(total_energy / LED_BULB_POWER)
    google_searches = math.floor(total_energy / GOOGLE_SEARCH_ENERGY)
    driving_distance = math.floor(total_energy / CAR_EFFICIENCY)

    return {
        'totalEnergy': round(total_energy, 2),
        'totalCO2': round(total_co2, 2),
        'phoneCharges': phone_charges,
        'ledHours': led_hours,
        'googleSearches': google_searches,
        'drivingDistance': driving_distance
    }

def main():
    st.set_page_config(page_title="AICarbonCalc", page_icon="🌿")

    st.title("AICarbonCalc - CO2 Beregner")

    st.write("Beregn dit CO2-udslip fra brugen af AI")

    prompts = st.number_input("Antal prompts om måneden", min_value=1, value=100)
    model = st.selectbox("Vælg AI-model", ["ChatGPT-4", "ChatGPT-4 Mini"])
    generation_type = st.selectbox("Vælg AI-genereringstype", ["Text-generation", "Billedgenerering"])
    complexity = st.select_slider("Vælg kompleksitet af dine prompts", options=["Lav", "Medium", "Høj"])
    months = st.slider("Vælg antal måneder", min_value=1, max_value=12, value=1)

    if st.button("Beregn CO2"):
        results = calculate_co2(prompts, model, generation_type, complexity, months)

        st.subheader("Resultater")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total energiforbrug", f"{results['totalEnergy']} kWh")
            st.metric("CO2-udledning", f"{results['totalCO2']} kg")

        with col2:
            st.metric("Mobilopladninger", f"{results['phoneCharges']} stk")
            st.metric("LED-pære brændetid", f"{results['ledHours']} timer")

        st.metric("Ækvivalent antal Google-søgninger", f"{results['googleSearches']} søgninger")
        st.metric("Ækvivalent kørsel i benzinbil", f"{results['drivingDistance']} km")

    st.sidebar.header("Om AICarbonCalc")
    st.sidebar.write("""
    AICarbonCalc er et værktøj til at estimere CO2-udledningen fra brug af AI-modeller.
    Beregningerne er baserede på gennemsnitsværdier og skal ses som vejledende estimater.
    """)

    st.sidebar.header("Sådan bruger du beregneren")
    st.sidebar.write("""
    1. Indtast antallet af prompts du bruger månedligt
    2. Vælg AI-model
    3. Vælg om du genererer tekst eller billeder
    4. Angiv kompleksiteten af dine prompts
    5. Vælg antal måneder du vil beregne for
    6. Klik på "Beregn CO2" for at se resultatet
    """)

if __name__ == "__main__":
    main()