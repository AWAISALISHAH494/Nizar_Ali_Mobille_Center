# Deployment Guide: LUNDKHWAR MOBILE CENTER

This guide will walk you through deploying the LUNDKHWAR MOBILE CENTER e-commerce website on Heroku with AWS S3 for static and media files.

## Prerequisites

1. **Heroku Account**: Sign up at [https://www.heroku.com](https://www.heroku.com)
2. **AWS Account**: Sign up at [https://aws.amazon.com](https://aws.amazon.com)
3. **Heroku CLI**: Install from [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
4. **Git**: Ensure Git is installed on your system
5. **Python 3.11+**: Required for local development

## Part 1: AWS S3 Setup

### Step 1: Create S3 Bucket

1. Log in to AWS Console
2. Go to S3 service
3. Click "Create bucket"
4. Configure bucket:
   - **Bucket name**: `lundkhwar-mobile-center` (must be globally unique)
   - **Region**: Choose closest to Pakistan (e.g., `ap-south-1` for Mumbai)
   - **Block Public Access**: Uncheck "Block all public access" (we need public access for static files)
   - **Bucket Versioning**: Enable (optional but recommended)
   - Click "Create bucket"

### Step 2: Configure Bucket Policy

1. Go to your bucket → Permissions → Bucket Policy
2. Add the following policy (replace `YOUR_BUCKET_NAME` with your actual bucket name):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
        }
    ]
}
```

3. Click "Save changes"

### Step 3: Configure CORS

1. Go to your bucket → Permissions → CORS
2. Add the following CORS configuration:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

3. Click "Save changes"

### Step 4: Create IAM User for S3 Access

1. Go to IAM service in AWS Console
2. Click "Users" → "Add users"
3. User name: `lundkhwar-s3-user`
4. Access type: "Programmatic access"
5. Click "Next: Permissions"
6. Click "Attach existing policies directly"
7. Search and select: `AmazonS3FullAccess` (or create a custom policy with only necessary permissions)
8. Click "Next" → "Next" → "Create user"
9. **IMPORTANT**: Save the Access Key ID and Secret Access Key (you'll need these for Heroku config vars)

### Step 5: Create Folders in S3 Bucket

1. Go to your S3 bucket
2. Create two folders:
   - `static/` (for CSS, JavaScript, images)
   - `media/` (for user uploads, product images)

## Part 2: Heroku Setup

### Step 1: Install Heroku CLI and Login

```bash
# Install Heroku CLI (if not already installed)
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login
```

### Step 2: Create Heroku App

```bash
# Navigate to your project directory
cd "D:\Ecomerce website"

# Create a new Heroku app
heroku create lundkhwar-mobile-center

# Or create with a specific region
heroku create lundkhwar-mobile-center --region us
```

### Step 3: Add PostgreSQL Database

```bash
# Add PostgreSQL addon (free tier: hobby-dev)
heroku addons:create heroku-postgresql:hobby-dev

# Verify database
heroku pg:info
```

### Step 4: Configure Environment Variables

Set all required environment variables on Heroku:

```bash
# Django Secret Key (generate a new one for production)
heroku config:set SECRET_KEY="your-secret-key-here"

# Debug mode (set to False for production)
heroku config:set DEBUG=False

# Allowed hosts (your Heroku app domain)
heroku config:set ALLOWED_HOSTS="lundkhwar-mobile-center.herokuapp.com,www.yourdomain.com"

# AWS S3 Configuration
heroku config:set USE_S3=True
heroku config:set AWS_ACCESS_KEY_ID="your-aws-access-key-id"
heroku config:set AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
heroku config:set AWS_STORAGE_BUCKET_NAME="your-bucket-name"
heroku config:set AWS_S3_REGION_NAME="ap-south-1"

# Database URL (automatically set by Heroku Postgres addon)
# No need to set this manually

# Email Configuration (optional but recommended)
heroku config:set EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
heroku config:set EMAIL_HOST="smtp.gmail.com"
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="your-app-password"
heroku config:set DEFAULT_FROM_EMAIL="noreply@lundkhwarmobilecenter.com"

# Site ID (for Django sites framework)
heroku config:set SITE_ID=1

# Timezone
heroku config:set TZ="Asia/Karachi"

# Security (for HTTPS)
heroku config:set SECURE_SSL_REDIRECT=True
```

### Step 5: Update requirements.txt

Ensure your `requirements.txt` includes all necessary packages. The file should already be set up, but verify it includes:

- `django-heroku` (for Heroku-specific settings)
- `gunicorn` (WSGI server)
- `whitenoise` (static file serving - backup to S3)
- `psycopg2-binary` (PostgreSQL adapter)
- `django-storages` (for S3)
- `boto3` (AWS SDK)

### Step 6: Update settings.py

The `settings.py` file has been updated to support:
- AWS S3 for static and media files
- Heroku deployment settings
- Production security settings
- Environment-based configuration

### Step 7: Create .env File for Local Development (Optional)

Create a `.env` file in your project root for local development:

```env
SECRET_KEY=your-local-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
USE_S3=False
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Note**: Add `.env` to `.gitignore` to avoid committing sensitive data.

### Step 8: Initialize Git Repository (if not already done)

