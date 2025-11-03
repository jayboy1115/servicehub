"""
Production-ready logging configuration for ServiceHub backend.
Provides structured logging with file rotation, different log levels, and proper formatting.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional
import json


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'endpoint'):
            log_entry['endpoint'] = record.endpoint
        if hasattr(record, 'method'):
            log_entry['method'] = record.method
        if hasattr(record, 'status_code'):
            log_entry['status_code'] = record.status_code
        if hasattr(record, 'duration'):
            log_entry['duration_ms'] = record.duration
            
        return json.dumps(log_entry)


class ServiceHubLogger:
    """Centralized logging configuration for ServiceHub."""
    
    def __init__(self):
        self.logger = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with appropriate handlers and formatters."""
        
        # Get configuration from environment
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        log_file_path = os.getenv('LOG_FILE_PATH', 'logs/servicehub.log')
        log_max_size = os.getenv('LOG_MAX_SIZE', '10MB')
        log_backup_count = int(os.getenv('LOG_BACKUP_COUNT', '5'))
        environment = os.getenv('ENVIRONMENT', 'development')
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create logger
        self.logger = logging.getLogger('servicehub')
        self.logger.setLevel(getattr(logging, log_level))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colored output for development
        console_handler = logging.StreamHandler(sys.stdout)
        if environment == 'development':
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            console_formatter = JSONFormatter()
        
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation for production
        if environment in ['staging', 'production']:
            # Convert size string to bytes
            max_bytes = self._parse_size(log_max_size)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file_path,
                maxBytes=max_bytes,
                backupCount=log_backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(JSONFormatter())
            self.logger.addHandler(file_handler)
        
        # Error file handler for critical errors
        if environment in ['staging', 'production']:
            error_file_path = log_file_path.replace('.log', '_errors.log')
            error_handler = logging.handlers.RotatingFileHandler(
                error_file_path,
                maxBytes=max_bytes,
                backupCount=log_backup_count,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(JSONFormatter())
            self.logger.addHandler(error_handler)
    
    def _parse_size(self, size_str: str) -> int:
        """Parse size string like '10MB' to bytes."""
        size_str = size_str.upper()
        if size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return int(size_str)
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get a logger instance."""
        if name:
            return logging.getLogger(f'servicehub.{name}')
        return self.logger
    
    def log_request(self, method: str, endpoint: str, status_code: int, 
                   duration: float, user_id: Optional[str] = None,
                   request_id: Optional[str] = None):
        """Log HTTP request with structured data."""
        logger = self.get_logger('requests')
        logger.info(
            f"{method} {endpoint} - {status_code} - {duration:.2f}ms",
            extra={
                'method': method,
                'endpoint': endpoint,
                'status_code': status_code,
                'duration': duration,
                'user_id': user_id,
                'request_id': request_id
            }
        )
    
    def log_database_operation(self, operation: str, collection: str, 
                              duration: float, success: bool = True,
                              error: Optional[str] = None):
        """Log database operations."""
        logger = self.get_logger('database')
        if success:
            logger.info(
                f"DB {operation} on {collection} - {duration:.2f}ms",
                extra={
                    'operation': operation,
                    'collection': collection,
                    'duration': duration,
                    'success': success
                }
            )
        else:
            logger.error(
                f"DB {operation} on {collection} failed - {error}",
                extra={
                    'operation': operation,
                    'collection': collection,
                    'duration': duration,
                    'success': success,
                    'error': error
                }
            )
    
    def log_authentication(self, event: str, user_id: Optional[str] = None,
                          email: Optional[str] = None, success: bool = True,
                          error: Optional[str] = None):
        """Log authentication events."""
        logger = self.get_logger('auth')
        message = f"Auth {event}"
        if user_id:
            message += f" for user {user_id}"
        elif email:
            message += f" for email {email}"
        
        extra = {
            'event': event,
            'user_id': user_id,
            'email': email,
            'success': success
        }
        
        if success:
            logger.info(message, extra=extra)
        else:
            extra['error'] = error
            logger.warning(f"{message} failed - {error}", extra=extra)
    
    def log_security_event(self, event: str, severity: str = 'medium',
                          user_id: Optional[str] = None,
                          ip_address: Optional[str] = None,
                          details: Optional[dict] = None):
        """Log security-related events."""
        logger = self.get_logger('security')
        message = f"Security event: {event}"
        
        extra = {
            'event': event,
            'severity': severity,
            'user_id': user_id,
            'ip_address': ip_address,
            'details': details or {}
        }
        
        if severity == 'high':
            logger.error(message, extra=extra)
        elif severity == 'medium':
            logger.warning(message, extra=extra)
        else:
            logger.info(message, extra=extra)


# Global logger instance
_logger_instance = None

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get the global logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ServiceHubLogger()
    return _logger_instance.get_logger(name)

def log_request(*args, **kwargs):
    """Convenience function for request logging."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ServiceHubLogger()
    return _logger_instance.log_request(*args, **kwargs)

def log_database_operation(*args, **kwargs):
    """Convenience function for database operation logging."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ServiceHubLogger()
    return _logger_instance.log_database_operation(*args, **kwargs)

def log_authentication(*args, **kwargs):
    """Convenience function for authentication logging."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ServiceHubLogger()
    return _logger_instance.log_authentication(*args, **kwargs)

def log_security_event(*args, **kwargs):
    """Convenience function for security event logging."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ServiceHubLogger()
    return _logger_instance.log_security_event(*args, **kwargs)