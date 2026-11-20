import json
from aerolab.openfoam import generate_mrf_case


def test_openfoam_case_generator(tmp_path):
    path = generate_mrf_case(tmp_path/"case", 2400, 12.0)
    meta = json.loads((path/"case_metadata.json").read_text())
    assert meta["omega_rad_s"] > 0
    assert (path/"constant/MRFProperties").exists()
    assert "rotatingZone" in (path/"constant/MRFProperties").read_text()
