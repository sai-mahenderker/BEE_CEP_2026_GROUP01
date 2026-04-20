# ============================================================
# BEE Course End Project - Group 01
# Title  : Superposition Theorem Verifier for Multi-Source DC Circuits
# Course : A9205 - Basic Electrical Engineering Laboratory
# Class  : I B.Tech. II Semester CSE-F
# ============================================================

import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# CIRCUIT TOPOLOGY (Fixed for this project)
#
#   V1 ---R1---+---R2--- V2
#              |
#              R3
#              |
#             GND
#
# Node A is the junction of R1, R2, R3.
# We find: Voltage at node A (Va) and currents I1, I2, I3
# using Superposition.
# ------------------------------------------------------------

def get_positive_float(prompt):
    """Input validation: accepts only positive numbers."""
    while True:
        try:
            val = float(input(prompt))
            if val <= 0:
                print("  [!] Value must be positive. Try again.")
            else:
                return val
        except ValueError:
            print("  [!] Invalid input. Enter a numeric value.")

def get_float(prompt):
    """Input validation: accepts any real number (voltages can be negative)."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  [!] Invalid input. Enter a numeric value.")

def solve_with_source1_only(V1, R1, R2, R3):
    """
    Deactivate V2 (short circuit: replace V2 with wire).
    Circuit: V1 -> R1 -> Node A -> (R2 || R3) -> GND
    R2 and R3 are in parallel (both connected to GND after V2 shorted).
    """
    R_parallel = (R2 * R3) / (R2 + R3)          # R2 || R3
    I1_a = V1 / (R1 + R_parallel)                # Current from V1
    Va_a = I1_a * R_parallel                      # Voltage at Node A
    I3_a = Va_a / R3                              # Current through R3
    I2_a = Va_a / R2                              # Current through R2 (toward short)
    return Va_a, I1_a, I2_a, I3_a

def solve_with_source2_only(V2, R1, R2, R3):
    """
    Deactivate V1 (short circuit: replace V1 with wire).
    Circuit: V2 -> R2 -> Node A -> (R1 || R3) -> GND
    R1 and R3 are in parallel (both connected to GND after V1 shorted).
    """
    R_parallel = (R1 * R3) / (R1 + R3)          # R1 || R3
    I2_b = V2 / (R2 + R_parallel)                # Current from V2
    Va_b = I2_b * R_parallel                      # Voltage at Node A
    I3_b = Va_b / R3                              # Current through R3
    I1_b = Va_b / R1                              # Current through R1 (toward short)
    return Va_b, I1_b, I2_b, I3_b

def solve_actual_circuit(V1, V2, R1, R2, R3):
    """
    Solve the actual circuit using Node Voltage Method.
    KCL at Node A:
        (Va - V1)/R1 + (Va - V2)/R2 + Va/R3 = 0
    Solving for Va:
        Va*(1/R1 + 1/R2 + 1/R3) = V1/R1 + V2/R2
    """
    G1, G2, G3 = 1/R1, 1/R2, 1/R3              # Conductances
    Va = (V1*G1 + V2*G2) / (G1 + G2 + G3)       # Node voltage
    I1 = (V1 - Va) / R1                           # Current through R1
    I2 = (V2 - Va) / R2                           # Current through R2
    I3 = Va / R3                                   # Current through R3
    return Va, I1, I2, I3

def print_section(title):
    print("\n" + "="*55)
    print(f"  {title}")
    print("="*55)

def plot_results(V1, V2, labels, actual_vals, super_vals, component_labels):
    """Bar chart comparing Actual vs Superposition results."""
    x = np.arange(len(labels))
    width = 0.35

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(
        f"Superposition Theorem Verifier\nV1={V1}V, V2={V2}V",
        fontsize=13, fontweight='bold'
    )

    # --- Plot 1: Voltage & Currents comparison ---
    ax1 = axes[0]
    bars1 = ax1.bar(x - width/2, actual_vals, width, label='Actual (Node Analysis)', color='steelblue')
    bars2 = ax1.bar(x + width/2, super_vals,  width, label='Superposition Result',   color='darkorange')
    ax1.set_xlabel('Circuit Quantity', fontsize=11)
    ax1.set_ylabel('Value (V or A)', fontsize=11)
    ax1.set_title('Actual vs Superposition Values', fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.6)
    for bar in bars1:
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.02,
                 f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.02,
                 f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=8)

    # --- Plot 2: R varying vs Node Voltage (sensitivity) ---
    ax2 = axes[1]
    R3_range = np.linspace(10, 500, 200)
    Va_range = []
    for r3 in R3_range:
        G1, G2, G3 = 1/R1_global, 1/R2_global, 1/r3
        va = (V1*G1 + V2*G2) / (G1 + G2 + G3)
        Va_range.append(va)
    ax2.plot(R3_range, Va_range, color='green', linewidth=2)
    ax2.set_xlabel('R3 (Ω)', fontsize=11)
    ax2.set_ylabel('Node Voltage Va (V)', fontsize=11)
    ax2.set_title('Node Voltage Va vs R3 (R1, R2 fixed)', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig('screenshots/superposition_output.png', dpi=150)
    print("\n  [✓] Graph saved to screenshots/superposition_output.png")
    plt.show()

# ============================================================
# MAIN PROGRAM
# ============================================================

# Global variables for plotting (set after input)
R1_global = R2_global = 1.0

def main():
    global R1_global, R2_global

    print("\n" + "#"*55)
    print("  SUPERPOSITION THEOREM VERIFIER")
    print("  Multi-Source DC Circuit Analyzer")
    print("  BEE Lab CEP | VCE | Group 01")
    print("#"*55)

    print("""
  Circuit Topology:
  
    V1(+) --[R1]--+--[R2]--(+)V2
                  |
                 [R3]
                  |
                 GND
                 
  Node A = junction of R1, R2, R3
  Finding: Va, I1 (thru R1), I2 (thru R2), I3 (thru R3)
    """)

    # --- User Inputs ---
    print_section("ENTER CIRCUIT PARAMETERS")
    V1 = get_float("  Enter V1 (Voltage Source 1 in Volts) : ")
    V2 = get_float("  Enter V2 (Voltage Source 2 in Volts) : ")
    R1 = get_positive_float("  Enter R1 (Resistance 1 in Ohms)      : ")
    R2 = get_positive_float("  Enter R2 (Resistance 2 in Ohms)      : ")
    R3 = get_positive_float("  Enter R3 (Resistance 3 in Ohms)      : ")

    R1_global = R1
    R2_global = R2

    # --- Step 1: V1 acting alone ---
    print_section("STEP 1 — V1 ACTING ALONE (V2 Shorted)")
    Va_a, I1_a, I2_a, I3_a = solve_with_source1_only(V1, R1, R2, R3)
    print(f"  Node Voltage Va' = {Va_a:.4f} V")
    print(f"  I1' (thru R1)    = {I1_a:.4f} A")
    print(f"  I2' (thru R2)    = {I2_a:.4f} A")
    print(f"  I3' (thru R3)    = {I3_a:.4f} A")

    # --- Step 2: V2 acting alone ---
    print_section("STEP 2 — V2 ACTING ALONE (V1 Shorted)")
    Va_b, I1_b, I2_b, I3_b = solve_with_source2_only(V2, R1, R2, R3)
    print(f"  Node Voltage Va'' = {Va_b:.4f} V")
    print(f"  I1'' (thru R1)    = {I1_b:.4f} A")
    print(f"  I2'' (thru R2)    = {I2_b:.4f} A")
    print(f"  I3'' (thru R3)    = {I3_b:.4f} A")

    # --- Step 3: Superposition Sum ---
    print_section("STEP 3 — SUPERPOSITION (Sum of Steps 1 & 2)")
    Va_sup = Va_a + Va_b
    I1_sup = I1_a + I1_b
    I2_sup = I2_a + I2_b
    I3_sup = I3_a + I3_b
    print(f"  Va (superposed)  = {Va_a:.4f} + {Va_b:.4f} = {Va_sup:.4f} V")
    print(f"  I1 (superposed)  = {I1_a:.4f} + {I1_b:.4f} = {I1_sup:.4f} A")
    print(f"  I2 (superposed)  = {I2_a:.4f} + {I2_b:.4f} = {I2_sup:.4f} A")
    print(f"  I3 (superposed)  = {I3_a:.4f} + {I3_b:.4f} = {I3_sup:.4f} A")

    # --- Step 4: Actual Circuit (Node Voltage Method) ---
    print_section("STEP 4 — ACTUAL CIRCUIT (Node Voltage Method)")
    Va_act, I1_act, I2_act, I3_act = solve_actual_circuit(V1, V2, R1, R2, R3)
    print(f"  Va (actual)  = {Va_act:.4f} V")
    print(f"  I1 (actual)  = {I1_act:.4f} A")
    print(f"  I2 (actual)  = {I2_act:.4f} A")
    print(f"  I3 (actual)  = {I3_act:.4f} A")

    # --- Step 5: Verification ---
    print_section("STEP 5 — VERIFICATION (Superposition vs Actual)")
    tolerance = 1e-6
    results = {
        "Va" : (Va_sup,  Va_act),
        "I1" : (I1_sup,  I1_act),
        "I2" : (I2_sup,  I2_act),
        "I3" : (I3_sup,  I3_act),
    }
    all_pass = True
    print(f"  {'Qty':<6} {'Superposition':>15} {'Actual':>12} {'Error%':>10} {'Status':>8}")
    print("  " + "-"*55)
    for qty, (sup, act) in results.items():
        err = abs(sup - act)
        err_pct = (err / abs(act) * 100) if abs(act) > 1e-9 else 0.0
        status = "✓ PASS" if err < tolerance else "✗ FAIL"
        if err >= tolerance:
            all_pass = False
        unit = "V" if qty == "Va" else "A"
        print(f"  {qty:<6} {sup:>14.6f}{unit} {act:>11.6f}{unit} {err_pct:>9.4f}% {status:>8}")

    print("\n" + "="*55)
    if all_pass:
        print("  ✅ THEOREM VERIFIED: Superposition holds!")
    else:
        print("  ❌ Mismatch detected — check circuit inputs.")
    print("="*55)

    # --- Power Check ---
    print_section("BONUS — POWER ANALYSIS (Actual Circuit)")
    P_R1 = I1_act**2 * R1
    P_R2 = I2_act**2 * R2
    P_R3 = I3_act**2 * R3
    P_V1 = V1 * I1_act
    P_V2 = V2 * I2_act
    print(f"  Power in R1     = {P_R1:.4f} W")
    print(f"  Power in R2     = {P_R2:.4f} W")
    print(f"  Power in R3     = {P_R3:.4f} W")
    print(f"  Power by V1     = {P_V1:.4f} W")
    print(f"  Power by V2     = {P_V2:.4f} W")
    print(f"  Total dissipated= {P_R1+P_R2+P_R3:.4f} W")
    print(f"  Total supplied  = {P_V1+P_V2:.4f} W")

    # --- Plot ---
    import os
    os.makedirs("screenshots", exist_ok=True)
    labels     = ['Va (V)', 'I1 (A)', 'I2 (A)', 'I3 (A)']
    actual_v   = [Va_act, I1_act, I2_act, I3_act]
    super_v    = [Va_sup, I1_sup, I2_sup, I3_sup]
    plot_results(V1, V2, labels, actual_v, super_v, labels)

if __name__ == "__main__":
    main()
