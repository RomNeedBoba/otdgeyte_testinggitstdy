import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Configures a production-grade rotating logger.
    Files larger than 10MB will be archived, keeping the server disk from filling up.
    """
    # Ensure log directory exists
    log_dir = "storage/logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "app.log")

    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) # Set to DEBUG if you need more info during testing

    # Create handlers
    c_handler = logging.StreamHandler() # Outputs to terminal
    
    # SECURITY: Rotating file handler prevents Denial of Service via log-flooding
    # Keeps max 5 files of 10MB each.
    f_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5) 
    
    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger