"""
Beam Analysis Tool v2
Developer: Monjyeeman Dutta

A computational mechanics tool for analyzing simply supported beams.

Capabilities:
- Reaction Force Calculation
- Shear Force Diagram (SFD)
- Bending Moment Diagram (BMD)
- Deflection Curve
- Serviceability Check (L/250)
- Supports Point Load & UDL

Built using Python + NumPy + Matplotlib
"""



import numpy as np
import matplotlib.pyplot as plt

#SAFEGUARDS
def choice_input(prompt, valid_choices):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_choices:
                return value
            print("Invalid choice. Try again.")
        except ValueError:
            print("Enter a valid number.")

def positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Value must be greater than zero.")
        except ValueError:
            print("Enter a valid number.")
            
np.set_printoptions(suppress=True)


#HELPER FUNCTIONS
def axis_length(x, unit):
    if unit == 1:
        return x, "m"
    elif unit == 2:
        return x * 1000, "mm"
    elif unit == 3:
        return x * 100, "cm"


#UNIT CONVERSION FUNCTIONS
def convert_length(value, unit):
        if unit == 1:      #m
            return value
        elif unit == 2:    #mm
            return value / 1000
        elif unit == 3:    #cm
            return value / 100

def convert_E(value, unit):
        if unit == 1:      #GPa
            return value * 1e9
        elif unit == 2:    #MPa
            return value * 1e6

def convert_I(value, unit):
        if unit == 1:      #mm^4
            return value * 1e-12
        elif unit == 2:    #m^4
            return value

def convert_load(value, unit):
            if unit == 1:      #N
                return value
            elif unit == 2:    #kN
                return value * 1000

def convert_udl(value, unit):
            if unit == 1:      #N/m
                return value
            elif unit == 2:    #kN/m
                return value * 1000


#PHYSICS FUNCTIONS
def point_load_ssb(P, L, E, I, a):
    b = L - a
    delta = (P * a * b * (L**2 - a**2 - b**2)) / (6 * E * I * L)

    return float(delta)


def udl_ssb(w,L,E,I):
    delta = (5*w*(L**4))/(384*E*I)
    return float(delta)


#PLOTTING FUNCTIONS
def plot_point_load_ssb(P, L, E, I, a, Lunits):

    x = np.linspace(0, L, 400)
    b = L-a
    
    y = np.zeros_like(x)

    mask1 = x < a
    y[mask1] = (P*b*x[mask1]/(6*L*E*I))*(L**2-b**2-x[mask1]**2)

    mask2 = x >= a
    y[mask2] = (P*a*(L - x[mask2])/(6*L*E*I))*(L**2-a**2-(L-x[mask2])**2)

    y_plot = y * 1000

    if Lunits == 1:
        x_plot = x
        length_label = "m"
    elif Lunits == 2:
        x_plot = x * 1000
        length_label = "mm"
    elif Lunits == 3:
        x_plot = x * 100
        length_label = "cm"

    plt.figure(figsize=(11,5), dpi=120)
    plt.plot(x_plot, y_plot, linewidth=3)

    plt.axhline(0)

    load_x = a
    if Lunits == 2:
        load_x *= 1000
    elif Lunits == 3:
        load_x *= 100

    plt.scatter(load_x, min(y_plot), zorder=5)
    plt.fill_between(x_plot, y_plot, 0, alpha=0.2)

    plt.title("Deflection Curve — Simply Supported Beam (Point Load)")
    plt.xlabel(f"Beam Length ({length_label})")
    plt.ylabel("Deflection (mm)")

    plt.gca().invert_yaxis()
    plt.ticklabel_format(style='plain', axis='y')
    plt.grid(True)
    plt.show()

