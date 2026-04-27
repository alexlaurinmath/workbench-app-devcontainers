# BigQuery Dashboard App

An interactive dashboard for visualizing BigQuery data with summary statistics, built for Verily Workbench.

## Features

- 📊 **Summary Statistics**: View row counts, column counts, and dataset metadata
- 📈 **Data Visualization**: Automatic bar chart generation from numeric columns
- 📋 **Data Table**: Browse raw data in a clean, responsive table format
- ⚡ **Static Display**: Data is embedded for fast, efficient loading
- 🔒 **BigQuery Integration**: Securely query data from Google BigQuery

## Deployment to Workbench

1. **In Workbench UI**, create a new custom application:
   - **Repository**: `https://github.com/YOUR-ORG/workbench-app-devcontainers.git`
   - **Branch**: `main` (or your branch name)
   - **Folder**: `src/dashboard-app`

2. **Wait for the app to build and start** (this may take a few minutes)

3. **Access your dashboard** at:
   ```
   https://workbench.verily.com/app/[APP_UUID]/proxy/8080/
   ```

To get the APP_UUID, run:
```bash
wb app list --format=json | jq -r '.[] | select(.status == "RUNNING") | .id' | head -1
```

## Current Configuration

The dashboard is configured to query:
- **Table**: `wb-buoyant-okra-4591.clean_output_himss.ConditionView`
- **Sample Size**: 1000 rows (configurable)
- **Total Row Count**: Queried separately via `COUNT(*)`

## Customization

### Change the BigQuery Query

Edit `app.py` and modify the queries:

1. **Row count query** (line 20):
   ```python
   count_query = """
   SELECT COUNT(*) as total_rows
   FROM `your-project.your-dataset.your-table`
   """
   ```

2. **Sample data query** (line 40):
   ```python
   query = """
   SELECT *
   FROM `your-project.your-dataset.your-table`
   LIMIT 1000
   """
   ```

Replace with your actual project, dataset, and table names.

### Adjust the Data Limit

By default, the query limits results to 1000 rows. Increase or decrease the `LIMIT` value as needed:

```python
LIMIT 5000  # Fetch up to 5000 rows
```

## Local Testing

To test the dashboard locally before deploying:

1. **Create the Docker network**:
   ```bash
   docker network create app-network
   ```

2. **Build and run the container**:
   ```bash
   cd src/dashboard-app
   docker compose up --build
   ```

3. **Access the dashboard**:
   ```
   http://localhost:8080
   ```

## Troubleshooting

### Data doesn't load

1. **Check BigQuery authentication**: Ensure the Workbench environment has access to your BigQuery project
2. **Verify the table name**: Make sure the table path in `app.py` is correct
3. **Check server logs**: Run `docker logs application-server` to see errors

### Server won't start

1. **Check if port is in use**:
   ```bash
   lsof -i :8080
   ```

2. **Kill existing process**:
   ```bash
   kill $(lsof -t -i :8080)
   ```

### Changes don't appear

After editing code:
1. **Rebuild the container**: `docker compose up --build`
2. **Hard refresh browser**: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

## Architecture

- **Backend**: Flask (Python 3.11)
- **Frontend**: HTML + Plotly.js for charts
- **Data Source**: Google BigQuery
- **Deployment**: Docker container in Workbench

## Key Files

- `app.py`: Flask application with API endpoints
- `templates/index.html`: Dashboard UI
- `Dockerfile`: Container build instructions
- `docker-compose.yaml`: Container orchestration
- `.devcontainer.json`: Workbench configuration
- `requirements.txt`: Python dependencies

## Security Notes

- The server binds to `0.0.0.0` to allow Workbench proxy access
- CORS is enabled for cross-origin requests
- Debug mode is disabled for production use
- All API calls use relative paths to work behind the proxy
