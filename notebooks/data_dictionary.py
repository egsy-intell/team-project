import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium", css_file="print.css")


@app.cell
def _():
    import marimo as mo

    import pandas as pd
    import xml.etree.ElementTree as ET

    return ET, mo, pd


@app.cell
def _(mo):
    mo.md(r"""
    # Data Dictionary

    ## Predictors
    """)
    return


@app.cell
def _(ET, mo, pd):
    data_dir = mo.notebook_dir() / ".." / "data" / "usgs"

    seawolf_meta_tree = ET.parse(
        data_dir / "seawolf" / "NationalPFASReconLandscapeMetadata.xml"
    )

    mcmahon_dict_df = pd.read_csv(data_dir / "mcmahon" / "PFAS_Data_Dictionary.csv", encoding="latin1")
    mcmahon_env_df = pd.read_csv(data_dir / "mcmahon" / "PFAS_ENV.csv")

    # Data quirk: All values are labeled with <<compound>>-VA
    # except for `"PFBS-V"`. This is a correction
    mcmahon_env_df = mcmahon_env_df.rename(columns={"PFBS-V": "PFBS-VA"})

    # McMahon spells some compounds differently than Smalling despite
    # referring to the same substance; normalize to Smalling's spelling so
    # shared compounds line up as a single row.
    mcmahon_alias = {
        "4_2 FTS": "4:2 FTS",
        "6_2 FTS": "6:2 FTS",
        "8_2 FTS": "8:2 FTS",
        "PFOSA": "FOSA",
        "PFOS ": "PFOS",
    }

    # mcmahon_env_df's "-VA"/"-RMK" columns use McMahon's original spelling;
    # align them here so downstream notebooks receive a dataframe that's
    # already consistent with all_compound_dict_df, without needing
    # mcmahon_alias itself.
    mcmahon_env_df = mcmahon_env_df.rename(
        columns={
            f"{old}-{suffix}": f"{new}-{suffix}"
            for old, new in mcmahon_alias.items()
            for suffix in ("VA", "RMK")
        }
    )

    def _to_float(value):
        return float(value) if value is not None else None

    seawolf_dict_df = pd.DataFrame(
        {
            "attribute": attr.findtext("attrlabl"),
            "definition": attr.findtext("attrdef"),
            "rdom_min": _to_float(attr.findtext(".//rdom/rdommin")),
            "rdom_max": _to_float(attr.findtext(".//rdom/rdommax")),
        }
        for attr in seawolf_meta_tree.findall(".//eainfo/detailed/attr")
    )

    def filter_mcmahon(table_name):
        filter = mcmahon_dict_df["TABLE"] == table_name

        return (
            mcmahon_dict_df.loc[filter, ["PARAMETER", "DEFINITION"]]
            .apply(lambda col: col.str.strip())
        )

    mo.ui.tabs({
        "Seawolf": seawolf_dict_df,
        "McMahon": filter_mcmahon("PFAS_ENV")
    })
    return filter_mcmahon, mcmahon_alias


@app.cell
def _(mo):
    mo.md(r"""
    ## Compounds
    """)
    return


@app.cell
def _(filter_mcmahon, mcmahon_alias, mo, pd):
    # McMahon's PFAS_ENV table mixes non-compound fields (NAWQA_ID, DATE, TIME)
    # and remark-code boilerplate rows in with the actual PFAS compounds, so
    # filter down to rows whose PARAMETER is an actual compound abbreviation.
    _mcmahon_non_compound = {
        "", "NAWQA_ID", "DATE", "TIME",
        "<parameter name>-RMK", "<parameter name>-VA",
        "<", "E", "n",
    }

    _mcmahon_compound_df = (
        filter_mcmahon("PFAS_ENV")
        .rename(columns={"PARAMETER": "compound", "DEFINITION": "definition"})
        .loc[lambda df: ~df["compound"].isin(_mcmahon_non_compound)]
        .assign(compound=lambda df: df["compound"].replace(mcmahon_alias))
        .reset_index(drop=True)
    )

    # Smalling's PFAS_ENV.csv has no accompanying data dictionary, so the
    # compound names are documented here directly.
    _smalling_compound_df = pd.DataFrame(
        [
            {"compound": "PFBA", "definition": "Perfluorobutanoate (PFBA), nanograms per liter"},
            {"compound": "PFPeA", "definition": "Perfluoropentanoate (PFPeA), nanograms per liter"},
            {"compound": "PFHxA", "definition": "Perfluorohexanoate (PFHxA), nanograms per liter"},
            {"compound": "PFHpA", "definition": "Perfluoroheptanoate (PFHpA), nanograms per liter"},
            {"compound": "PFOA", "definition": "Perfluorooctanoate (PFOA), nanograms per liter"},
            {"compound": "PFNA", "definition": "Perfluorononanoate (PFNA), nanograms per liter"},
            {"compound": "PFDA", "definition": "Perfluorodecanoate (PFDA), nanograms per liter"},
            {"compound": "PFBS", "definition": "Perfluorobutane sulfonate (PFBS), nanograms per liter"},
            {"compound": "PFPeS", "definition": "Perfluoropentane sulfonate (PFPeS), nanograms per liter"},
            {"compound": "PFHxS", "definition": "Perfluorohexane sulfonate (PFHxS), nanograms per liter"},
            {"compound": "PFHpS", "definition": "Perfluoroheptane sulfonate (PFHpS), nanograms per liter"},
            {"compound": "PFOS", "definition": "Perfluorooctane sulfonate (PFOS), nanograms per liter"},
            {"compound": "PFDS", "definition": "Perfluorodecane sulfonate (PFDS), nanograms per liter"},
            {"compound": "PFPrS", "definition": "Perfluoropropane sulfonate (PFPrS), nanograms per liter"},
            {"compound": "6:2 FTS", "definition": "6:2 Fluorotelomer sulfonate (6:2 FTS), nanograms per liter"},
            {"compound": "FOSA", "definition": "Perfluorooctane sulfonamide (FOSA, also called PFOSA), nanograms per liter"},
            {"compound": "HFPO-DA;GenX", "definition": "Hexafluoropropylene oxide dimer acid (HFPO-DA, trade name GenX), nanograms per liter"},
        ]
    )

    all_compound_dict_df = (
        pd.merge(
            _mcmahon_compound_df,
            _smalling_compound_df,
            on="compound",
            how="outer",
            suffixes=("_mcmahon", "_smalling"),
            indicator=True,
        )
        .assign(
            definition=lambda df: df["definition_mcmahon"].fillna(df["definition_smalling"]),
            mcmahon=lambda df: df["_merge"].isin(["left_only", "both"]),
            smalling=lambda df: df["_merge"].isin(["right_only", "both"]),
        )
        .loc[:, ["compound", "definition", "mcmahon", "smalling"]]
        .sort_values("compound")
        .reset_index(drop=True)
    )

    _factors_dir = mo.notebook_dir() / ".." / "data" / "factors"
    _tq_benchmark_df = pd.read_csv(_factors_dir / "pfas_tq_benchmarks_epa_aligned.csv")

    all_compound_dict_df = all_compound_dict_df.merge(
        _tq_benchmark_df, on="compound", how="left"
    )
    return


if __name__ == "__main__":
    app.run()
