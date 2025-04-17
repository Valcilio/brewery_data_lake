"""Module for testing the BreweryTransformer class."""

from pandas import DataFrame

from domain.usecases.brewerytransformer import BreweryTransformer


def test_structure_into_dataframe(test_json_raw: list):
    """Test the structure_into_dataframe method of BreweryTransformer."""

    df = BreweryTransformer().structure_into_dataframe(test_json_raw)
    assert isinstance(df, DataFrame)


def test_get_brewery_quantity_aggregated_by_location_and_type(
    test_parquet_raw: DataFrame,
):
    """Test the get_brewery_quantity_aggregated_by_location_and_type method."""

    df_agg = BreweryTransformer().get_brewery_quantity_aggregated_by_location_and_type(
        test_parquet_raw
    )

    assert isinstance(df_agg, DataFrame)
    assert "brewery_type" in df_agg.columns
    assert "country" in df_agg.columns
    assert "state_province" in df_agg.columns
    assert "city" in df_agg.columns
