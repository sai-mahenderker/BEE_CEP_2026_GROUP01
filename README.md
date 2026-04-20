# BEE_CEP_2026_GROUP01
# Superposition Theorem Verifier for Multi-Source DC Circuits

**Course:** A9205 - Basic Electrical Engineering Laboratory (VCE-R25)  
**Class:** I B.Tech. II Semester CSE – F  
**Academic Year:** 2025-2026  
**Institution:** Vardhaman College of Engineering  

---

## 👥 Group Members

| Name | Roll No |
|------|---------|
| T. Rishi | 25881A05AU |
| M. Sai | 25881A05BC |
| M. Pranav | 25881A05AR |

---

## 📌 Problem Description
Verify the Superposition Theorem for a 3-resistor, 2-voltage-source DC circuit
by computing branch voltages and currents using superposition and comparing with
node voltage method results.

## 🔌 Circuit Topology
V1(+) --[R1]--+--[R2]--(+)V2
|
[R3]
|
GND
Node A = junction of R1, R2, R3

## 📐 Mathematical Formulation

**KCL at Node A (Actual Circuit):**
Va × (1/R1 + 1/R2 + 1/R3) = V1/R1 + V2/R2

**Superposition Principle:**
Va_total = Va(due to V1 alone) + Va(due to V2 alone)
I_total  = I(due to V1 alone) + I(due to V2 alone)

**When V1 acts alone (V2 shorted):**
R_eq = R1 + (R2 || R3)
Va'  = V1 × (R2||R3) / (R1 + R2||R3)

**When V2 acts alone (V1 shorted):**
R_eq = R2 + (R1 || R3)
Va'' = V2 × (R1||R3) / (R2 + R1||R3)

## ▶️ How to Run

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Run the program
python src/superposition_verifier.py
```

## 📥 Input & Output Format

**Input (via console):**
- V1 — Voltage Source 1 (Volts)
- V2 — Voltage Source 2 (Volts)
- R1, R2, R3 — Resistances (Ohms)

**Output:**
- Step-by-step superposition calculations
- Node voltage and branch currents
- Verification table (Superposition vs Actual)
- Power analysis
- Comparison bar chart + Va vs R3 sensitivity graph

## 🧪 Sample Output
Input : V1=12V, V2=6V, R1=100Ω, R2=200Ω, R3=300Ω
STEP 1 — V1 ACTING ALONE (V2 Shorted)
Node Voltage Va'  =  4.3636 V
I1' (thru R1)     =  0.0764 A
STEP 2 — V2 ACTING ALONE (V1 Shorted)
Node Voltage Va'' =  1.0909 V
I2'' (thru R2)    =  0.0245 A
STEP 3 — SUPERPOSITION RESULT
Va = 5.4545 V
STEP 4 — ACTUAL CIRCUIT
Va = 5.4545 V
✅ THEOREM VERIFIED: Superposition holds!

## 📁 Repository Structure
BEE_CEP_2026_GROUP01/
├── src/
│   └── superposition_verifier.py
├── report/
│   └── BEE_CEP_Report_Group01.pdf
├── screenshots/
│   └── superposition_output.png
├── README.md
└── requirements.txt

## 📚 References
1. V.K. Mehta, *Principles of Basic Electrical Engineering*, S. Chand, 2020.
2. D.P. Kothari & I.J. Nagrath, *Basic Electrical Engineering*, Tata McGraw-Hill, 2019.
