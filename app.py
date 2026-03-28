import streamlit as st
import math
import math
import pandas as pd
from fpdf import FPDF  
from datetime import datetime  
import os

# Page configuration
st.set_page_config(
    page_title="UPV Reinforcement Correction Tool",
    layout="wide"
)

# Header
st.markdown("""
### THIAGARAJAR COLLEGE OF ENGINEERING  
Thiruparankundram, Madurai  

**Department of Civil Engineering**  

#### Evaluation of Rebar-Induced Disturbances in Ultrasonic Pulse Velocity Measurements of Reinforced Concrete

👨‍💻 **Developed by**

• **Dr. S. Arul Mary** – 📞 +91 9486459732 – 📧 samcivil@tce.edu  
• **Ananda Rao B K K** – 📞 +91 9361951527 – 📧 anandarao242004@gmail.com  
• **Kathir Nivas P** – 📞 +91 6383402262 – 📧 kathirnivas@student.tce.edu  
• **Dharshini M** – 📞 +91 9361835809 – 📧 dharshini@student.tce.edu  

---
""")

st.title("Ultrasonic Pulse Velocity (UPV) Observation")

# Sidebar
# Main Sidebar Title
st.sidebar.title("UPV Corrections")

# 1. Select the Method
correction_method = st.sidebar.radio(
    "Select Correction Orientation",
    ["No Correction", "Parallel to the Rebar", "Perpendicular to the Bar"]
)

# 2. The Guidelines Expander (The box in the corner)
with st.sidebar.expander("📖 User Guidelines & Formulas"):
    st.markdown("""
    ### Project Overview
    Evaluating **Rebar-Induced Disturbances** in UPV measurements for Concrete Quality.
    
    ### Notations:
    * **Vc**: Corrected Velocity (km/s)
    * **Vs**: Steel Velocity (Fixed at 5.2 km/s)
    * **a**: Offset distance (mm)
    * **T**: Transit time (µs)
    * **L**: Path Length (mm)
    * **Vm**: Measured Velocity in Upv Appartus(km/s)
    * **K**: Correction Factor 
    * **Vc**: = K * Vm 
                
                
    
    ### References:
    * **1**: British standards 1881:1986 part 203
    * **2**: NDT Hand Book by Malhotra
    * **3**: Non destructive Testing IS 1331:1992 part 1     
    """)

    st.markdown("""
    ### References:
    * **1**: British standards 1881:1986 part 203
    * **2**: NDT Hand Book by Malhotra
    * **3**: Non destructive Testing IS 1331:1992 part 1     
    """)

    # --- ATTACHING EXISTING DESKTOP PDF ---
    import os

    # The file name must match what is in your folder
    local_pdf_path = "user.pdf" 

    if os.path.exists(local_pdf_path):
        with open(local_pdf_path, "rb") as f:
            pdf_bytes = f.read()
        
        st.download_button(
            label="📄 Download Guidelines PDF",
            data=pdf_bytes,
            file_name="UPV_User_Guidelines.pdf",
            mime="application/pdf"
        )
    else:
        st.error(f"⚠️ Error: '{local_pdf_path}' not found in the project folder.")
        st.info("Please move the 'user.pdf' from your Desktop into the same folder where your Python script is saved.")

# --- 4. MAIN INPUT VALUES ---
st.subheader("Input Values")
# (Your number_inputs with keys go here)
# Input values
st.subheader("Input Values")

path_length_mm = st.number_input("Path Length (mm)", min_value=1.0, value=150.0)
time_micro = st.number_input("Pulse Time (microseconds)", min_value=1.0, value=35.0)

# Unit conversions
path_length_km = path_length_mm / 1_000_000
time_seconds = time_micro / 1_000_000

# Velocity calculation
velocity = path_length_km / time_seconds

# Converted values
st.subheader("Converted Values")

st.write(f"Path Length: {path_length_km:.6f} km")
st.write(f"Time: {time_seconds:.6f} seconds")

# Result
st.subheader("Measured Velocity")

st.write(f"Velocity = {velocity:.3f} km/sec")

# Concrete quality classification
st.subheader("Concrete Quality")

if velocity > 4.5:
    st.success("Concrete Quality: Excellent")
elif velocity >= 3.5:
    st.info("Concrete Quality: Good")
elif velocity >= 3.0:
    st.warning("Concrete Quality: Medium")
else:
    st.error("Concrete Quality: Doubtful")

# Reference table
st.subheader("Velocity Criteria for Concrete Quality")

