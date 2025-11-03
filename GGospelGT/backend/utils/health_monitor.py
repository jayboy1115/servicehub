"""
Production Health Monitoring System
Provides comprehensive health checks for all system components.
"""

import asyncio
import time
import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from fastapi import HTTPException
from ..database import database
from utils.logger import get_logger

logger = get_logger('health_monitor')

class HealthMonitor:
    """Comprehensive health monitoring for production systems."""
    
    def __init__(self):
        self.start_time = time.time()
        self.last_health_check = None
        self.health_history = []
        self.max_history_size = 100
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health status."""
        try:
            health_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "healthy",
                "uptime": self._get_uptime(),
                "system": await self._get_system_metrics(),
                "database": await self.get_database_health(),
                "services": await self._get_service_health(),
                "environment": self._get_environment_info(),
                "performance": await self._get_performance_metrics()
            }
            
            # Determine overall health status
            health_data["status"] = self._determine_overall_status(health_data)
            
            # Store in history
            self._store_health_history(health_data)
            
            logger.info("Health check completed", extra={
                "status": health_data["status"],
                "uptime": health_data["uptime"],
                "memory_usage": health_data["system"]["memory"]["usage_percent"]
            })
            
            return health_data
            
        except Exception as e:
            logger.error("Health check failed", extra={"error": str(e)})
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def get_database_health(self) -> Dict[str, Any]:
        """Get detailed database health information."""
        try:
            db = database.database
            start_time = time.time()
            
            # Test database connection
            await db.command("ping")
            connection_time = (time.time() - start_time) * 1000
            
            # Get database stats
            stats = await db.command("dbStats")
            
            # Count documents in main collections
            collections_info = {}
            main_collections = ["users", "jobs", "interests", "reviews", "messages", "notifications"]
            
            for collection in main_collections:
                try:
                    count = await db[collection].count_documents({})
                    collections_info[collection] = count
                except Exception as e:
                    collections_info[collection] = f"Error: {str(e)}"
            
            # Get recent activity (last 24 hours)
            yesterday = datetime.utcnow() - timedelta(days=1)
            recent_activity = {}
            
            try:
                recent_users = await db.users.count_documents({
                    "created_at": {"$gte": yesterday}
                })
                recent_jobs = await db.jobs.count_documents({
                    "created_at": {"$gte": yesterday}
                })
                recent_activity = {
                    "new_users_24h": recent_users,
                    "new_jobs_24h": recent_jobs
                }
            except Exception as e:
                recent_activity["error"] = str(e)
            
            return {
                "status": "healthy",
                "connection_time_ms": round(connection_time, 2),
                "database_size_mb": round(stats.get("dataSize", 0) / (1024 * 1024), 2),
                "collections": collections_info,
                "recent_activity": recent_activity,
                "indexes": stats.get("indexes", 0),
                "storage_size_mb": round(stats.get("storageSize", 0) / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error("Database health check failed", extra={"error": str(e)})
            return {
                "status": "unhealthy",
                "error": str(e),
                "connection_time_ms": None
            }
    
    def _get_uptime(self) -> Dict[str, Any]:
        """Get application uptime information."""
        uptime_seconds = time.time() - self.start_time
        uptime_hours = uptime_seconds / 3600
        uptime_days = uptime_hours / 24
        
        return {
            "seconds": round(uptime_seconds, 2),
            "hours": round(uptime_hours, 2),
            "days": round(uptime_days, 2),
            "human_readable": self._format_uptime(uptime_seconds)
        }
    
    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            
            # Network metrics (if available)
            try:
                network = psutil.net_io_counters()
                network_info = {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv
                }
            except:
                network_info = {"error": "Network metrics unavailable"}
            
            return {
                "cpu": {
                    "usage_percent": cpu_percent,
                    "count": cpu_count,
                    "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "used_gb": round(memory.used / (1024**3), 2),
                    "usage_percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "used_gb": round(disk.used / (1024**3), 2),
                    "usage_percent": round((disk.used / disk.total) * 100, 2)
                },
                "network": network_info
            }
            
        except Exception as e:
            logger.error("System metrics collection failed", extra={"error": str(e)})
            return {"error": str(e)}
    
    async def _get_service_health(self) -> Dict[str, Any]:
        """Check health of various services."""
        services = {}
        
        # Check database connection
        try:
            await database.database.command("ping")
            services["database"] = {"status": "healthy", "response_time_ms": "< 100"}
        except Exception as e:
            services["database"] = {"status": "unhealthy", "error": str(e)}
        
        # Check environment variables
        # Normalize DB URL env names across the app: backend connects using MONGO_URL or MONGODB_URL
        required_env_vars = [
            "SECRET_KEY",
        ]
        # Consider DB URL as set if either variable exists
        has_db_url = os.getenv("MONGO_URL") or os.getenv("MONGODB_URL")
        env_status = {
            "MONGO_URL_or_MONGODB_URL": "set" if has_db_url else "missing",
        }
        
        for var in required_env_vars:
            env_status[var] = "set" if os.getenv(var) else "missing"
        
        services["environment"] = {
            "status": "healthy" if (has_db_url and all(os.getenv(var) for var in required_env_vars)) else "degraded",
            "variables": env_status
        }
        
        return services
    
    def _get_environment_info(self) -> Dict[str, Any]:
        """Get environment and configuration information."""
        return {
            "python_version": os.sys.version.split()[0],
            "environment": os.getenv("ENVIRONMENT", "development"),
            "debug_mode": os.getenv("DEBUG", "false").lower() == "true",
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "timezone": str(datetime.now().astimezone().tzinfo)
        }
    
    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance-related metrics."""
        try:
            # Database query performance test
            start_time = time.time()
            await database.database.users.find_one({})
            db_query_time = (time.time() - start_time) * 1000
            
            return {
                "database_query_time_ms": round(db_query_time, 2),
                "health_check_count": len(self.health_history),
                "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _determine_overall_status(self, health_data: Dict[str, Any]) -> str:
        """Determine overall system health status."""
        try:
            # Check critical thresholds
            system = health_data.get("system", {})
            
            # Memory usage > 90% is critical
            memory_usage = system.get("memory", {}).get("usage_percent", 0)
            if memory_usage > 90:
                return "critical"
            
            # CPU usage > 95% is critical
            cpu_usage = system.get("cpu", {}).get("usage_percent", 0)
            if cpu_usage > 95:
                return "critical"
            
            # Disk usage > 95% is critical
            disk_usage = system.get("disk", {}).get("usage_percent", 0)
            if disk_usage > 95:
                return "critical"
            
            # Database issues are critical
            db_status = health_data.get("database", {}).get("status")
            if db_status == "unhealthy":
                return "critical"
            
            # Warning thresholds
            if memory_usage > 80 or cpu_usage > 80 or disk_usage > 85:
                return "warning"
            
            return "healthy"
            
        except Exception:
            return "unknown"
    
    def _store_health_history(self, health_data: Dict[str, Any]) -> None:
        """Store health check in history."""
        self.last_health_check = datetime.utcnow()
        
        # Store simplified version in history
        history_entry = {
            "timestamp": health_data["timestamp"],
            "status": health_data["status"],
            "memory_usage": health_data.get("system", {}).get("memory", {}).get("usage_percent"),
            "cpu_usage": health_data.get("system", {}).get("cpu", {}).get("usage_percent"),
            "db_status": health_data.get("database", {}).get("status")
        }
        
        self.health_history.append(history_entry)
        
        # Keep only recent history
        if len(self.health_history) > self.max_history_size:
            self.health_history = self.health_history[-self.max_history_size:]
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime in human-readable format."""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def get_health_history(self) -> List[Dict[str, Any]]:
        """Get recent health check history."""
        return self.health_history[-20:]  # Return last 20 checks

# Global health monitor instance
health_monitor = HealthMonitor()