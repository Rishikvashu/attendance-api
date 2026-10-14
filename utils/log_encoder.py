"""
Module for custom JSON log model in Flask and Gunicorn.
"""
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Class for defining JSON log structure of Flask."""

    def add_fields(self, log_record, record, message_dict):
        """Add custom fields to the JSON log record."""
        super().add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            log_record["timestamp"] = record.created

        if "r" in record.args:
            log_record["request"] = record.args.get("r")
            log_record["message"] = None

        if "s" in record.args:
            log_record["status_code"] = record.args.get("s")

        if "m" in record.args:
            log_record["method"] = record.args.get("m")

        if "h" in record.args:
            log_record["remote_address"] = record.args.get("h")