st.table({
    "Velocity (km/sec)": ["> 4.5", "3.5 – 4.5", "3.0 – 3.5", "< 3.0"],
    "Quality": ["Excellent", "Good", "Medium", "Doubtful"]
})
# -------------------------------
# No Correction
# -------------------------------

if correction_method == "No Correction":

    st.subheader("Measured Ultrasonic Pulse Velocity")

    st.success(f"Measured Pulse Velocity = {velocity:.3f} km/sec")

    st.subheader("Concrete Quality")

    if velocity > 4.5:
        st.success("Concrete Quality: Excellent")
    elif velocity >= 3.5:
        st.info("Concrete Quality: Good")
    elif velocity >= 3.0:
        st.warning("Concrete Quality: Medium")
    else:
        st.error("Concrete Quality: Doubtful")

elif correction_method == "Perpendicular to the Bar":
    st.subheader("Correction: Perpendicular to the Bar")

    # Inputs
    L_val = path_length_mm        # mm
    T_us = time_micro             # microseconds

    st.info(f"Using Values: Path Length = {L_val} mm, Transit Time = {T_us} µs")

    # Bar diameter
    Ls_val = st.number_input("Enter Bar Diameter (Ls) in mm", min_value=1.0, value=12.0)

    Vs = 5.2  # km/s

    # Unit conversion
    L_km = L_val / 1_000_000
    T_sec = T_us / 1_000_000

    # Measured velocity
    V_measured = L_km / T_sec if T_sec != 0 else 0

    # Corrected velocity
    numerator = V_measured * (L_val - Ls_val)
    denominator = L_val - (V_measured * (Ls_val / Vs))

    if denominator != 0:
        v_corrected = numerator / denominator
    else:
        v_corrected = 0.0

    # Gamma and k
    gamma = v_corrected / Vs if Vs != 0 else 0
    k_factor = v_corrected / V_measured if V_measured != 0 else 0

    # Display results
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Measured Velocity (Vm)", f"{V_measured:.3f} km/s")
    with col2:
        st.metric("Gamma (γ)", f"{gamma:.4f}")
    with col3:
        st.metric("Correction Factor (k)", f"{k_factor:.4f}")

    st.success(f"Corrected Velocity (Vc) = {v_corrected:.3f} km/s")

    # ✅ IMPORTANT: DEFINE quality_str HERE
    st.subheader("Concrete Quality Assessment")

    if v_corrected > 4.5:
        st.success("Concrete Quality: Excellent")
        quality_str = "Excellent"
    elif v_corrected >= 3.5:
        st.info("Concrete Quality: Good")
        quality_str = "Good"
    elif v_corrected >= 3.0:
        st.warning("Concrete Quality: Medium")
        quality_str = "Medium"
    else:
        st.error("Concrete Quality: Doubtful")
        quality_str = "Doubtful"

    # ✅ PDF BUTTON (NOW IT WILL WORK)
