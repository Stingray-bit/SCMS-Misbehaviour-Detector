
## Project Overview

This project developed a data-driven simulation platform to process real-world vehicular data from an SCMS pilot conducted by the US Department of Transportation (USDOT), simulate Basic Safety Message (BSM) exchanges, and detect attacks including RF level spoofing, speed and acceleration anomalies, and timestamp manipulation. 

**Key features include:**

- **Efficient Data Processing:** Capable of handling large-scale vehicular datasets.
- **Attack Simulation & Detection:** Using the Vehicle class, the system accurately represents both genuine and misbehaving vehicles. The EventMsg class allows for flexible BSM modifications.
- **Misbehaviour Detection:** Incorporates historical data and moving window techniques for detecting RF level, speed, acceleration, and timestamp-related anomalies.
- **Performance Metrics:** Rigorous testing on datasets containing over 9000 endpoints demonstrates the system's efficiency and accuracy.
- **SCMS Compliant Reporting:** The MisbehaviorReport class systematically reports detected anomalies, adhering to SCMS standards.
- **Future Directions:** Focus on enhancing simulation accuracy, integrating machine learning for improved detection, and optimizing scalability of report generation.

**Documentation:**

In order to run the code, navigate to `Main.py`, then adjust the misbehaviour percentage to your liking. It is set as 0.5 by default. If you would like to spoof certain fields to see the consequences, adjust the field dict. BSM class diagram shown below. Right now, the file is configured for testing of detection times. To execute the project, run `Main.py`.

**BSM Class Diagram:**



