"""Generate a documented OpenFOAM case skeleton for a rotating propeller region.

The generated case is a starter template. Boundary patches must match the mesh,
and users must review solver/model choices before execution.
"""
from pathlib import Path
import json


def generate_mrf_case(output_dir, rpm, inlet_velocity_m_s, density_kg_m3=1.225,
                      turbulence_model="kOmegaSST"):
    if rpm <= 0 or density_kg_m3 <= 0:
        raise ValueError("rpm and density must be positive.")
    out = Path(output_dir)
    (out/"0").mkdir(parents=True, exist_ok=True)
    (out/"constant").mkdir(exist_ok=True)
    (out/"system").mkdir(exist_ok=True)
    omega = rpm*2*3.141592653589793/60
    control = """FoamFile
{
    version 2.0;
    format ascii;
    class dictionary;
    object controlDict;
}
application simpleFoam;
startFrom startTime;
startTime 0;
stopAt endTime;
endTime 2000;
deltaT 1;
writeControl timeStep;
writeInterval 200;
purgeWrite 0;
writeFormat ascii;
writePrecision 8;
writeCompression off;
timeFormat general;
timePrecision 6;
runTimeModifiable true;
"""
    fv_solution = f"""FoamFile
{{
    version 2.0;
    format ascii;
    class dictionary;
    object fvSolution;
}}
solvers
{{
    p {{ solver GAMG; tolerance 1e-7; relTol 0.01; smoother GaussSeidel; }}
    U {{ solver smoothSolver; smoother symGaussSeidel; tolerance 1e-8; relTol 0.1; }}
    k {{ solver smoothSolver; smoother symGaussSeidel; tolerance 1e-8; relTol 0.1; }}
    omega {{ solver smoothSolver; smoother symGaussSeidel; tolerance 1e-8; relTol 0.1; }}
}}
SIMPLE {{ nNonOrthogonalCorrectors 2; }}
relaxationFactors {{ fields {{ p 0.3; }} equations {{ U 0.7; k 0.7; omega 0.7; }} }}
"""
    fv_schemes = """FoamFile
{
    version 2.0;
    format ascii;
    class dictionary;
    object fvSchemes;
}
ddtSchemes { default steadyState; }
gradSchemes { default Gauss linear; }
divSchemes
{
    default none;
    div(phi,U) bounded Gauss linearUpwind grad(U);
    div(phi,k) bounded Gauss upwind;
    div(phi,omega) bounded Gauss upwind;
}
laplacianSchemes { default Gauss linear corrected; }
interpolationSchemes { default linear; }
snGradSchemes { default corrected; }
"""
    transport = """FoamFile
{
    version 2.0;
    format ascii;
    class dictionary;
    object transportProperties;
}
transportModel Newtonian;
nu [0 2 -1 0 0 0 0] 1.5e-05;
"""
    mrf = f"""FoamFile
{{
    version 2.0;
    format ascii;
    class dictionary;
    object MRFProperties;
}}
MRF1
{{
    cellZone rotatingZone;
    active yes;
    nonRotatingPatches (inlet outlet casing);
    origin (0 0 0);
    axis (0 0 1);
    omega {omega:.8f};
}}
"""
    metadata = {
        "rpm": rpm, "omega_rad_s": omega,
        "inlet_velocity_m_s": inlet_velocity_m_s,
        "density_kg_m3": density_kg_m3,
        "turbulence_model_requested": turbulence_model,
        "status": "starter_case_requires_mesh_and_boundary_condition_review",
        "required_mesh_patches": ["inlet", "outlet", "casing", "blade", "hub"],
        "required_cell_zone": "rotatingZone",
        "review_before_run": True,
    }
    (out/"system/controlDict").write_text(control)
    (out/"system/fvSolution").write_text(fv_solution)
    (out/"system/fvSchemes").write_text(fv_schemes)
    (out/"constant/transportProperties").write_text(transport)
    (out/"constant/MRFProperties").write_text(mrf)
    (out/"case_metadata.json").write_text(json.dumps(metadata, indent=2))
    (out/"README_CASE.md").write_text(
        "# OpenFOAM MRF starter case\n\n"
        "This generator creates solver dictionaries and case metadata only. "
        "It does not generate a mesh, boundary files, turbulence fields, or a "
        "validated converged simulation. Match patch names and rotating cell zone "
        "to your mesh, set inlet/outlet and wall conditions in `0/`, review the "
        "turbulence model and fluid properties, then run the appropriate OpenFOAM "
        "version. Check residuals and force histories before accepting results.\n"
    )
    return out