if st.button("📄 Generate Perpendicular PDF", key="perp_pdf_btn"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "THIAGARAJAR COLLEGE OF ENGINEERING", ln=True, align='C')

    pdf.set_font("Arial", 'I', 11)
    pdf.cell(190, 8, "Department of Civil Engineering - Madurai", ln=True, align='C')

    pdf.ln(8)

    # Title
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(190, 10, "Ultrasonic Pulse Velocity (UPV) Reinforcement Correction Report", ln=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(190, 8, f"Date of Analysis: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)

    pdf.ln(5)

    # Section 1
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 8, "1. Test Parameters", ln=True, fill=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(190, 8, f"Correction Method: Perpendicular to Rebar", ln=True)
    pdf.cell(190, 8, f"Path Length (L): {L_val} mm", ln=True)
    pdf.cell(190, 8, f"Transit Time (T): {T_us} micro-seconds", ln=True)
    pdf.cell(190, 8, f"Bar Diameter (Ls): {Ls_val} mm", ln=True)

    pdf.ln(4)

    # Section 2
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 8, "2. Calculation Results", ln=True, fill=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(190, 8, f"Measured Velocity (Vm): {V_measured:.3f} km/sec", ln=True)
    pdf.cell(190, 8, f"Correction Factor (k): {k_factor:.4f}", ln=True)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, f"Corrected Velocity (Vc): {v_corrected:.3f} km/sec", ln=True)

    pdf.cell(190, 8, f"Concrete Quality: {quality_str}", ln=True)

    # Output
    pdf_output = pdf.output(dest='S').encode('latin-1')

    st.download_button(
        "Download PDF Report",
        data=pdf_output,
        file_name="UPV_Perpendicular_Report.pdf",
        mime="application/pdf"
        
    )
    
elif correction_method == "Parallel to the Rebar":
    st.subheader("Correction: Parallel to the Rebar")

    # 1. Inputs unique to Parallel Mode
    a_dist = st.number_input("Enter Offset Distance (a) in mm", min_value=0.1, value=40.0, step=1.0)
    Vs = 5.2 # Constant for Steel Velocity

    # 2. Safe Data Retrieval from Main Inputs
    # This uses .get() to prevent the "AttributeError" if the keys aren't initialized
    # Make sure your main inputs have: key="main_transit_time" and key="main_path_length"
    T_us = st.session_state.get("main_transit_time", 32.40)
    L_val = st.session_state.get("main_path_length", 150.0)

    # 3. Calculation Logic
    # Calculate Measured Apparent Velocity (Vm)
    v_measured = L_val / T_us if T_us != 0 else 0 

    # Calculate Corrected Velocity (Vc) using your specific geometric formula
    # Vc = (2 * a * Vs) / sqrt(4*a^2 + (T*Vs - L)^2)
    numerator = 2 * a_dist * Vs
    term_inner = (T_us * Vs) - L_val
    denominator = math.sqrt(4 * (a_dist**2) + (term_inner**2))
    
    if denominator != 0:
        v_corrected = numerator / denominator
    else:
        v_corrected = 0.0

    # Calculate Correction Factor (k) and Gamma (y)
    # k = Vc / Vm (How much we adjust the measured reading)
    k_factor = v_corrected / v_measured if v_measured != 0 else 0.0
    gamma = v_corrected / Vs

    # 4. Display Results (Dashboard Style)
    st.markdown("---")
    
    # Display k and gamma in columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Gamma ($\gamma$)", f"{gamma:.4f}")
    with col2:
        st.metric("Correction Factor ($k$)", f"{k_factor:.4f}")

    st.markdown("---")
    st.write(f"**Synchronized Data:** Path Length = {L_val} mm | Transit Time = {T_us} µs")
    
    if Vs > v_corrected:
        st.success(f"**Corrected Velocity ($V_c$) = {v_corrected:.3f} km/sec**")
    else:
        st.warning("Warning: Condition $V_s > V_c$ not met. Check your input values.")

    # 5. Concrete Quality Check
    st.subheader("Concrete Quality")
    if v_corrected > 4.5:
        st.success("Concrete Quality: Excellent")
    elif v_corrected >= 3.5:
        st.info("Concrete Quality: Good")
    elif v_corrected >= 3.0:
        st.warning("Concrete Quality: Medium")
    else:
        st.error("Concrete Quality: Doubtful")
        from fpdf import FPDF

# --- Generate Technical Report ---
    st.markdown("---")
    st.subheader("Generate Technical Report")

    if st.button("📄 Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        
        # Header: THIAGARAJAR COLLEGE OF ENGINEERING
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 8, txt="THIAGARAJAR COLLEGE OF ENGINEERING", ln=True, align='C')
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 6, txt="Department of Civil Engineering - Madurai", ln=True, align='C')
        pdf.ln(10)

        # Title
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Ultrasonic Pulse Velocity (UPV) Reinforcement Correction Report", ln=True, align='L')
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, txt=f"Date of Analysis: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
        pdf.ln(5)

        # Input Data Section
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt="1. Test Parameters", ln=True, fill=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(100, 8, txt=f"Correction Method: Parallel to Rebar", ln=True)
        pdf.cell(100, 8, txt=f"Path Length (L): {L_val} mm", ln=True)
        pdf.cell(100, 8, txt=f"Transit Time (T): {T_us} micro-seconds", ln=True)
        pdf.cell(100, 8, txt=f"Offset Distance (a): {a_dist} mm", ln=True)
        pdf.ln(5)

        # Results Section
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt="2. Calculation Results", ln=True, fill=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(100, 8, txt=f"Measured Velocity (Vm): {v_measured:.3f} km/sec", ln=True)
        pdf.cell(100, 8, txt=f"Correction Factor (k): {k_factor:.4f}", ln=True)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(100, 10, txt=f"Corrected Concrete Velocity (Vc): {v_corrected:.3f} km/sec", ln=True)
        
        # Quality Assessment
        quality = "Excellent" if v_corrected > 4.5 else "Good" if v_corrected >= 3.5 else "Medium" if v_corrected >= 3.0 else "Doubtful"
        pdf.cell(100, 10, txt=f"Concrete Quality: {quality}", ln=True)

        # Finalize and Download
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(
            label="Download Final PDF",
            data=pdf_output,
            file_name=f"UPV_Correction_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )