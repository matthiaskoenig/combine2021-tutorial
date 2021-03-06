"""

"""

from pathlib import Path

import roadrunner
from sbmlutils.cytoscape import visualize_sbml
from sbmlutils.factory import *
from sbmlutils.metadata import *
from pymetadata.omex import *


class U(Units):
    min = UnitDefinition("min")
    mmole = UnitDefinition("mmole")
    mmole_per_min = UnitDefinition("mmole_per_min", "mmole/min")
    mM = UnitDefinition("mM", "mmole/liter")


_m = Model(
    sid="model1",
    name="Example model from COMBINE2021",
    notes="""
    # COMBINE2021 model
    This model was built within the **tutorial session**.
    """,
    units=U,
    model_units=ModelUnits(
        time=U.min,
        substance=U.mmole,
        extent=U.mmole,
        length=U.meter,
        volume=U.liter
    ),
    compartments=[
        Compartment(
            sid="c",
            value=1.0,
            sboTerm=SBO.PHYSICAL_COMPARTMENT,
            name="cytosol",
            annotations=[
                (BQB.IS, "ncit/C61554"),
                (BQB.IS, "GO:0005829"),
                (BQB.IS, "FMA:66836"),
            ],
            unit=U.liter
        ),
    ],
    species=[
        Species(
            sid="glc",
            compartment="c",
            initialConcentration=10.0,
            hasOnlySubstanceUnits=False,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            name="glucose",
            annotations=[
                (BQB.IS, "ncit/C2831"),
                (BQB.IS, "CHEBI:17234"),
            ],
            substanceUnit=U.mmole
        ),
        Species(
            sid="glc6p",
            compartment="c",
            initialConcentration=0.0,
            hasOnlySubstanceUnits=False,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            name="glucose 6-phosphate",
            annotations=[
                # FIXME
            ],
            substanceUnit=U.mmole
        )
    ],
    reactions=[
        Reaction(
            sid="HK",
            name="hexokinase",
            sboTerm=SBO.BIOCHEMICAL_REACTION,
            equation="glc -> glc6p",
            pars=[
                Parameter("HK_Vmax", 10.0, U.mmole_per_min,
                          sboTerm=SBO.MAXIMAL_VELOCITY),
                Parameter("HK_Km_glc", 0.1, U.mM, sboTerm=SBO.MICHAELIS_CONSTANT,
                          notes="""
                          From ABC1987: Km = 0.1 +- 0.02 mM
                          """),
            ],
            formula=("HK_Vmax * glc/(glc + HK_Km_glc)", U.mmole_per_min)
        )
    ]
)


def simulate(sbml_path: Path):
    import pandas as pd
    r: roadrunner.RoadRunner = roadrunner.RoadRunner(str(sbml_path))
    _s = r.simulate(start=0, end=10, steps=1000)
    r.plot(_s)
    s = pd.DataFrame(_s, columns=_s.colnames)
    print(s)


if __name__ == "__main__":
    fac_result = create_model(
        _m,
        output_dir=Path(__file__).parent / "results",
        units_consistency=True,
    )
    print(
        "Report: ",
        "https://sbml4humans.de/model_url?url=http://be86-77-13-36-21.ngrok.io/model1.xml",
    )
    simulate(fac_result.sbml_path)

    visualize_sbml(sbml_path=fac_result.sbml_path,
                   delete_session=False)

    omex = Omex()
    omex.add_entry(
        fac_result.sbml_path,
        ManifestEntry(
            location="./model1.xml", format=EntryFormat.SBML_L3V2
        )
    )
    omex.to_omex(
        Path(__file__).parent / "model1.omex"
    )
