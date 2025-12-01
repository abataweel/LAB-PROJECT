import sys                                  # Gives access to system-level functions (like command-line args, exit)
import cmath                               # Provides complex math functions (used for AC impedance and angles)
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox  # Main Qt classes for GUI app and message boxes
from PyQt5.uic import loadUi               # Allows loading a .ui file created with Qt Designer


class MainApp(QMainWindow):                # Main window class, inherits from QMainWindow
    def __init__(self):
        super().__init__()                 # Initialize the parent QMainWindow properly
        loadUi("Lab_project.ui", self)  # Load the Qt Designer UI file and attach widgets to 'self'

        # Start on the first page (Series/Parallel selector page_2)
        self.stackedWidget.setCurrentWidget(self.page_2)

        # When the user changes the comboBox on page_2 (Series / Parallel), call switch_page()
        self.comboBox1_2.currentIndexChanged.connect(self.switch_page)

        # Listen to AC / DC combo boxes on both pages
        self.comboBox1_3.currentIndexChanged.connect(self.apply_acdc_mode)  # Parallel page AC/DC selector
        self.comboBox1_8.currentIndexChanged.connect(self.apply_acdc_mode)  # Series page AC/DC selector

        # Connect simulate buttons to their functions
        self.pushButton.clicked.connect(self.simulate_parallel)   # Simulate button on parallel page
        self.pushButton_3.clicked.connect(self.simulate_series)   # Simulate button on series page

        # Back buttons you added (parallel and series pages)
        if hasattr(self, "pushButton_2"):                        # Check if pushButton_2 exists (parallel page back)
            self.pushButton_2.clicked.connect(self.go_back_to_main)  # If it exists, connect to go_back_to_main()

        if hasattr(self, "pushButton_4"):                        # Check if pushButton_4 exists (series page back)
            self.pushButton_4.clicked.connect(self.go_back_to_main)  # Connect to go_back_to_main()

        # Disable all input widgets until AC or DC mode is chosen
        self.lock_all_inputs()

    # ---------------------------------------------------------
    # Go back to first page (Series/Parallel selection page)
    # ---------------------------------------------------------
    def go_back_to_main(self):
        self.stackedWidget.setCurrentWidget(self.page_2)          # Switch stackedWidget back to page_2

    # ---------------------------------------------------------
    # Lock everything before AC/DC is selected
    # ---------------------------------------------------------
    def lock_all_inputs(self):
        # List of widgets that must be disabled until AC/DC mode is chosen
        widgets = [
            # Parallel page input widgets
            self.lineEdit, self.lineEdit_2, self.lineEdit_3,      # Impedance/Resistor 1, 2 and Voltage (parallel)
            self.comboBox, self.comboBox_2,                       # Component type combos (Resistor/Inductor/Capacitor)
            self.comboBox1, self.comboBox2,                       # Tolerance combo boxes (parallel)
            self.lineEdit_freq,                                   # Frequency input (parallel)

            # Series page input widgets
            self.lineEdit_9, self.lineEdit_8, self.lineEdit_7,    # Impedance/Resistor 1, 2 and Voltage (series)
            self.comboBox_5, self.comboBox_6,                     # Component type combos (series)
            self.comboBox1_7, self.comboBox2_3,                   # Tolerance combo boxes (series)
            self.lineEdit_freq_3,                                 # Frequency input (series)
        ]
        for w in widgets:
            w.setEnabled(False)                                   # Disable each widget in the list

    # ---------------------------------------------------------
    # Switch between series / parallel calculator pages
    # ---------------------------------------------------------
    def switch_page(self):
        choice = self.comboBox1_2.currentText()                   # Get current text from Series/Parallel combo box

        if choice == "Series":                                    # If user chose "Series"
            self.stackedWidget.setCurrentWidget(self.page_3)      # Show series page (page_3)

        elif choice == "Parallel":                                # If user chose "Parallel"
            self.stackedWidget.setCurrentWidget(self.page)        # Show parallel page (page)

    # ---------------------------------------------------------
    # Decide global AC / DC mode based on the dropdowns
    # ---------------------------------------------------------
    def apply_acdc_mode(self):
        # Create a set of both AC/DC combo box values (from parallel and series pages)
        modes = {self.comboBox1_3.currentText(), self.comboBox1_8.currentText()}

        if "AC" in modes:                                         # If any of them says "AC"
            mode = "AC"                                           # Global mode is AC
        elif "DC" in modes:                                       # If any of them says "DC"
            mode = "DC"                                           # Global mode is DC
        else:
            mode = None                                           # No valid selection (still "AC/DC")

        if mode is None:                                          # If no AC or DC chosen yet
            self.lock_all_inputs()                                # Lock all inputs so user can't type
            self.label_4.setText("")                              # Clear output label (parallel result)
            self.label_18.setText("")                             # Clear output label (series result)
            return                                                # Exit function

        if mode == "DC":                                          # If global mode is DC
            self.enable_dc_mode()                                 # Configure everything for DC mode
        else:                                                     # Otherwise it's AC
            self.enable_ac_mode()                                 # Configure everything for AC mode

    # ---------------------------------------------------------
    # DC MODE → resistors only, no frequency
    # ---------------------------------------------------------
    def enable_dc_mode(self):
        # -------- Parallel page --------
        for w in [self.lineEdit, self.lineEdit_2, self.lineEdit_3]:
            w.setEnabled(True)                                    # Enable R1, R2 and Voltage inputs (parallel)

        # Component selection combos forced to "Resistor" and disabled
        self.comboBox.setCurrentIndex(0)                          # Force first combo to "Resistor"
        self.comboBox_2.setCurrentIndex(0)                        # Force second combo to "Resistor"
        self.comboBox.setEnabled(False)                           # Disable combo so user can't change type
        self.comboBox_2.setEnabled(False)                         # Disable combo so user can't change type

        # Frequency disabled in DC mode (parallel)
        self.lineEdit_freq.setText("")                            # Clear frequency value
        self.lineEdit_freq.setEnabled(False)                      # Disable frequency input

        # Tolerance comboboxes ON (parallel)
        self.comboBox1.setEnabled(True)                           # Enable tolerance for element 1
        self.comboBox2.setEnabled(True)                           # Enable tolerance for element 2

        # Labels show "Resistor 1" and "Resistor 2" in DC
        self.label.setText("Resistor 1")                          # Label for first element (parallel)
        self.label_2.setText("Resistor 2")                        # Label for second element (parallel)
        # Tolerance labels set to "Resistor X Tolerance"
        self.label_5.setText("Resistor 1 Tolerance")              # Label describing tolerance 1
        self.label_6.setText("Resistor 2 Tolerance")              # Label describing tolerance 2

        # -------- Series page --------
        for w in [self.lineEdit_9, self.lineEdit_8, self.lineEdit_7]:
            w.setEnabled(True)                                    # Enable R1, R2 and Voltage inputs (series)

        self.comboBox_5.setCurrentIndex(0)                        # Force first combo (series) to "Resistor"
        self.comboBox_6.setCurrentIndex(0)                        # Force second combo (series) to "Resistor"
        self.comboBox_5.setEnabled(False)                         # Disable type combo (series)
        self.comboBox_6.setEnabled(False)                         # Disable type combo (series)

        self.lineEdit_freq_3.setText("")                          # Clear frequency input (series)
        self.lineEdit_freq_3.setEnabled(False)                    # Disable frequency (series)

        self.comboBox1_7.setEnabled(True)                         # Enable tolerance for first element (series)
        self.comboBox2_3.setEnabled(True)                         # Enable tolerance for second element (series)

        self.label_20.setText("Resistor 1")                       # Label for first resistor (series)
        self.label_15.setText("Resistor 2")                       # Label for second resistor (series)
        self.label_16.setText("Resistor 1 Tolerance")             # Tolerance label for first resistor (series)
        self.label_21.setText("Resistor 2 Tolerance")             # Tolerance label for second resistor (series)

    # ---------------------------------------------------------
    # AC MODE → full impedance options + frequency
    # ---------------------------------------------------------
    def enable_ac_mode(self):
        # -------- Parallel page --------
        for w in [
            self.lineEdit, self.lineEdit_2, self.lineEdit_3,      # R1, R2, Voltage (parallel)
            self.comboBox, self.comboBox_2,                       # Element type (Resistor/Inductor/Capacitor)
            self.comboBox1, self.comboBox2,                       # Tolerance combos (parallel)
            self.lineEdit_freq,                                   # Frequency input (parallel)
        ]:
            w.setEnabled(True)                                    # Enable all these widgets

        # In AC mode, elements are treated as "Impedance"
        self.label.setText("Impedance 1")                         # Label for first impedance (parallel)
        self.label_2.setText("Impedance 2")                       # Label for second impedance (parallel)
        self.label_5.setText("Impedance 1 Tolerance")             # Tolerance label for first impedance (parallel)
        self.label_6.setText("Impedance 2 Tolerance")             # Tolerance label for second impedance (parallel)

        # -------- Series page --------
        for w in [
            self.lineEdit_9, self.lineEdit_8, self.lineEdit_7,    # R1, R2, Voltage (series)
            self.comboBox_5, self.comboBox_6,                     # Type combos (series)
            self.comboBox1_7, self.comboBox2_3,                   # Tolerance combos (series)
            self.lineEdit_freq_3,                                 # Frequency input (series)
        ]:
            w.setEnabled(True)                                    # Enable all these widgets (series)

        self.label_20.setText("Impedance 1")                      # Label for first impedance (series)
        self.label_15.setText("Impedance 2")                      # Label for second impedance (series)
        self.label_16.setText("Impedance 1 Tolerance")            # Tolerance label for first impedance (series)
        self.label_21.setText("Impedance 2 Tolerance")            # Tolerance label for second impedance (series)

    # ---------------------------------------------------------
    # Simple numeric validation helper for QLineEdit
    # ---------------------------------------------------------
    def get_float(self, box, name):
        text = box.text().strip()                                 # Read and strip text from QLineEdit

        if text == "":                                            # If text is empty
            QMessageBox.warning(self, "Missing Input",
                                f"Please enter a value for {name}.")  # Warn user that value is required
            return None

        try:
            return float(text)                                    # Try converting to float
        except ValueError:                                        # If conversion fails
            QMessageBox.warning(self, "Invalid Number",
                                f"'{text}' is not a valid number for {name}.")  # Show error
            return None

    # ---------------------------------------------------------
    # Complex impedance calculation helper for AC mode
    # ---------------------------------------------------------
    def calc_impedance(self, type_name, value, freq):
        if value <= 0:                                            # Impedance component should be > 0
            QMessageBox.warning(self, "Invalid Input",
                                "Impedance value must be greater than 0.")
            return None

        w = 2 * 3.14159 * freq                                    # Angular frequency ω = 2πf

        if type_name.startswith("Resistor"):                      # If the selected type is Resistor
            return complex(value, 0)                              # Pure real impedance R + j0

        elif type_name.startswith("Inductor"):                    # If selected type is Inductor
            return complex(0, w * value)                          # Inductive reactance: jωL

        elif type_name.startswith("Capacitor"):                   # If selected type is Capacitor
            if value == 0:
                QMessageBox.warning(self, "Math Error",
                                    "Capacitance cannot be zero.")
                return None
            return complex(0, -1 / (w * value))                   # Capacitive reactance: -j / (ωC)

        return None                                               # Fallback (unknown type)

    # ---------------------------------------------------------
    # Parallel simulation (both DC and AC)
    # ---------------------------------------------------------
    def simulate_parallel(self):
        mode = self.comboBox1_3.currentText()                     # Read AC/DC mode from parallel page combo

        if mode == "AC/DC":                                       # If still on default option
            QMessageBox.warning(self, "Mode Error",
                                "Choose AC or DC first.")         # Force user to choose AC or DC
            return

        v = self.get_float(self.lineEdit_3, "Voltage")            # Get voltage value from input
        r1 = self.get_float(self.lineEdit, "Impedance 1")         # Get first impedance/resistor value
        r2 = self.get_float(self.lineEdit_2, "Impedance 2")       # Get second impedance/resistor value
        if None in [v, r1, r2]:                                   # If any input is invalid
            return                                                # Stop simulation

        tol1 = self.comboBox1.currentText()                       # Read tolerance text for element 1
        tol2 = self.comboBox2.currentText()                       # Read tolerance text for element 2
        if tol1 == "Select Tolerance" or tol2 == "Select Tolerance":
            QMessageBox.warning(self, "Tolerance Error",
                                "Please select tolerance for both elements.")  # Tolerances must be chosen
            return

        # ---------- DC ----------
        if mode == "DC":                                          # If mode is DC
            try:
                total = 1 / (1 / r1 + 1 / r2)                     # Parallel resistance formula: 1/Rt = 1/R1 + 1/R2
            except ZeroDivisionError:                             # Handle division by zero if r1 or r2 is zero
                QMessageBox.warning(self, "Error",
                                    "Invalid resistor values.")
                return

            current = v / total                                   # I = V / Rt

            self.label_4.setText(                                 # Build and display result string (DC parallel)
                f"--- Circuit Simulation (DC Parallel) ---\n"
                f"Source: {v} V\n"
                f"R₁: {r1} Ω {tol1}\n"
                f"R₂: {r2} Ω {tol2}\n"
                f"Total Resistance: {total:.3f} Ω\n"
                f"Total Current: {current:.3f} A"
            )
            return                                                # Stop here for DC

        # ---------- AC ----------
        freq = self.get_float(self.lineEdit_freq, "Frequency")    # Get frequency in Hz for AC
        if freq is None or freq <= 0:                             # Validate frequency
            QMessageBox.warning(self, "Invalid Frequency",
                                "Frequency must be greater than 0.")
            return

        z1 = self.calc_impedance(self.comboBox.currentText(), r1, freq)   # Calculate impedance Z1 based on type
        z2 = self.calc_impedance(self.comboBox_2.currentText(), r2, freq) # Calculate impedance Z2 based on type
        if None in [z1, z2]:                                      # If impedance calculation failed
            return                                                # Stop simulation

        total = 1 / (1 / z1 + 1 / z2)                             # Parallel total impedance: 1/Zt = 1/Z1 + 1/Z2
        current = v / total                                       # Total current I = V / Zt
        ang_total = cmath.phase(total) * 180 / 3.14159            # Angle of total impedance in degrees

        self.label_4.setText(                                     # Display AC parallel result with magnitude and angle
            f"--- Circuit Simulation (AC Parallel) ---\n"
            f"Source: {v:.1f} V\n"
            f"Z₁: {abs(z1):.3f} Ω ∠ {cmath.phase(z1) * 180 / 3.14159:.2f}° {tol1}\n"
            f"Z₂: {abs(z2):.3f} Ω ∠ {cmath.phase(z2) * 180 / 3.14159:.2f}° {tol2}\n"
            f"Total Impedance: {abs(total):.3f} Ω ∠ {ang_total:.2f}°\n"
            f"Total Current: {abs(current):.3f} A"
        )

    # ---------------------------------------------------------
    # Series simulation (both DC and AC)
    # ---------------------------------------------------------
    def simulate_series(self):
        mode = self.comboBox1_8.currentText()                     # Read AC/DC mode from series page combo

        if mode == "AC/DC":                                       # If user hasn't chosen mode
            QMessageBox.warning(self, "Mode Error",
                                "Choose AC or DC first.")
            return

        v = self.get_float(self.lineEdit_7, "Voltage")            # Get voltage (series page)
        r1 = self.get_float(self.lineEdit_9, "Impedance 1")       # Get first impedance/resistor value (series)
        r2 = self.get_float(self.lineEdit_8, "Impedance 2")       # Get second impedance/resistor value (series)
        if None in [v, r1, r2]:                                   # If any invalid
            return

        tol1 = self.comboBox1_7.currentText()                     # Tolerance for element 1 (series)
        tol2 = self.comboBox2_3.currentText()                     # Tolerance for element 2 (series)
        if tol1 == "Select Tolerance" or tol2 == "Select Tolerance":
            QMessageBox.warning(self, "Tolerance Error",
                                "Please select tolerance for both elements.")  # Tolerance required
            return

        # ---------- DC ----------
        if mode == "DC":                                          # If DC mode
            total = r1 + r2                                       # Series total resistance Rt = R1 + R2
            current = v / total                                   # Current I = V / Rt

            self.label_18.setText(                                # Display DC series result
                f"--- Circuit Simulation (DC Series) ---\n"
                f"Source: {v} V\n"
                f"R₁: {r1} Ω {tol1}\n"
                f"R₂: {r2} Ω {tol2}\n"
                f"Total Resistance: {total:.3f} Ω\n"
                f"Total Current: {current:.3f} A"
            )
            return                                                # Stop here for DC

        # ---------- AC ----------
        freq = self.get_float(self.lineEdit_freq_3, "Frequency")  # Get frequency for AC (series page)
        if freq is None or freq <= 0:                             # Validate frequency
            QMessageBox.warning(self, "Invalid Frequency",
                                "Frequency must be greater than 0.")
            return

        z1 = self.calc_impedance(self.comboBox_5.currentText(), r1, freq)  # Calculate Z1 for series
        z2 = self.calc_impedance(self.comboBox_6.currentText(), r2, freq)  # Calculate Z2 for series
        if None in [z1, z2]:                                      # If impedance calc fails
            return

        total = z1 + z2                                           # Series total impedance Zt = Z1 + Z2
        current = v / total                                       # Total current I = V / Zt
        ang = cmath.phase(total) * 180 / 3.14159                  # Angle of total impedance in degrees

        self.label_18.setText(                                    # Display AC series result
            f"--- Circuit Simulation (AC Series) ---\n"
            f"Source: {v:.1f} V\n"
            f"Z₁: {abs(z1):.3f} Ω ∠ {cmath.phase(z1) * 180 / 3.14159:.2f}° {tol1}\n"
            f"Z₂: {abs(z2):.3f} Ω ∠ {cmath.phase(z2) * 180 / 3.14159:.2f}° {tol2}\n"
            f"Total Impedance: {abs(total):.3f} Ω ∠ {ang:.2f}°\n"
            f"Total Current: {abs(current):.3f} A"
        )


# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------
app = QApplication(sys.argv)                 # Create the Qt application object
window = MainApp()                           # Create an instance of MainApp (our main window)
window.show()                                # Show the main window on the screen
sys.exit(app.exec_())                        # Start the Qt event loop, exit cleanly when window is closed
