"""
Module for custom JSON log model in Flask and Gunicorn.
"""
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Class for defining JSON log structure of Flask."""

    def add_fields(self, log_data, record, message_dict):
        """Add custom fields to the JSON log record."""
        super().add_fields(log_data, record, message_dict)

        if not log_data.get("timestamp"):
            log_data["timestamp"] = record.created

        if "r" in record.args:
            log_data["request"] = record.args.get("r")
            log_data["message"] = None

        if "s" in record.args:
            log_data["status_code"] = record.args.get("s")

        if "m" in record.args:
            log_data["method"] = record.args.get("m")

        if "h" in record.args:
            log_data["remote_address"] = record.args.get("h")
