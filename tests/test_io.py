import pandas as pd
import pytest
from aerolab.io import load_propeller_data
from aerolab.exceptions import DataValidationError


def test_loader_rejects_missing_columns(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"rpm": [1000]}).to_csv(path, index=False)
    with pytest.raises(DataValidationError, match="Missing required"):
        load_propeller_data(path)


def test_loader_rejects_zero_rpm(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({
        "run_id": ["A"], "time_s": [0], "rpm": [0], "thrust_N": [1],
        "torque_Nm": [0.1], "airspeed_m_s": [2], "density_kg_m3": [1.2],
        "diameter_m": [0.2],
    }).to_csv(path, index=False)
    with pytest.raises(DataValidationError, match="rpm must be positive"):
        load_propeller_data(path)
