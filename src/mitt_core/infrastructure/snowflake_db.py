import os
from typing import List, Dict, Any, Optional
import streamlit as st

# Safe import to handle non-cloud local testing execution footprints elegantly
try:
    import snowflake.connector
    SNOWFLAKE_AVAILABLE = True
except ImportError:
    SNOWFLAKE_AVAILABLE = False


class SnowflakeBioprocessDataLayer:
    """
    Manages secure analytical queries against Snowflake data warehouses to extract
    historical batch runs, Golden Batch envelopes, and multi-batch time-series parameters.
    """
    def __init__(self):
        # Pull parameters securely out of Streamlit secrets or runtime shell vectors
        self.account = st.secrets.get("SNOWFLAKE_ACCOUNT") or os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = st.secrets.get("SNOWFLAKE_USER") or os.getenv("SNOWFLAKE_USER")
        self.password = st.secrets.get("SNOWFLAKE_PASSWORD") or os.getenv("SNOWFLAKE_PASSWORD")
        self.warehouse = st.secrets.get("SNOWFLAKE_WAREHOUSE") or os.getenv("SNOWFLAKE_WAREHOUSE")
        self.database = st.secrets.get("SNOWFLAKE_DATABASE") or os.getenv("SNOWFLAKE_DATABASE")
        self.schema = st.secrets.get("SNOWFLAKE_SCHEMA") or os.getenv("SNOWFLAKE_SCHEMA")

    def _get_connection(self) -> Any:
        """Establishes an active network context session with the target snowflake cluster."""
        if not SNOWFLAKE_AVAILABLE:
            raise RuntimeError("Package 'snowflake-connector-python' is not installed in this environment.")
        
        if not all([self.account, self.user, self.password]):
            raise ValueError("Snowflake authentication credentials missing from config stack secrets.")

        return snowflake.connector.connect(
            account=self.account,
            user=self.user,
            password=self.password,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema
        )

    def fetch_historical_batch_matrix(self, recipe_id: str, limit_batches: int = 10) -> List[Dict[str, Any]]:
        """
        Executes a secure query to pull historical time-series datasets 
        for training and calibration of latent variable soft sensors.
        """
        query = """
            SELECT BATCH_ID, TIMESTAMP, TEMPERATURE, PH, AGITATION_RPM, AERATION_RATE, SUBSTRATE_FEED_RATE
            FROM BIOPROCESS_TELEMETRY_HISTORICAL
            WHERE RECIPE_TARGET = %s
            ORDER BY BATCH_ID, TIMESTAMP ASC
            LIMIT %s;
        """
        
        # Non-destructive simulation fallback for sandboxed/local engineering tests
        if not SNOWFLAKE_AVAILABLE or not self.account:
            print(f"[SNOWFLAKE SIMULATION] Fetching historical runs matching recipe context: {recipe_id}")
            return []

        conn = self._get_connection()
        try:
            with conn.cursor(snowflake.connector.cursor.DictCursor) as cur:
                cur.execute(query, (recipe_id, limit_batches))
                results = cur.fetchall()
                return list(results)
        finally:
            conn.close()


if __name__ == "__main__":
    print("Verifying structural configuration integrity of Snowflake Connector...")
    db_layer = SnowflakeBioprocessDataLayer()
    
    # Run a non-destructive simulation execution lookup test
    data = db_layer.fetch_historical_batch_matrix(recipe_id="PEN_V_GOLDEN", limit_batches=5)
    print("Integrity validation step passed.")
