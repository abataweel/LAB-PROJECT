from PyQt5.uic import loadUi  # load UI definitions from .ui file
import sys  # access to argv and exit
from PyQt5.QtWidgets import QMainWindow, QApplication  # main window and app classes


class Source:
    def __init__(self, voltage):
        self.voltage = voltage  # supply voltage value


class Resistor:
    def __init__(self, resistance, tolerance):
        self.resistance = resistance  # resistance in ohms
        self.tolerance = tolerance  # tolerance percentage


class Circuit:
    def __init__(self, source):
        self.source = source  # Source instance
        self.resistors = []  # list to hold resistors

    def add_resistor(self, resistor):
        self.resistors.append(resistor)  # append a resistor to the circuit

    def simulate(self):
        lines = ["Circuit Simulation", f"Source voltage: {self.source.voltage} V"]  # header lines

        total_resistance = 0  # accumulator for total resistance
        for i, r in enumerate(self.resistors, start=1):  # iterate over resistors
            lines.append(f"Resistor {i}: {int(r.resistance)} Ω ±{int(r.tolerance)}%")  # formatted resistor line
            total_resistance += r.resistance  # add each resistor value

        if total_resistance == 0:  # avoid division by zero
            lines.append("Total current: undefined (total resistance is 0)")  # message for zero resistance
        else:
            current = self.source.voltage / total_resistance  # calculate current
            lines.append(f"Total current: {current:.3f} A")  # formatted current line

        output = "\n".join(lines)  # join lines for output
        return output  # return full message


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # initialize base class
        loadUi("lab_project.ui", self)  # load UI layout
        self.pushButton.clicked.connect(self.simulate)  # connect button to simulate
        self.label_4.setWordWrap(True)  # allow label text wrapping



    def _parse_tolerance(self, combo_text):
        text = combo_text.strip()  # clean text
        if not text or "Select" in text:  # check placeholder
            return None  # no selection
        if text.startswith("±"):  # tolerance like ±5%
            text = text[1:]  # strip leading ±
        if text.endswith("%"):  # strip percent sign
            text = text[:-1]  # remove '%'
        try:
            return float(text)  # convert to float
        except ValueError:
            return None  # invalid format

    def simulate(self):
        try:
            r1_value = float(self.lineEdit.text())  # read Resistor 1 input
            r2_value = float(self.lineEdit_2.text())  # read Resistor 2 input
            voltage_value = float(self.lineEdit_3.text())  # read Voltage input
        except ValueError:
            self.label_4.setText("Please enter valid numbers for Resistor 1, Resistor 2, and Voltage.")  # show error
            self.statusbar.clearMessage()  # clear status bar
            return  # exit on invalid input

        tol1 = self._parse_tolerance(self.comboBox1.currentText())  # parse tolerance for Resistor 1
        tol2 = self._parse_tolerance(self.comboBox2.currentText())  # parse tolerance for Resistor 2
        if tol1 is None or tol2 is None:  # ensure both tolerances selected
            self.label_4.setText("Please select tolerances for Resistor 1 and Resistor 2.")  # show error
            self.statusbar.clearMessage()  # clear status bar
            return  # exit on missing tolerance

        source = Source(voltage_value)  # create source
        circuit = Circuit(source)  # create circuit with source
        circuit.add_resistor(Resistor(r1_value, tol1))  # add first resistor with tolerance
        circuit.add_resistor(Resistor(r2_value, tol2))  # add second resistor with tolerance

        output = circuit.simulate()  # run simulation
        self.label_4.setText(output)  # display full message in label
        self.statusbar.clearMessage()  # clear status bar


if __name__ == "__main__":
    app = QApplication(sys.argv)  # create application
    window = MainWindow()  # create main window
    window.show()  # show window
    sys.exit(app.exec_())  # start event loop
