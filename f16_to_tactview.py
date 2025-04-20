import jsbsim
import pandas as pd
import math
import os

# === CONFIGURATION ===
JSBSIM_ROOT = "path to jasbsim folder"
OUTPUT_CSV = "f16_simple_flight.csv"

# === SETUP JSBSim ===
sim = jsbsim.FGFDMExec(root_dir=JSBSIM_ROOT)
sim.set_aircraft_path("aircraft")
sim.load_model("f16")

# === INITIAL CONDITIONS ===
sim["ic/h-sl-ft"] = 20000
sim["ic/vc-kts"] = 320
sim["ic/psi-true-deg"] = 90
sim["ic/theta-deg"] = 5
sim["ic/alpha-deg"] = 8
sim["ic/phi-deg"] = 0
sim["ic/beta-deg"] = 0
sim["ic/lat-gc-deg"] = 32.9
sim["ic/long-gc-deg"] = -97.0

sim.run_ic()
dt = 0.01
sim.set_dt(dt)

data = []

# === SIMULATE STRAIGHT FLIGHT ===
for _ in range(3000):  # 30 seconds
    sim["fcs/throttle-cmd-norm"] = 1.0
    sim["fcs/elevator-cmd-norm"] = -0.3
    sim["fcs/aileron-cmd-norm"] = 0.0
    sim["fcs/rudder-cmd-norm"] = 0.0
    sim.run()

    # Compute heading from velocity vector
    vel_north = sim["velocities/v-north-fps"]
    vel_east = sim["velocities/v-east-fps"]
    heading_rad = math.atan2(vel_east, vel_north)
    heading_deg = math.degrees(heading_rad) % 360

    data.append({
        "Time": sim.get_sim_time(),
        "Longitude": sim["position/long-gc-deg"],
        "Latitude": sim["position/lat-gc-deg"],
        "Altitude": sim["position/h-sl-ft"] * 0.3048,
        "Roll (deg)": sim["attitude/phi-deg"],
        "Pitch (deg)": sim["attitude/theta-deg"],
        "Yaw (deg)": heading_deg
    })

# === SAVE CSV ===
df = pd.DataFrame(data)
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Simple flight saved to: {os.path.abspath(OUTPUT_CSV)}")
