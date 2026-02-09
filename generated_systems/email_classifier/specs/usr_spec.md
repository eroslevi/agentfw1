# User System Specification: 24-hour Weather Forecaster (Multi-agent)

## Project Title
24-hour Weather Forecaster (uses past 168h data)

## Project Description
An intelligent multi-agent system that gathers the last 168 hours of weather data from a weather API, processes and aggregates that data, and generates an hour-by-hour weather prediction for the next 24 hours. Predictions are reviewed and annotated by an AI reviewer agent which validates, corrects, and provides reasoning and confidence scores.

## Primary Goals

1. **Data Collection**: Continuously fetch and store the last 168 hours of weather observations (temperature, humidity, wind, precipitation, pressure, cloud cover, timestamps) from a configurable weather API.
2. **Preprocessing & Feature Engineering**: Clean, resample, and compute features (trend, moving averages, diurnal cycles) from the 168h window.
3. **Forecasting**: Produce an hourly forecast for the next 24 hours (temperature, precipitation probability, wind speed, cloud cover) with numerical values and confidence scores.
4. **AI Review**: An AI reviewer agent inspects the generated forecast, checks for anomalies, adjusts confidence, and provides human-readable explanations for each hour.
5. **Deliverable Output**: Return a structured JSON forecast plus a short human summary and audit trail of data sources and reviewer notes.

## Key Requirements

- Fetch and store up to 168 hours of historical observations from a specified weather API (e.g., OpenWeatherMap) with timestamps in UTC.
- Update data at a configurable cadence (e.g., hourly) and support on-demand refresh.
- Forecast generation latency: < 5 seconds for a 24-hour forecast after data is available.
- Forecast confidence scoring per hour and per variable.
- AI reviewer must run automatically after forecasting and can propose adjustments.
- Output must include an audit trail: data fetch times, API endpoints, versions of models/algorithms used, and reviewer annotations.

## Input Data / Context

1. **Configuration**: API endpoint URI, API key, location (lat, lon), units, update cadence.
2. **Historical Observations**: Last 168 hours of data fields:
   - timestamp (UTC)
   - temperature (°C)
   - humidity (%)
   - wind_speed (m/s)
   - precipitation (mm)
   - pressure (hPa)
   - cloud_cover (%)
3. **Optional Context**: Local terrain notes, station elevation, known sensor biases.

## Expected Output

1. **Hourly Forecast (24 items)**
```json
{
  "location": {"lat": 59.33, "lon": 18.07},
  "generated_at": "2026-02-09T10:00:00Z",
  "hourly_forecast": [
    {
      "hour": "2026-02-09T11:00:00Z",
      "temperature_c": 3.2,
      "precip_prob": 0.12,
      "wind_m_s": 4.5,
      "cloud_cover": 60,
      "confidence": 0.87,
      "reviewer_note": "Matches short-term trend; slight uncertainty due to recent pressure drop"
    }
    /* ... 23 more entries ... */
  ],
  "summary": "Light rain expected overnight, temperatures near freezing."
}
```

2. **Audit & Metadata**:
   - `data_window`: start/end timestamps of the 168h data
   - `api_calls`: list of calls with timestamps and status
   - `model_version`: forecasting algorithm version
   - `reviewer_version`: AI reviewer model/version

## Agents (high-level)

- **DataCollector**: Fetches and stores historical observations from the weather API, handles retries and rate limits.
- **Preprocessor**: Cleans data, resamples to hourly, computes features (lags, moving averages, gradients).
- **Forecaster**: Generates the 24-hour hourly forecast using statistical/ML model or ruleset.
- **AIReviewer**: Reviews forecaster output, detects anomalies, adjusts confidences, and writes reviewer notes.
- **Publisher**: Packages forecast, audit trail, and summary; exposes REST endpoint or file output.

## Constraints and Limitations

1. **API Rate Limits**: Respect API quotas; implement caching and backoff.
2. **Data Gaps**: If historical data has gaps > 3 consecutive hours, mark those hours and degrade confidence.
3. **Forecast Window**: Only next 24 hours; long-term forecasts out of scope.
4. **Geographic Scope**: Single-location forecasts per run (support multiple locations via replication).
5. **Privacy & Licensing**: Comply with weather API terms; do not expose API keys.

## Success Criteria

- **Accuracy**: Mean absolute error (MAE) for temperature < 2.5°C over test periods.
- **Timeliness**: Forecast generated within 5s after data available.
- **Reviewer Coverage**: AIReviewer provides notes for ≥95% of hours when confidence < 0.9.
- **Reliability**: System handles 99% of scheduled runs without manual intervention.

## Example Run Notes

- `location`: (lat, lon) provided in config
- System fetches 168h of history, preprocesses, runs forecast, runs reviewer, publishes JSON

## Next Steps for Implementation

1. Generate an `ARCH_SPEC` describing data flows between the agents and tools.
2. Generate a `TECH_SPEC` with concrete class/method signatures for each agent and tool.
3. Implement `DataCollector` tool to call the configured weather API and store results in `src/data/`.
4. Implement `Forecaster` with a baseline statistical model and add tests.

---