```bash
# Initialize git (if not already initialized)
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Ready for deployment"

# Add Heroku remote
heroku git:remote -a lundkhwar-mobile-center
```

### Step 9: Deploy to Heroku

```bash
# Deploy to Heroku
git push heroku main

# Or if using master branch
git push heroku master
```

### Step 10: Run Migrations

```bash
# Run database migrations
heroku run python manage.py migrate

# Create superuser (optional)
heroku run python manage.py createsuperuser

# Collect static files to S3
heroku run python manage.py collectstatic --noinput
```

### Step 11: Verify Deployment

```bash
# Open your app in browser
heroku open

# Check logs
heroku logs --tail
```

## Part 3: Post-Deployment Tasks

### Step 1: Set Up Domain (Optional)

If you have a custom domain:

```bash
# Add custom domain
heroku domains:add www.yourdomain.com
heroku domains:add yourdomain.com

# Update DNS records as instructed by Heroku
```

### Step 2: Set Up Site Settings

1. Log in to Django admin: `https://your-app.herokuapp.com/admin/`
2. Go to "Core" → "Site Settings"
3. Update:
   - Site name: "LUNDKHWAR MOBILE CENTER"
   - Site description
   - Contact email
   - Phone number
   - Social media links

### Step 3: Upload Media Files to S3

If you have existing media files:

```bash
# Option 1: Use AWS CLI
aws s3 sync media/ s3://your-bucket-name/media/ --region ap-south-1

# Option 2: Use Django management command (if created)
heroku run python manage.py upload_media_to_s3
```

### Step 4: Set Up Automated Backups

```bash
# Enable automated backups for PostgreSQL
heroku pg:backups:schedule DATABASE_URL --at '02:00 Asia/Karachi'

# Create manual backup
heroku pg:backups:capture
```

### Step 5: Monitor Your Application

```bash
# View application metrics
heroku ps

# View recent logs
heroku logs --tail

# Scale dynos (if needed)
heroku ps:scale web=1
```

## Part 4: Environment Variables Summary

Here's a complete list of environment variables you need to set on Heroku:

### Required Variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `False` for production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `USE_S3` - Set to `True` to use AWS S3
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_STORAGE_BUCKET_NAME` - Your S3 bucket name
- `AWS_S3_REGION_NAME` - AWS region (e.g., `ap-south-1`)

### Optional Variables:
- `EMAIL_BACKEND` - Email backend (SMTP for production)
- `EMAIL_HOST` - SMTP server
- `EMAIL_PORT` - SMTP port (usually 587)
- `EMAIL_USE_TLS` - Use TLS (True/False)
- `EMAIL_HOST_USER` - Email username
- `EMAIL_HOST_PASSWORD` - Email password
- `DEFAULT_FROM_EMAIL` - Default sender email
- `SITE_ID` - Django site ID (usually 1)

## Part 5: Troubleshooting

### Issue: Static files not loading
**Solution**: 
- Verify `USE_S3=True` is set
- Check AWS credentials are correct
- Run `heroku run python manage.py collectstatic --noinput`
- Verify S3 bucket policy allows public read access

### Issue: Media files not uploading
**Solution**:
- Check AWS credentials
- Verify S3 bucket has `media/` folder
- Check IAM user has write permissions
- Verify `DEFAULT_FILE_STORAGE` is set correctly

### Issue: Database connection errors
**Solution**:
- Verify PostgreSQL addon is attached: `heroku addons`
- Check DATABASE_URL is set: `heroku config:get DATABASE_URL`
- Run migrations: `heroku run python manage.py migrate`

### Issue: Application crashes on startup
**Solution**:
- Check logs: `heroku logs --tail`
- Verify all required environment variables are set
- Check `Procfile` is correct
- Verify `requirements.txt` is up to date

## Part 6: Maintenance

### Regular Tasks:

1. **Update Dependencies**:
   ```bash
   # Update requirements.txt
   pip freeze > requirements.txt
   git add requirements.txt
   git commit -m "Update dependencies"
   git push heroku main
   ```

2. **Database Backups**:
   ```bash
   # Create backup
   heroku pg:backups:capture
   
   # Download backup
   heroku pg:backups:download
   ```

3. **Monitor Logs**:
   ```bash
   heroku logs --tail
   ```

4. **Scale Application**:
   ```bash
   # Scale web dynos
   heroku ps:scale web=2
   ```

## Part 7: Cost Estimation

### Heroku:
- **Hobby Dyno**: $7/month (or free tier with limitations)
- **PostgreSQL Hobby Dev**: Free (with limitations)
- **Add-ons**: Varies

### AWS S3:
- **Storage**: ~$0.023 per GB/month
- **Requests**: ~$0.005 per 1,000 requests
- **Data Transfer**: First 100 GB free, then ~$0.09 per GB

**Estimated Monthly Cost**: $10-20 for small to medium traffic

## Support

For issues or questions:
- Check Heroku logs: `heroku logs --tail`
- Check AWS CloudWatch logs
- Review Django error logs in admin panel
- Contact support with specific error messages

## Additional Resources

- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
- [Django on Heroku](https://devcenter.heroku.com/articles/django-app-configuration)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [django-storages Documentation](https://django-storages.readthedocs.io/)

---

**Last Updated**: 2025-01-XX
**Version**: 1.0



