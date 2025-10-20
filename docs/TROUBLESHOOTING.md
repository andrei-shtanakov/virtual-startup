# Virtual Startup - Troubleshooting Guide

**Version**: 1.0.0
**Last Updated**: October 18, 2025

This guide helps you diagnose and resolve common issues with the Virtual Startup multi-agent AI system.

---

## Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Backend Issues](#backend-issues)
3. [Frontend Issues](#frontend-issues)
4. [WebSocket Issues](#websocket-issues)
5. [Database Issues](#database-issues)
6. [Agent System Issues](#agent-system-issues)
7. [Performance Issues](#performance-issues)
8. [Deployment Issues](#deployment-issues)
9. [Common Error Messages](#common-error-messages)
10. [Getting Help](#getting-help)

---

## Quick Diagnostics

### System Health Check

Run these commands to quickly check system status:

```bash
# 1. Check if backend is running
curl http://localhost:5000/api/health

# 2. Check if frontend is running
curl http://localhost:5173

# 3. Check backend logs
cd backend
tail -n 50 logs/app.log

# 4. Check database connection
cd backend
uv run flask shell
>>> from app import db
>>> db.session.execute('SELECT 1').scalar()
1

# 5. Check WebSocket
# Open browser DevTools > Network > WS tab
# You should see a WebSocket connection to ws://localhost:5000/socket.io/
```

### Quick Fix Checklist

Before diving into specific issues, try these quick fixes:

- [ ] Restart backend: `Ctrl+C` and `uv run python run.py`
- [ ] Restart frontend: `Ctrl+C` and `npm run dev`
- [ ] Clear browser cache and hard reload: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- [ ] Check `.env` files exist in both `backend/` and `frontend/`
- [ ] Verify ports 5000 and 5173 are not in use: `lsof -i :5000` and `lsof -i :5173`
- [ ] Check if all dependencies are installed: `uv sync` (backend) and `npm install` (frontend)

---

## Backend Issues

### Issue: "Agent system not initialized"

**Symptoms:**
- API returns error: "Agent system not initialized"
- Chat functionality doesn't work
- `/api/agents` returns empty list

**Cause:**
Agent system hasn't been initialized after backend start.

**Solution:**

```bash
# Initialize the agent system
curl -X POST http://localhost:5000/api/init

# Or restart backend (auto-initialization may be enabled)
cd backend
uv run python run.py
```

**Prevention:**
The system should auto-initialize on startup. If not, check logs for initialization errors.

---

### Issue: Backend won't start

**Symptoms:**
- Backend crashes immediately after `uv run python run.py`
- Error: "Address already in use"
- Error: "ModuleNotFoundError"

**Solutions:**

**Problem: Port 5000 in use**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process (replace PID)
kill -9 <PID>

# Or use a different port
FLASK_RUN_PORT=5001 uv run flask run
```

**Problem: Missing dependencies**
```bash
cd backend

# Reinstall dependencies
uv sync

# Or manually install
uv add flask flask-sqlalchemy flask-migrate flask-cors flask-socketio
```

**Problem: Database not initialized**
```bash
cd backend

# Initialize database
uv run flask db init
uv run flask db migrate -m "Initial migration"
uv run flask db upgrade
```

---

### Issue: "Database locked" error (SQLite)

**Symptoms:**
- Error: `sqlite3.OperationalError: database is locked`
- Operations fail intermittently

**Cause:**
SQLite doesn't handle concurrent writes well.

**Solution:**

**Short-term:**
```bash
# Close all connections to the database
# Restart backend
cd backend
uv run python run.py
```

**Long-term (Production):**
```bash
# Switch to PostgreSQL
# See DEPLOYMENT_GUIDE.md for PostgreSQL setup
```

---

### Issue: OpenAI API errors

**Symptoms:**
- Error: "Invalid API key"
- Error: "Rate limit exceeded"
- Agents don't respond

**Solutions:**

**Invalid API Key:**
```bash
# Check .env file
cd backend
cat .env | grep OPENAI_API_KEY

# Update API key
nano .env
# Add: OPENAI_API_KEY=sk-...

# Restart backend
uv run python run.py
```

**Rate Limit Exceeded:**
```bash
# Wait a few minutes
# Or upgrade your OpenAI plan
# Or reduce concurrent requests by limiting agents
```

**API Connection Issues:**
```bash
# Test API connectivity
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Check firewall/proxy settings
```

---

### Issue: CORS errors

**Symptoms:**
- Browser console: "CORS policy blocked"
- Frontend can't reach backend API
- Network requests fail with CORS error

**Solution:**

```bash
# Check backend .env
cd backend
cat .env | grep CORS_ORIGINS

# Should be:
CORS_ORIGINS=http://localhost:5173

# If wrong, update and restart backend
nano .env
uv run python run.py
```

**Multiple Origins (Production):**
```env
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

---

## Frontend Issues

### Issue: Frontend won't start

**Symptoms:**
- Error: "EADDRINUSE: address already in use"
- Error: "Cannot find module"
- Vite fails to start

**Solutions:**

**Port in use:**
```bash
# Find process using port 5173
lsof -i :5173

# Kill it
kill -9 <PID>

# Or use different port
npm run dev -- --port 5174
```

**Missing dependencies:**
```bash
cd frontend

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

**Build errors:**
```bash
cd frontend

# Check TypeScript errors
npm run typecheck

# Fix linting issues
npm run lint:fix
```

---

### Issue: "API connection failed"

**Symptoms:**
- Dashboard shows "Failed to fetch"
- Chat doesn't work
- Console error: "Network request failed"

**Solutions:**

**Check backend is running:**
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "ok"}
```

**Check API URL configuration:**
```bash
cd frontend
cat .env | grep VITE_API_URL

# Should be:
VITE_API_URL=http://localhost:5000/api

# If wrong, update and restart frontend
nano .env
npm run dev
```

**Check CORS (see Backend Issues > CORS errors)**

---

### Issue: Page blank or loading forever

**Symptoms:**
- White screen after loading
- React errors in console
- Page stuck on loading spinner

**Solutions:**

**Check browser console for errors:**
```
Press F12 > Console tab
Look for red error messages
```

**Common fixes:**

1. **Clear cache and reload:**
   - Chrome/Firefox: `Ctrl+Shift+R`
   - Safari: `Cmd+Option+R`

2. **Check if backend is initialized:**
   ```bash
   curl -X POST http://localhost:5000/api/init
   ```

3. **Rebuild frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Check for JavaScript errors:**
   - Look in Console tab
   - Common issue: Missing environment variables

---

### Issue: TypeScript errors

**Symptoms:**
- Red underlines in VS Code
- `npm run typecheck` fails
- Build fails with type errors

**Solutions:**

```bash
cd frontend

# Run type checking
npm run typecheck

# Common fixes:
# 1. Install missing types
npm install --save-dev @types/node @types/react @types/react-dom

# 2. Update tsconfig.json if needed
# 3. Add type annotations or // @ts-ignore for complex cases
```

---

## WebSocket Issues

### Issue: WebSocket not connecting

**Symptoms:**
- Chat messages don't send/receive
- DevTools Network > WS shows no connection
- Console: "WebSocket connection failed"

**Cause:**
- Backend not running with `run.py` (using `flask run` instead)
- WebSocket server not initialized
- CORS blocking WebSocket

**Solution:**

**Always use `run.py`:**
```bash
cd backend

# CORRECT way to start backend
uv run python run.py

# WRONG way (WebSocket won't work)
# uv run flask run
```

**Check WebSocket in DevTools:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Filter by "WS" (WebSocket)
4. Look for `ws://localhost:5000/socket.io/`
5. Should show status: "101 Switching Protocols"

**Check backend logs:**
```bash
# Look for WebSocket-related logs
tail -f backend/logs/app.log | grep socket
```

---

### Issue: WebSocket disconnects frequently

**Symptoms:**
- Connection drops every few seconds
- Chat messages sometimes don't send
- Console shows repeated connection attempts

**Solutions:**

**Increase timeout:**
```python
# In backend/run.py or backend/app/__init__.py
socketio = SocketIO(
    app,
    cors_allowed_origins="http://localhost:5173",
    ping_timeout=60,  # Increase from default 5
    ping_interval=25  # Increase from default 25
)
```

**Check network stability:**
```bash
# Ping backend
ping localhost

# Check for firewall/antivirus blocking
```

**Browser issues:**
```
# Try different browser
# Clear cookies and cache
# Disable browser extensions
```

---

### Issue: Messages not appearing in real-time

**Symptoms:**
- Send message, but no response
- Have to refresh page to see messages
- WebSocket connected but not receiving events

**Solutions:**

**Check event handlers:**
```javascript
// In frontend, check if event listeners are set up
// Look in ChatDemo.tsx or CLI.tsx for:
socket.on('agent_response', handleResponse);
socket.on('status_update', handleStatus);
```

**Backend event emission:**
```python
# Verify backend is emitting events
# In backend, look for:
socketio.emit('agent_response', data)
```

**Test WebSocket manually:**
```javascript
// In browser console
const socket = io('http://localhost:5000');
socket.on('connect', () => console.log('Connected'));
socket.on('agent_response', (data) => console.log('Response:', data));
socket.emit('send_message', {agent: 'driver', message: 'test'});
```

---

## Database Issues

### Issue: Migration errors

**Symptoms:**
- Error: "Can't locate revision"
- Error: "Target database is not up to date"
- Database schema mismatch

**Solutions:**

**Check current revision:**
```bash
cd backend
uv run flask db current

# Should show a revision hash
# If empty, database not initialized
```

**Reset migrations (Development only!):**
```bash
cd backend

# DANGER: This deletes all data!
rm -rf migrations/
rm app.db

# Reinitialize
uv run flask db init
uv run flask db migrate -m "Initial migration"
uv run flask db upgrade
```

**Upgrade to latest:**
```bash
cd backend
uv run flask db upgrade
```

**Downgrade one step:**
```bash
cd backend
uv run flask db downgrade
```

---

### Issue: Database corruption

**Symptoms:**
- Error: "database disk image is malformed"
- Random SQLite errors
- Data loss or inconsistencies

**Solutions:**

**Export and rebuild (SQLite):**
```bash
cd backend

# Export data
sqlite3 app.db .dump > backup.sql

# Remove corrupted database
rm app.db

# Recreate and import
uv run flask db upgrade
sqlite3 app.db < backup.sql
```

**Prevention:**
- Switch to PostgreSQL for production
- Regular backups (see DEPLOYMENT_GUIDE.md)

---

## Agent System Issues

### Issue: Agents not responding

**Symptoms:**
- Send message to agent, no response
- Agent status stuck on "working"
- Timeout errors

**Causes & Solutions:**

**1. Agent system not initialized:**
```bash
curl -X POST http://localhost:5000/api/init
```

**2. OpenAI API issue:**
```bash
# Check API key
cd backend
cat .env | grep OPENAI_API_KEY

# Test API
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**3. Agent crashed:**
```bash
# Check backend logs
cd backend
tail -f logs/app.log | grep ERROR

# Restart backend
uv run python run.py
```

**4. Rate limiting:**
```
# Wait a few minutes
# Check OpenAI dashboard for usage
```

---

### Issue: "Failed to create agent"

**Symptoms:**
- Generator can't create new agents
- Error in logs about agent creation
- Dynamic agents not appearing

**Solutions:**

**Check AutoGen configuration:**
```bash
cd backend
cat .env | grep -E "OPENAI_API_KEY|DEFAULT_LLM_MODEL"

# Should have:
OPENAI_API_KEY=sk-...
DEFAULT_LLM_MODEL=gpt-4
```

**Check agent limits:**
```python
# In backend config
MAX_DYNAMIC_AGENTS=10  # Default limit

# Check current count
curl http://localhost:5000/api/agents | grep -c '"type":"dynamic"'
```

**Check logs for specific error:**
```bash
cd backend
tail -f logs/app.log | grep "create_agent"
```

---

### Issue: RAG service not finding documents

**Symptoms:**
- Creator agent says "I don't have information about..."
- RAG searches return no results
- Knowledge base seems empty

**Solutions:**

**Check ChromaDB:**
```bash
cd backend

# Verify ChromaDB directory exists
ls -la chroma_db/

# Should contain collection data
```

**Reinitialize knowledge base:**
```bash
cd backend

# Check if sample documents exist
ls -la app/data/sample_docs/

# Reinitialize ChromaDB (deletes existing)
rm -rf chroma_db/
uv run python -c "from app.services import get_rag_service; get_rag_service()"
```

**Check RAG service logs:**
```bash
cd backend
tail -f logs/app.log | grep RAG
```

---

## Performance Issues

### Issue: Slow response times

**Symptoms:**
- Agent responses take >30 seconds
- API requests timeout
- UI feels sluggish

**Causes & Solutions:**

**1. OpenAI API latency:**
```bash
# Use faster model
# In .env, change:
DEFAULT_LLM_MODEL=gpt-3.5-turbo  # Faster than gpt-4
```

**2. Database queries slow:**
```bash
# Check SQLite performance
cd backend
sqlite3 app.db

# Analyze query performance
.timer ON
SELECT * FROM agents;

# Consider PostgreSQL for production
```

**3. Too many concurrent agents:**
```bash
# Check active agents
curl http://localhost:5000/api/agents

# Terminate idle dynamic agents
curl -X DELETE http://localhost:5000/api/agents/<id>
```

**4. Frontend bundle size:**
```bash
cd frontend

# Analyze bundle
npm run build
npx vite-bundle-visualizer

# Optimize imports
# Use code splitting
```

---

### Issue: High memory usage

**Symptoms:**
- Backend using >2GB RAM
- System becomes unresponsive
- Out of memory errors

**Solutions:**

**Check memory usage:**
```bash
# Check backend process
ps aux | grep python

# Check system memory
free -h
```

**Reduce ChromaDB memory:**
```python
# In backend RAG service
# Limit collection size
# Implement document rotation
```

**Limit concurrent agents:**
```env
# In backend .env
MAX_DYNAMIC_AGENTS=5  # Reduce from 10
```

**Restart backend periodically:**
```bash
# Add to crontab (restart daily at 3 AM)
0 3 * * * systemctl restart virtualstartup-backend
```

---

## Deployment Issues

### Issue: Backend not starting after deployment

**Symptoms:**
- Supervisor shows "FATAL"
- Backend crashes immediately
- "Module not found" errors

**Solutions:**

**Check supervisor logs:**
```bash
sudo supervisorctl tail virtualstartup-backend stderr
```

**Common fixes:**

1. **Wrong Python version:**
```bash
python3 --version  # Should be 3.12+
```

2. **Missing dependencies:**
```bash
cd /var/www/virtual-startup/backend
uv sync
```

3. **Environment variables not set:**
```bash
# Check supervisor config has environment variables
sudo nano /etc/supervisor/conf.d/virtualstartup-backend.conf

# Should have:
environment=FLASK_ENV="production"
```

4. **Database not initialized:**
```bash
cd /var/www/virtual-startup/backend
uv run flask db upgrade
```

---

### Issue: 502 Bad Gateway (NGINX)

**Symptoms:**
- NGINX shows 502 error
- Backend seems down
- Can't reach API

**Solutions:**

**Check backend is running:**
```bash
sudo supervisorctl status virtualstartup-backend
# Should show: RUNNING

# If not running:
sudo supervisorctl start virtualstartup-backend
```

**Check backend port:**
```bash
# Backend should be on 127.0.0.1:5000
netstat -tulpn | grep 5000
```

**Check NGINX configuration:**
```bash
# Test config
sudo nginx -t

# Check upstream
sudo nano /etc/nginx/sites-available/virtualstartup
# Verify: proxy_pass http://127.0.0.1:5000;

# Restart NGINX
sudo systemctl restart nginx
```

**Check logs:**
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/virtualstartup/backend.log
```

---

### Issue: SSL certificate errors

**Symptoms:**
- "Your connection is not private"
- SSL handshake failed
- Mixed content warnings

**Solutions:**

**Renew Let's Encrypt certificate:**
```bash
sudo certbot renew
sudo systemctl reload nginx
```

**Check certificate expiry:**
```bash
sudo certbot certificates
```

**Force HTTPS redirect:**
```nginx
# In NGINX config
server {
    listen 80;
    return 301 https://$server_name$request_uri;
}
```

**Fix mixed content:**
```bash
# Ensure all API calls use HTTPS in production
# Check frontend .env.production:
VITE_API_URL=https://yourdomain.com/api  # Not http://
```

---

## Common Error Messages

### Backend Errors

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `Agent system not initialized` | `/api/init` not called | Run `curl -X POST http://localhost:5000/api/init` |
| `Database is locked` | SQLite concurrency issue | Restart backend, or use PostgreSQL |
| `Invalid API key` | OpenAI key wrong/missing | Check `OPENAI_API_KEY` in `.env` |
| `CORS policy blocked` | CORS not configured | Check `CORS_ORIGINS` in backend `.env` |
| `Address already in use` | Port 5000 occupied | Kill process on port 5000 |
| `No module named 'app'` | Dependencies not installed | Run `uv sync` in backend |
| `Target database not up to date` | Migrations not run | Run `uv run flask db upgrade` |

### Frontend Errors

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `Failed to fetch` | Backend not running | Start backend with `uv run python run.py` |
| `Network request failed` | Wrong API URL | Check `VITE_API_URL` in frontend `.env` |
| `WebSocket connection failed` | Backend not using `run.py` | Use `uv run python run.py` (not `flask run`) |
| `Module not found` | Dependencies missing | Run `npm install` in frontend |
| `Unexpected token '<'` | API returning HTML instead of JSON | Check backend errors, API endpoint |
| `Cannot read property of undefined` | Data structure mismatch | Check API response format |

---

## Getting Help

### Before Asking for Help

1. **Check logs:**
   ```bash
   # Backend
   cd backend && tail -f logs/app.log

   # Frontend browser console
   Press F12 > Console tab
   ```

2. **Reproduce the issue:**
   - Document exact steps to reproduce
   - Note any error messages
   - Check if issue is consistent

3. **Check documentation:**
   - `docs/USER_GUIDE.md` - Usage guide
   - `docs/api.md` - API reference
   - `docs/DEPLOYMENT_GUIDE.md` - Deployment help

### Reporting Issues

Include this information:

- **Environment:**
  - OS and version
  - Python version (`python3 --version`)
  - Node version (`node --version`)
  - Backend/frontend running?

- **Steps to reproduce:**
  1. Step 1
  2. Step 2
  3. Error occurs

- **Error messages:**
  - Backend logs
  - Frontend console errors
  - Screenshots if applicable

- **What you've tried:**
  - Solutions attempted
  - Results

### Useful Commands for Debugging

```bash
# System info
uname -a
python3 --version
node --version

# Backend diagnostics
cd backend
uv run pytest -v  # Run tests
uv run flask routes  # List all routes
uv run flask shell  # Interactive shell

# Frontend diagnostics
cd frontend
npm run typecheck  # Check TypeScript
npm run lint  # Check code style
npm run build  # Test build

# Check logs
tail -f backend/logs/app.log
tail -f /var/log/nginx/error.log  # Production

# Check resources
df -h  # Disk space
free -h  # Memory
htop  # CPU/Memory usage
```

---

## Additional Resources

- **Documentation:** `docs/` folder
- **API Reference:** `docs/api.md`
- **User Guide:** `docs/USER_GUIDE.md`
- **Deployment Guide:** `docs/DEPLOYMENT_GUIDE.md`
- **GitHub Issues:** [Report bugs](https://github.com/your-repo/issues)

---

**Version**: 1.0.0
**Last Updated**: October 18, 2025
**Maintainer**: Virtual Startup Team
**Need more help?** Check the documentation or open a GitHub issue
