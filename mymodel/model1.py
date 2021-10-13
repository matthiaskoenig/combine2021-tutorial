"""

"""

from pathlib import Path

from sbmlutils.factory import *
from sbmlutils.metadata import *

_m = Model(
    sid="model1",
    name="Example model from COMBINE2021",
    notes="""
    # COMBINE2021 model
    This model was built within the **tutorial session**.
    """,
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
        )
    ],
)


if __name__ == "__main__":
    create_model(
        _m,
        output_dir=Path(__file__).parent / "results",
        units_consistency=False,
    )
    print(
        "Report: ",
        "https://sbml4humans.de/model_url?url=http://be86-77-13-36-21.ngrok.io/model1.xml",
    )
