def get_electric_field_vector(df) -> np.ndarray:
    if df.empty:
        return np.zeros(3, dtype=complex)
    return np.array([
        df["electric_field_x"].values.mean(),
        df["electric_field_y"].values.mean(),
        df["electric_field_z"].values.mean(),
    ])  # shape (3,), dtype complex

def generate_energy_beamlines(template_path, min_e=30, max_e=1000) -> list:
    """
    Generates diffrent beamlines for a range of photon energies based on a template RML file.
    Sets the energy of each source to the current energy.
    Returns:
        A list of beamline objects.
    """

    # Check if min_e and max_e are valid
    if min_e >= max_e or max_e <= min_e:
        print("Invalid energy range")
        return []

    template_path = template_path
    beamlines = []

    for energy in range(min_e, max_e + 1):
        bl = rayx.import_beamline(template_path)
        bl.sources[0].energy = energy
        beamlines.append(bl)

    return beamlines