def plot_udl_ssb(w, L, E, I, Lunits):

    x = np.linspace(0, L, 400)
    y = (w * x * (L**3 - 2*L*(x**2) + x**3)) / (24 * E * I)

    y_plot = y * 1000

    if Lunits == 1:
        x_plot = x
        length_label = "m"
    elif Lunits == 2:
        x_plot = x * 1000
        length_label = "mm"
    elif Lunits == 3:
        x_plot = x * 100
        length_label = "cm"

    plt.figure(figsize=(11,5), dpi=120)
    plt.plot(x_plot, y_plot, linewidth=3)

    plt.axhline(0)
    plt.fill_between(x_plot, y_plot, 0, alpha=0.2)

    plt.title("Deflection Curve — Simply Supported Beam (UDL)")
    plt.xlabel(f"Beam Length ({length_label})")
    plt.ylabel("Deflection (mm)")

    plt.gca().invert_yaxis()
    plt.ticklabel_format(style='plain', axis='y')
    plt.grid(True)
    plt.show()

#REACTION FORCES
def reactions_point_load(P, L, a):
    b = L - a
    R1 = P * b / L
    R2 = P * a / L
    
    print("\n---Reaction Forces---")
    print(f"Left Reaction  = {R1:.3f} N")
    print(f"Right Reaction = {R2:.3f} N")
    
    return R1, R2

def reactions_udl(w, L):
    R = w * L / 2
    
    print("\n---Reaction Forces---")
    print(f"Left Reaction  = {R:.3f} N")
    print(f"Right Reaction = {R:.3f} N")
    
    return R, R


#SFD & BMD
def plot_sfd_point(R1, P, a, L, Lunits):
    x = np.linspace(0, L, 400)
    x_plot, length_label = axis_length(x, Lunits)
    V = np.where(x < a, R1, R1 - P)

    plt.figure(figsize=(10,5),dpi=120)
    plt.plot(x_plot, V, linewidth=3)
    plt.fill_between(x_plot, V, 0, alpha=0.25)
    
    plt.axhline(0)
    plt.title("Shear Force Diagram — Point Load")
    plt.xlabel(f"Beam Length ({length_label})")
    plt.ylabel("Shear Force (N)")
    plt.grid(True)
    plt.show()

def plot_bmd_point(R1, P, a, L, Lunits):
    x = np.linspace(0, L, 400)
    x_plot, length_label = axis_length(x, Lunits)
    M = np.where(x < a, R1*x, R1*x - P*(x-a))

    plt.figure(figsize=(10,5), dpi=120)
    plt.plot(x_plot, M, linewidth=3)
    plt.fill_between(x_plot, M, 0, alpha=0.25)

    plt.axhline(0)
    plt.title("Bending Moment Diagram — Point Load")
    plt.xlabel(f"Beam Length ({length_label})")
    plt.ylabel("Moment (Nm)")
    plt.grid(True)
    plt.show()

def plot_sfd_udl(w, L, Lunits):
    x = np.linspace(0, L, 400)
    x_plot, length_label = axis_length(x, Lunits)
    R = w * L / 2
    V = R - w * x

    plt.figure(figsize=(10,5), dpi=120)
    plt.plot(x_plot, V, linewidth=3)
    plt.fill_between(x_plot, V, 0, alpha=0.25)

    plt.axhline(0)
    plt.title("Shear Force Diagram — UDL")
    plt.xlabel(f"Beam Length ({length_label})")
    plt.ylabel("Shear Force (N)")
    plt.grid(True)
    plt.show()

def plot_bmd_udl(w, L, Lunits):
    x = np.linspace(0, L, 400)
    x_plot, length_label = axis_length(x, Lunits)
    R = w * L / 2
    M = R*x - (w*x**2)/2

    plt.figure(figsize=(10,5), dpi=120)
    plt.plot(x_plot, M, linewidth=3)
    plt.fill_between(x_plot, M, 0, alpha=0.25)

    plt.axhline(0)
    plt.title("Bending Moment Diagram — UDL")
    plt.xlabel(f"Beam Length ({length_label})")
    plt.ylabel("Moment (Nm)")
    plt.grid(True)
    plt.show()


#CONSTANTS
NEGLIGIBLE_DEFLECTION = 0.001

