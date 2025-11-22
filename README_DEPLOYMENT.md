# Quick Deployment Guide - LUNDKHWAR MOBILE CENTER

## Quick Start Checklist

### 1. AWS S3 Setup (15 minutes)

1. **Create S3 Bucket**
   - Name: `lundkhwar-mobile-center` (or your choice)
   - Region: `ap-south-1` (Mumbai - closest to Pakistan)
   - Uncheck "Block all public access"

2. **Set Bucket Policy** (Permissions → Bucket Policy):
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }]
}
```

3. **Create IAM User**
   - User: `lundkhwar-s3-user`
   - Policy: `AmazonS3FullAccess`
   - **Save Access Key ID and Secret Access Key**

4. **Create Folders in Bucket**
   - `static/`
   - `media/`

### 2. Heroku Setup (10 minutes)

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create lundkhwar-mobile-center

# 3. Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 4. Set environment variables
heroku config:set SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="lundkhwar-mobile-center.herokuapp.com"
heroku config:set USE_S3=True
heroku config:set AWS_ACCESS_KEY_ID="your-aws-access-key"
heroku config:set AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
heroku config:set AWS_STORAGE_BUCKET_NAME="your-bucket-name"
heroku config:set AWS_S3_REGION_NAME="ap-south-1"

# 5. Deploy
git push heroku main

# 6. Run migrations
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput

# 7. Create superuser
heroku run python manage.py createsuperuser
```

### 3. Verify Deployment

```bash
# Open your app
heroku open

# Check logs
heroku logs --tail
```

## Important Notes

1. **Never commit `.env` file** - It contains sensitive information
2. **Always set `DEBUG=False`** in production
3. **Update `ALLOWED_HOSTS`** with your domain when you get one
4. **Backup database regularly**: `heroku pg:backups:capture`

## Troubleshooting

- **Static files not loading**: Check AWS credentials and run `collectstatic`
- **Database errors**: Verify PostgreSQL addon is attached
- **App crashes**: Check logs with `heroku logs --tail`

For detailed instructions, see `DEPLOYMENT.md`



