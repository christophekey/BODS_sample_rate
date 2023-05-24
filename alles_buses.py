import os
import sys
import traci

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

# Start SUMO and load the network
sumo_bin = os.path.join(os.environ["SUMO_HOME"], "bin", "sumo")
sumo_cmd = [sumo_bin, "-c", "test_network/network.sumocfg"]
traci.start(sumo_cmd)

# Get the list of traffic light junctions
junction_ids = traci.trafficlight.getIDList()
for junction_id in junction_ids:
    print(f"Junction ID: {junction_id}")
# Set the traffic light program TLS for each junction

for junction_id in junction_ids:
    program_id = f"{junction_id}"
    program_logics = traci.trafficlight.getAllProgramLogics(junction_id)
    program_definition = "<additional>\n"
    program_definition += f'<program id="{program_id}" type="static" programID="{program_id}">\n'
    for logic in program_logics:
        phases = logic.getPhases()
        for phase in phases:
            duration = phase.duration
            state = phase.state
            program_definition += f'<phase duration="{duration}" state="{state}" />\n'
    program_definition += "</program>\n"
    program_definition += "</additional>\n"
    traci.junction.setParameter(junction_id, "programDefinition", program_definition)

# Simuluate the Scenario
simulation_steps = 100
for step in range(simulation_steps):
    traci.simulationStep()
    # check for a bus
    for junction_id in junction_ids:
        bus_ids = traci.junction.getIDList()
        if len(bus_ids) > 0:
            traci.trafficlight.setProgram(junction_id, f"{junction_id}_program")
            break
        else:
            traci.trafficlight.setProgram(junction_id, "0")

traci.close()
