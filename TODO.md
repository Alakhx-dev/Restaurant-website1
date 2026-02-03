# Admin Authentication Improvement Tasks

## 1. Update /admin-login route in app.py
- [ ] Check if data/admin.json exists; if not, redirect to /admin-register
- [ ] If exists, load credentials and validate against form input
- [ ] Remove fixed credentials logic

## 2. Add new /admin-register route in app.py
- [ ] Handle GET: render admin_register.html
- [ ] Handle POST: save username/password to data/admin.json (only if not exists)

## 3. Create templates/admin_register.html
- [ ] Form with username and password fields
- [ ] Submit to /admin-register POST

## 4. Test the flow
- [ ] First access to /admin-login redirects to /admin-register
- [ ] Set credentials, then login works
- [ ] Existing admin features remain functional
