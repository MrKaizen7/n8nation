#!/usr/bin/env python3
"""
n8nation Knowledge Base Webhook Trigger
Permite actualizar la base de conocimiento via HTTP requests
Útil para integración con GitHub webhooks, apps React, etc.
"""

from flask import Flask, request, jsonify
import subprocess
import threading
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UpdateManager:
    def __init__(self):
        self.is_updating = False
        self.last_update_status = {"status": "idle", "message": "Ready"}
    
    def run_update(self, source_name=None, force=False):
        """Run update in background thread"""
        if self.is_updating:
            return {"error": "Update already in progress"}
        
        def _update():
            self.is_updating = True
            self.last_update_status = {"status": "running", "message": "Update in progress..."}
            
            try:
                # Build command
                cmd = ["python3", "knowledge_updater.py"]
                if force:
                    cmd.append("--force")
                if source_name:
                    cmd.extend(["--source", source_name])
                
                # Run update
                result = subprocess.run(
                    cmd,
                    cwd=os.path.dirname(__file__),
                    capture_output=True,
                    text=True,
                    timeout=3600  # 1 hour timeout
                )
                
                if result.returncode == 0:
                    self.last_update_status = {
                        "status": "success", 
                        "message": "Update completed successfully",
                        "output": result.stdout
                    }
                else:
                    self.last_update_status = {
                        "status": "error", 
                        "message": f"Update failed: {result.stderr}",
                        "output": result.stdout
                    }
                    
            except subprocess.TimeoutExpired:
                self.last_update_status = {
                    "status": "error", 
                    "message": "Update timed out after 1 hour"
                }
            except Exception as e:
                self.last_update_status = {
                    "status": "error", 
                    "message": f"Update failed: {str(e)}"
                }
            finally:
                self.is_updating = False
        
        # Start background thread
        thread = threading.Thread(target=_update)
        thread.daemon = True
        thread.start()
        
        return {"status": "started", "message": "Update started in background"}

# Global update manager
update_manager = UpdateManager()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "n8nation Knowledge Updater",
        "version": "1.0"
    })

@app.route('/update', methods=['POST'])
def trigger_update():
    """Trigger knowledge base update"""
    
    # Check authentication (simple token-based)
    auth_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    expected_token = os.getenv('UPDATE_TOKEN', 'default-token-change-me')
    
    if auth_token != expected_token:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Get parameters
    data = request.get_json() or {}
    source_name = data.get('source')
    force = data.get('force', False)
    
    # Trigger update
    result = update_manager.run_update(source_name, force)
    
    return jsonify(result)

@app.route('/status', methods=['GET'])
def get_status():
    """Get update status"""
    return jsonify({
        "is_updating": update_manager.is_updating,
        "last_update": update_manager.last_update_status
    })

@app.route('/sources', methods=['GET'])
def list_sources():
    """List available sources"""
    try:
        # Read sources config
        import json
        config_path = os.path.join(os.path.dirname(__file__), 'sources_config.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                sources = json.load(f)
            return jsonify({"sources": sources})
        else:
            return jsonify({"sources": [], "message": "No sources configured yet"})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """Handle GitHub webhooks for automatic updates"""
    
    # Verify GitHub webhook (simplified)
    event = request.headers.get('X-GitHub-Event')
    
    if event == 'push':
        # Repository was updated
        payload = request.get_json()
        
        # Check if it's a relevant repository/branch
        repo_name = payload.get('repository', {}).get('name', '')
        branch = payload.get('ref', '').replace('refs/heads/', '')
        
        if branch == 'main' and 'docs' in repo_name.lower():
            logger.info(f"GitHub push detected on {repo_name}:{branch}")
            
            # Trigger update for file-based sources
            result = update_manager.run_update(source_name="n8nation_workflows", force=True)
            
            return jsonify({
                "message": "Update triggered by GitHub webhook",
                "result": result
            })
    
    return jsonify({"message": "Webhook received but no action taken"})

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting n8nation Knowledge Updater API on {host}:{port}")
    logger.info(f"Update token: {os.getenv('UPDATE_TOKEN', 'default-token-change-me')}")
    
    app.run(host=host, port=port, debug=debug)
