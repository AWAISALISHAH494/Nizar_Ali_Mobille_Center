# Professional E-commerce Website

A full-featured, professional e-commerce platform built with Django, HTML5, CSS3, and JavaScript.

## Features

### Core Features
- **User Management**: Registration, authentication, profiles, addresses
- **Product Catalog**: Categories, products, variants, search, filtering
- **Shopping Cart**: Persistent cart, guest checkout, quantity management
- **Order Management**: Checkout, order tracking, order history
- **Payment Integration**: Stripe and PayPal support
- **Reviews & Ratings**: Product reviews, ratings, helpful votes
- **Wishlist**: Save products for later
- **Coupons**: Discount codes and promotional campaigns
- **Analytics**: User behavior tracking, sales analytics
- **Admin Dashboard**: Comprehensive management interface

### Technical Features
- **Responsive Design**: Mobile-first, modern UI
- **Security**: CSRF protection, XSS prevention, secure authentication
- **Performance**: Caching, image optimization, lazy loading
- **SEO**: Meta tags, structured data, sitemap
- **Scalability**: Horizontal scaling, load balancing ready

## Technology Stack

- **Backend**: Django 4.2+ (Python 3.9+)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: PostgreSQL 14+
- **Cache**: Redis 6+
- **Search**: Elasticsearch 8+
- **Payment**: Stripe API, PayPal API
- **Email**: SendGrid/AWS SES
- **Storage**: AWS S3 (for media files)
- **Deployment**: Docker, AWS/DigitalOcean

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- Node.js (for frontend assets)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-website
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py loaddata fixtures/sample_data.json
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Docker Development

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Gateways
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret

# Redis
REDIS_URL=redis://localhost:6379/1
```

### Payment Setup

1. **Stripe Setup**
   - Create a Stripe account
   - Get your API keys from the Stripe dashboard
   - Add webhook endpoints for payment processing

2. **PayPal Setup**
   - Create a PayPal developer account
   - Create a new application
   - Get your client ID and secret

## Deployment

### Production Deployment

1. **Set up production environment**
   ```bash
   # Set production environment variables
   export DEBUG=False
   export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   export DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the application**
   ```bash
   gunicorn --bind 0.0.0.0:8000 ecommerce.wsgi:application
   ```

### Docker Production

1. **Build production image**
   ```bash
   docker build -t ecommerce-app .
   ```

2. **Run with production settings**
   ```bash
   docker run -d -p 8000:8000 -e DEBUG=False ecommerce-app
   ```

## API Documentation

### Authentication Endpoints
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout

### Product Endpoints
- `GET /products/` - List products
- `GET /products/{id}/` - Product detail
- `GET /products/search/` - Search products

### Cart Endpoints
- `GET /cart/` - Get cart contents
- `POST /cart/add/` - Add item to cart
- `PUT /cart/update/` - Update cart item
- `DELETE /cart/remove/` - Remove item from cart

### Order Endpoints
- `POST /orders/checkout/` - Create order
- `GET /orders/{id}/` - Order detail
- `GET /orders/` - User orders

## Testing

### Run Tests
```bash
python manage.py test
```

### Run with Coverage
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Performance Optimization

### Database Optimization
- Use database indexes for frequently queried fields
- Implement database connection pooling
- Use select_related and prefetch_related for queries

### Caching
- Redis for session storage and caching
- Implement page-level caching for static content
- Use CDN for static file delivery

### Frontend Optimization
- Minify CSS and JavaScript
- Implement lazy loading for images
- Use browser caching for static assets

## Security

### Security Measures
- CSRF protection enabled
- XSS protection with content security policy
- SQL injection prevention with ORM
- Rate limiting for API endpoints
- Secure password hashing
- HTTPS enforcement in production

### Security Checklist
- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS in production
- [ ] Configure secure headers
- [ ] Regular security updates
- [ ] Database backups

## Monitoring and Analytics

### Analytics Features
- User behavior tracking
- Sales analytics
- Product performance metrics
- Conversion tracking
- Customer segmentation

### Monitoring
- Application performance monitoring
- Error tracking and logging
- Database performance monitoring
- Server resource monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact: support@ecommerce.com
- Documentation: [docs.ecommerce.com](https://docs.ecommerce.com)

## Changelog

### Version 1.0.0
- Initial release
- Core e-commerce functionality
- Payment integration
- Admin dashboard
- Mobile-responsive design
