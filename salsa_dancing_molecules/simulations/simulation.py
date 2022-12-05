def run(sim_info, atoms):
    # TODO: implement real simulation
    f = open(sim_info["traj_output_path"], "w")
    f.write(sim_info["potential"])
    f.close()
    f = open(sim_info["csv_output_path"], "w")
    f.write(sim_info["ensemble"])
    f.close()
