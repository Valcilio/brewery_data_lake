"""Module to transform brewery data into a structured format."""

import pandas as pd

from domain.utils.etllogger import ETLLogger

LOGGER = ETLLogger("BreweryTransformer").get_logger()


class BreweryTransformer:
    """Transform the brewery data into a structured format."""

    @staticmethod
    def structure_into_dataframe(data: list) -> pd.DataFrame:
        """Structure the extracted data into a DataFrame.

        Args:
            data (list): The extracted data in JSON format."""

        LOGGER.info("Structuring json (in list format) into DataFrame.")
        df = pd.DataFrame(data)

        return df

    @staticmethod
    def get_brewery_quantity_aggregated_by_location_and_type(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Aggregate the brewery data by location and brewery type.

        Args:
            df (pd.DataFrame): The DataFrame containing brewery data."""

        group_by_columns = ["brewery_type", "country", "state_province", "city"]
        LOGGER.info(f"Grouping data data by {group_by_columns}.")
        grouped_df = df.groupby(group_by_columns, observed=True)
        LOGGER.info("Aggregating data grouped by the count of the IDs.")
        df_agg = grouped_df.aggregate({"id": "count"}).reset_index()
        LOGGER.info("Sorting by brewery type.")
        sorted_df = df_agg.sort_values("brewery_type")

        return sorted_df
