import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("replication-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Data Replication Strategies API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/replications")
def get_replications():
    return [
        {"id": "rep-fin-001", "name": "SQL to Snowflake CDC", "source": "Azure SQL", "target": "Snowflake", "status": "SYNCING", "lag": "1.2s"},
        {"id": "rep-sales-042", "name": "Oracle to Databricks", "source": "On-Prem Oracle", "target": "Databricks", "status": "STALLED", "lag": "2.4h"},
        {"id": "rep-hr-101", "name": "S3 to ADLS Mirror", "source": "AWS S3", "target": "Azure Data Lake", "status": "COMPLETED", "lag": "0s"}
    ]

@app.get("/lag/summary")
def get_lag_summary():
    return {
        "avg_latency": "1.4s",
        "p99_latency": "12.5s",
        "stalled_jobs": 1,
        "throughput_gbps": 2.4
    }

@app.get("/dr/readiness")
def get_dr_readiness():
    return {
        "overall_readiness": "98.4%",
        "rpo_compliance": "Optimal",
        "last_failover_test": "2026-04-20",
        "regional_health": "GREEN"
    }

@app.get("/costs/summary")
def get_costs_summary():
    return {
        "monthly_egress_est": "$12.5K",
        "compression_ratio": "4.2:1",
        "savings_impact": "$4.1K",
        "top_spender": "Cross-Cloud Analytics Hub"
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_replication_links": 42,
        "active_data_volume": "142 TB",
        "global_uptime": "99.998%",
        "security_incidents": 0
    }

@app.post("/replications/create")
def create_replication(source: str, target: str, pattern: str):
    logger.info(f"Provisioning new replication link: {source} -> {target} using {pattern}")
    return {"status": "Provisioning Job Enqueued", "job_id": "job_rep_456"}
