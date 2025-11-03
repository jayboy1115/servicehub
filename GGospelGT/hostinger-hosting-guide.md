# 🌟 ServiceHub Hostinger Hosting Guide

## 📊 Hostinger Plan Recommendations

### Option 1: VPS Hosting (Recommended)
- **Plan**: VPS 1 or VPS 2
- **Price**: $4.99-$8.99/month
- **Specs**: 1-4 GB RAM, 20-80 GB SSD, Full root access
- **Best for**: Full control, custom software installation

### Option 2: Cloud Hosting
- **Plan**: Cloud Startup or Cloud Professional
- **Price**: $9.99-$14.99/month
- **Specs**: Managed infrastructure, automatic scaling
- **Best for**: Less technical setup, managed services

### Why Not Shared Hosting?
❌ Shared hosting only supports PHP/HTML
❌ No Python/Node.js support
❌ No custom database installation
❌ Limited server control

## 🎯 Recommended Choice: VPS 2
- **RAM**: 4 GB
- **Storage**: 80 GB SSD
- **Bandwidth**: Unlimited
- **Price**: ~$8.99/month
- **Perfect for**: ServiceHub full-stack application

---

## 🛒 Step 1: Purchase Hostinger VPS

1. Visit: https://www.hostinger.com/vps-hosting
2. Select **VPS 2** plan
3. Choose **Ubuntu 22.04** as operating system
4. Complete purchase and account setup
5. Wait for VPS provisioning (5-10 minutes)

---

## 🔐 Step 2: Access Your VPS

### Via SSH (Recommended)
```bash
ssh root@your-vps-ip-address
# Use password provided in Hostinger email
```

### Via Hostinger hPanel
1. Login to hPanel
2. Go to VPS section
3. Click "Manage" on your VPS
4. Use browser terminal

---

## ⚙️ Step 3: Server Setup

### Update System
```bash
apt update && apt upgrade -y
```

### Install Required Software
```bash
# Install Node.js (for React)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install -y nodejs

# Install Python & pip
apt install -y python3 python3-pip python3-venv

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
apt update
apt install -y mongodb-org

# Install Nginx (web server)
apt install -y nginx

# Install PM2 (process manager)
npm install -g pm2
```

### Start Services
```bash
systemctl start mongod
systemctl enable mongod
systemctl start nginx
systemctl enable nginx
```

---

## 📁 Step 4: Upload Your Code

### Option A: Git Clone (Recommended)
```bash
cd /var/www
git clone https://github.com/yourusername/servicehub.git
cd servicehub
```

### Option B: File Upload
1. Use FileZilla or SCP to upload your `/app` folder
2. Place in `/var/www/servicehub/`

---

## 🔧 Step 5: Backend Setup

```bash
cd /var/www/servicehub/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
nano .env
```

### Backend .env Configuration:
```env
MONGO_URL=mongodb://localhost:27017/servicehub
FRONTEND_URL=https://yourdomain.com
TERMII_API_KEY=your-termii-key
SENDGRID_API_KEY=your-sendgrid-key
SENDER_EMAIL=no-reply@yourdomain.com
DB_NAME=servicehub
CORS_ORIGINS=https://yourdomain.com
PORT=8001
```

### Start Backend with PM2
```bash
pm2 start server.py --name "servicehub-backend" --interpreter python3
pm2 save
pm2 startup
```

---

## 🎨 Step 6: Frontend Setup

```bash
cd /var/www/servicehub/frontend

# Install dependencies
npm install

# Update environment variables
nano .env
```

### Frontend .env Configuration:
```env
REACT_APP_BACKEND_URL=https://yourdomain.com/api
REACT_APP_GOOGLE_MAPS_API_KEY=your-google-maps-key
```

### Build Frontend
```bash
npm run build
```

---

## 🌐 Step 7: Nginx Configuration

```bash
nano /etc/nginx/sites-available/servicehub
```

### Nginx Config File:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend (React build)
    location / {
        root /var/www/servicehub/frontend/build;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Enable Site
```bash
ln -s /etc/nginx/sites-available/servicehub /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

---

## 🔒 Step 8: Domain & SSL Setup

### A. Point Domain to VPS
1. In your domain registrar (e.g., Namecheap, GoDaddy):
   - A Record: @ → Your VPS IP
   - A Record: www → Your VPS IP

### B. Install SSL Certificate (Free)
```bash
# Install Certbot
apt install certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 📊 Step 9: Database Setup

```bash
# Connect to MongoDB
mongosh

# Create database and sample data
use servicehub

# Run your seeding script
cd /var/www/servicehub/backend
python3 quick_seed.py
```

---

## 🔍 Step 10: Testing & Monitoring

### Test Your Site
```bash
# Check backend
curl https://yourdomain.com/api/health

# Check frontend
curl https://yourdomain.com

# Check PM2 processes
pm2 status
```

### Monitoring Commands
```bash
# View backend logs
pm2 logs servicehub-backend

# Restart backend
pm2 restart servicehub-backend

# Check Nginx status
systemctl status nginx

# Check MongoDB status
systemctl status mongod
```

---

## 💰 Cost Breakdown

| Service | Monthly Cost |
|---------|-------------|
| Hostinger VPS 2 | $8.99 |
| Domain (optional) | $1/month |
| **Total** | **~$10/month** |

---

## 🆘 Troubleshooting

### Common Issues:

1. **Site not loading**: Check Nginx config and PM2 status
2. **API errors**: Check backend logs with `pm2 logs`
3. **Database issues**: Check MongoDB status
4. **SSL problems**: Rerun certbot command

### Support Resources:
- Hostinger Knowledge Base
- Hostinger 24/7 Chat Support
- Community forums

---

## 🎉 Success Checklist

- [ ] VPS purchased and set up
- [ ] Server software installed
- [ ] Code uploaded and configured
- [ ] Backend running via PM2
- [ ] Frontend built and served
- [ ] Nginx configured correctly
- [ ] Domain pointed to VPS
- [ ] SSL certificate installed
- [ ] Database populated with data
- [ ] Site accessible at your domain

Your ServiceHub website will be live at: **https://yourdomain.com**