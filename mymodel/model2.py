"""

"""

from pathlib import Path

from sbmlutils.cytoscape import visualize_sbml
from sbmlutils.factory import *
from sbmlutils.metadata import *


class U(Units):
    min = UnitDefinition("min")
    mmole = UnitDefinition("mmole")
    mmole_per_min = UnitDefinition("mmole_per_min", "mmole/min")
    mM = UnitDefinition("mM", "mmole/liter")


_m = Model(
    sid="model2",
    name="Example model from COMBINE2021 linear chain",
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
    parameters=[
        Parameter("R_Vmax", 10.0, U.mmole_per_min,
                          sboTerm=SBO.MAXIMAL_VELOCITY),
        Parameter("R_Km", 0.1, U.mM, sboTerm=SBO.MICHAELIS_CONSTANT)
    ],
    species=[
        Species(
            sid="S0",
            compartment="c",
            initialConcentration=10.0,
            hasOnlySubstanceUnits=False,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            name="S0",
            annotations=[
            ],
            substanceUnit=U.mmole
        ),
    ],
    reactions=[
    ]
)

n_chain = 10
for k in range(n_chain):
    _m.species.append(
        Species(
            sid=f"S{k+1}",
            compartment="c",
            initialConcentration=0.0,
            hasOnlySubstanceUnits=False,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            name=f"S{k+1}",
            substanceUnit=U.mmole
        )
    )
    _m.reactions.append(
        Reaction(
            sid=f"R{k}",
            name=f"R{k}",
            sboTerm=SBO.BIOCHEMICAL_REACTION,
            equation=f"S{k} -> S{k+1}",
            formula=(f"R_Vmax * S{k}/(S{k} + R_Km)", U.mmole_per_min)
        )
    )


if __name__ == "__main__":
    fac_result = create_model(
        _m,
        output_dir=Path(__file__).parent / "results",
        units_consistency=True,
    )
    print(
        "Report: ",
        "https://sbml4humans.de/model_url?url=http://be86-77-13-36-21.ngrok.io/model2.xml",
    )
    visualize_sbml(sbml_path=fac_result.sbml_path,
                   delete_session=False)