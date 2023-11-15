Project Overview:
This project developed a data-driven simulation platform to process real-world vehicular data, simulate Basic Safety Message (BSM) exchanges, and detect attacks. Key features include:

Efficient Data Processing: Capable of handling large-scale vehicular datasets.
Attack Simulation & Detection: Using the Vehicle class, the system accurately represents both genuine and misbehaving vehicles. The EventMsg class allows for flexible BSM modifications.
Advanced Misbehaviour Detection: Incorporates historical data and moving window techniques for detecting RF level, speed, acceleration, and timestamp-related anomalies.
Performance Metrics: Rigorous testing on datasets containing over 9000 endpoints demonstrates the system's efficiency and accuracy.
SCMS Compliant Reporting: The MisbehaviorReport class systematically reports detected anomalies, adhering to SCMS standards.
Future Directions: Focus on enhancing simulation accuracy, integrating machine learning for improved detection, and optimizing scalability of report generation.

Documentation:
In order to run the code, navigate to Main.py, then adjust the misbehaviour perentage to your liking. It is set as 0.5 by default. If you would like to spoof certain fields to see the consequences, adjust the field dict. BSM class diagram shown below. Right now the file is configured for testing of detection times. To execute the project, run Main.py

BSM class diagram:

EventMsg
│
├── eventMsgSeqNum (int)
│
└── BsmRecord
    │
    ├── MsgHeader
    │   ├── myRFLevel (int)
    │   └── authenticated (bool)
    │
    └── BsmMsg
        │
        ├── CoreData
        │   ├── msgCnt (int)
        │   ├── id (str)
        │   ├── accuracy
        │   │   ├── semiMajor (int)
        │   │   ├── semiMinor (int)
        │   │   └── orientation (int)
        │   ├── transmission (str)
        │   ├── angle (int)
        │   ├── accelSet
        │   │   ├── long_mpss (float)
        │   │   ├── lat_mpss (float)
        │   │   ├── vert_mpss (float)
        │   │   └── yaw_dps (float)
        │   ├── brakes
        │   │   ├── wheelBrakes (str)
        │   │   ├── traction (str)
        │   │   ├── abs (str)
        │   │   ├── scs (str)
        │   │   ├── brakeBoost (str)
        │   │   └── auxBrakes (str)
        │   ├── size
        │   │   ├── width (int)
        │   │   └── length (int)
        │   ├── X_m (float)
        │   ├── Y_m (float)
        │   ├── Z_m (float)
        │   ├── T_s (float)
        │   ├── speed_mps (int)
        │   └── heading_deg (float)
        │
        └── PartII (list of PartII objects)
            ├── partII_Id (int)
            └── partII_Value
                ├── classification (int, optional)
                ├── vehicleData
                │   ├── height (int, optional)
                │   └── mass (int, optional)
                ├── pathHistory
                │   └── crumbData (list of CrumbData objects)
                │       ├── xOffset_m (float)
                │       ├── yOffset_m (float)
                │       ├── zOffset_m (float)
                │       └── tOffset_s (float)
                └── pathPrediction
                    ├── radiusOfCurve (int, optional)
                    └── confidence (int, optional)
