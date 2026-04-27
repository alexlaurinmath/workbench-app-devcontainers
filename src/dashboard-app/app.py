from flask import Flask, render_template, jsonify
from flask_cors import CORS
from google.cloud import bigquery
import os

app = Flask(__name__)
app.config['STRICT_SLASHES'] = False  # Prevents 308 redirects behind the proxy
CORS(app)

# Cache for data
_data_cache = None
_row_count_cache = None

def get_table_row_count():
    """
    Get the total row count from the BigQuery table.
    """
    global _row_count_cache
    if _row_count_cache is not None:
        return _row_count_cache

    client = bigquery.Client()

    # Query to get total row count
    count_query = """
    SELECT COUNT(*) as total_rows
    FROM `wb-buoyant-okra-4591.clean_output_himss.ConditionView`
    """

    try:
        result = client.query(count_query).to_dataframe()
        _row_count_cache = int(result['total_rows'].iloc[0])
        return _row_count_cache
    except Exception as e:
        print(f"Error getting row count: {e}")
        raise

def get_bigquery_data():
    """
    Fetch sample data from BigQuery.
    """
    global _data_cache
    if _data_cache is not None:
        return _data_cache

    client = bigquery.Client()

    # Query to get sample data from the table
    query = """
    SELECT *
    FROM `wb-buoyant-okra-4591.clean_output_himss.ConditionView`
    LIMIT 1000
    """

    try:
        df = client.query(query).to_dataframe()
        _data_cache = df.to_dict(orient='records')
        return _data_cache
    except Exception as e:
        print(f"Error querying BigQuery: {e}")
        raise

@app.route('/')
def index():
    """Serve the main dashboard page."""
    return render_template('index.html')

@app.route('api/data')
def get_data():
    """API endpoint to fetch data."""
    try:
        data = get_bigquery_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('api/metadata')
def get_metadata():
    """API endpoint to fetch metadata about the dataset."""
    try:
        data = get_bigquery_data()
        total_rows = get_table_row_count()
        if data:
            return jsonify({
                "columns": list(data[0].keys()),
                "row_count": total_rows,
                "sample_size": len(data)
            })
        return jsonify({"columns": [], "row_count": 0, "sample_size": 0})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # CRITICAL: host='0.0.0.0' required for Workbench proxy access
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