#MAIN
def main():
    print("Beam Analysis Tool")
    print("\nNOTE : All calculations are performed in SI units.")
    
    print("\n---Beam Properties---")
    L = positive_float("Enter the length of the beam = ")
    Lunits = choice_input("Select your units [1.Metre(m), 2.Millimeters(mm), 3.Centimeter(cm)] = ", [1,2,3])
    L = convert_length(L, Lunits)
    
    E = positive_float("Enter the Young's Modulus of Elasticity = ")
    Eunits = choice_input("Select your units [1.Giga Pascal(GPa), 2.Mega Pascal(MPa)] = ", [1,2])
    E = convert_E(E, Eunits)
    
    I = positive_float("Enter the Moment of Inertia = ")
    Iunits = choice_input("Select your units [1.Millimeters(mm^4), 2.Meters(m^4)] = ", [1,2])
    I = convert_I(I, Iunits)
    if I < 1e-10: 
        print("WARNING : Moment of Inertia is extremely small check units.")

    print("\n---Loading Properties---")
    option = choice_input(
        "\n1.Point Load acting on a Simply Supported Beam\n"
        "2.Uniformly Distributed Load on a Simply Supported Beam\n"
        "Select the type of Load = ",
        [1,2]
    )
    
    LIMIT = L * 1000 / 250  
    
    if option == 1:
        P = float(input("Enter your Load Magnitude (Use -ve values for upward loading) = "))
        Punits = choice_input("Select your units [1.Newtons(N), 2.Kilo Newtons(kN)] = ", [1,2])
        P = convert_load(P, Punits)
        
        a = float(input("Enter your Load Position from Left Hand Supported = "))
        aunits = choice_input("Select your units [1.Metre(m), 2.Millimeters(mm), 3.Centimeter(cm)] = ", [1,2,3])
        a = convert_length(a, aunits)

        if not (0 < a < L):
            print("Invalid Load Position. Load must lie between 0 and Beam Length.")
            return
        
        deflection = point_load_ssb(P,L,E,I,a)
        actual_deflection = deflection * 1000

        R1, R2 = reactions_point_load(P, L, a)

        if actual_deflection < NEGLIGIBLE_DEFLECTION:
            print("\nMaximum Deflection is negligible under the given loading conditions.")
        elif actual_deflection > LIMIT:
            print("\nWARNING : Deflection exceeds typical serviceability limits (L/250).\nBeam may not be suitable for structural use.")

        print("\n----RESULT---\n")
        print(f"Maximum Deflection :\n {deflection:.6f} m\n {actual_deflection:.3f} mm")

        plot_sfd_point(R1, P, a, L, Lunits)
        plot_bmd_point(R1, P, a, L, Lunits)
        plot_point_load_ssb(P, L, E, I, a, Lunits)
            
    elif option == 2:
        w = positive_float("Enter the Load Intensity = ")
        wunits = choice_input("Select your units [1.Newton per Metre(N/m), 2.Kilo Newton per Metre(kN/m)] = ", [1,2])
        w = convert_udl(w, wunits)
        
        deflection = udl_ssb(w,L,E,I)
        actual_deflection = deflection * 1000

        R1, R2 = reactions_udl(w, L)

        if actual_deflection < NEGLIGIBLE_DEFLECTION:
            print("\nMaximum Deflection is negligible under the given loading conditions.")
        elif actual_deflection > LIMIT:
            print("\nWARNING : Deflection exceeds typical serviceability limits (L/250).\nBeam may not be suitable for structural use.")
            print("\n----RESULT---\n")
            print(f"Maximum Deflection :\n {deflection:.6f} m\n {actual_deflection:.3f} mm")
                
        print("\n----RESULT---\n")
        print(f"Maximum Deflection :\n {deflection:.6f} m\n {actual_deflection:.3f} mm")

        plot_sfd_udl(w, L, Lunits)
        plot_bmd_udl(w, L, Lunits)
        plot_udl_ssb(w,L,E,I,Lunits)
        
    else:
        print("Invalid Selection. Please Restart the Programme.")
    print("\nAnalysis Complete.")   
    
if __name__ == "__main__":
    main()