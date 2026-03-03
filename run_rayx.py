import sys, json, rayx, app
import pandas as pd

"""
This lightweight script traces a RayX beamline and writes the resulting dataframe to a json file.
It is run by the single_run_job.sh script.
"""

# Read input arguments and output json path
# Both come from the command line in the single_run_job.sh
rml_path, results_path = sys.argv[1], sys.argv[2]

# Run the RayX simulation
beamline = rayx.import_beamline(rml_path)
traced_beamline = beamline.trace()

# Turn the traced beamline into a dataframe
columns = [
                "direction_x", "direction_y", "direction_z",
                "electric_field_x", "electric_field_y", "electric_field_z",
                "energy", "event_type",
                "last_element_id", "order", "path_length",
                "position_x", "position_y", "position_z",
                "ray_id", "source_id",
            ]

df = pd.DataFrame({col: getattr(traced_beamline, col) for col in columns})

# Write the dataframe to a json file
df.to_json(results_path, orient="records")