# Fluxor API - Advanced Cryptocurrency Trading Platform

A comprehensive Django-based cryptocurrency trading API with advanced features including real-time price feeds, algorithmic trading, risk management, compliance monitoring, and a Vue.js frontend.

## Features

### Core Trading Features
- **Real-time Market Data**: Live price feeds from multiple exchanges
- **Order Management**: Advanced order types and execution
- **Portfolio Management**: Comprehensive portfolio tracking and analytics
- **Risk Management**: Automated risk monitoring and position limits
- **Algorithmic Trading**: Custom trading strategies and automation

### Advanced Features
- **Compliance Monitoring**: KYC/AML checks and regulatory reporting
- **Alert System**: Real-time notifications and trading signals
- **Reporting Engine**: Automated report generation and scheduling
- **WebSocket Support**: Real-time updates and notifications
- **Rate Limiting**: API protection and usage monitoring

### Infrastructure
- **Celery Tasks**: Background processing and scheduled tasks
- **Redis Caching**: High-performance caching layer
- **PostgreSQL**: Robust database backend
- **Docker Support**: Containerized deployment
- **API Documentation**: Swagger/OpenAPI documentation

## Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **Celery**: Background task processing
- **Redis**: Caching and message broker
- **PostgreSQL**: Database
- **Channels**: WebSocket support

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vue Router**: Client-side routing
- **Pinia**: State management
- **Chart.js**: Data visualization

### Trading & Cryptocurrency
- **CCXT**: Cryptocurrency exchange library
- **Bitcoin**: Bitcoin integration
- **Coincurve**: Cryptography utilities

## Project Structure

```
fluxor_api/
├── accounts/                 # User management and authentication
├── wallets/                  # Cryptocurrency wallet management
├── trades/                   # Trade execution and history
├── blockchain/               # Blockchain integration and monitoring
├── market_data/              # Real-time market data and feeds
├── order_management/         # Order processing and management
├── portfolio_management/     # Portfolio tracking and analytics
├── trading_engine/           # Trading algorithms and strategies
├── risk_management/          # Risk monitoring and limits
├── compliance/               # KYC/AML and regulatory compliance
├── alerts/                   # Alert system and notifications
├── reports/                  # Report generation and scheduling
├── core/                     # Core utilities and middleware
├── src/                      # Vue.js frontend
└── fluxor_api/               # Django project settings
```

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- Node.js 16+ (for frontend)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fluxor_api
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

4. **Environment configuration**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load initial data**
   ```bash
   python manage.py loaddata initial_data.json
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd src
   npm install
   ```

2. **Development server**
   ```bash
   npm run dev
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=fluxor_api
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Bitcoin
BITCOIN_NETWORK=testnet
COMPANY_WALLET_LABEL=company_wallet

# Trading
DEFAULT_EXCHANGE=binance
API_KEY=your-api-key
API_SECRET=your-api-secret
```

### Celery Configuration

1. **Start Redis**
   ```bash
   redis-server
   ```

2. **Start Celery worker**
   ```bash
   celery -A fluxor_api worker -l info
   ```

3. **Start Celery beat (for scheduled tasks)**
   ```bash
   celery -A fluxor_api beat -l info
   ```

## Running the Application

### Development

1. **Start Django server**
   ```bash
   python manage.py runserver
   ```

2. **Start Celery worker**
   ```bash
   celery -A fluxor_api worker -l info
   ```

3. **Start Celery beat**
   ```bash
   celery -A fluxor_api beat -l info
   ```

4. **Start frontend**
   ```bash
   cd src && npm run dev
   ```

### Production

1. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

2. **Use production server**
   ```bash
   gunicorn fluxor_api.wsgi:application
   ```

## API Documentation

The API documentation is available at:
- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

### Key Endpoints

#### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/refresh/` - Token refresh

#### Trading
- `GET /api/trades/` - Get user trades
- `POST /api/orders/` - Create order
- `GET /api/portfolio/` - Get portfolio

#### Market Data
- `GET /api/market-data/prices/` - Get current prices
- `GET /api/market-data/orderbook/` - Get order book
- `GET /api/market-data/trades/` - Get recent trades

## WebSocket Endpoints

- `ws://localhost:8000/ws/price/` - Real-time price updates
- `ws://localhost:8000/ws/trading/` - Trading updates
- `ws://localhost:8000/ws/alerts/` - Alert notifications
- `ws://localhost:8000/ws/market-data/` - Market data updates

## Testing

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
cd src && npm run test
```

## Deployment

### Docker Deployment

1. **Build images**
   ```bash
   docker-compose build
   ```

2. **Run services**
   ```bash
   docker-compose up -d
   ```

### Manual Deployment

1. **Set up production environment**
   ```bash
   export DJANGO_SETTINGS_MODULE=fluxor_api.settings.production
   ```

2. **Configure web server (nginx)**
   ```bash
   # Configure nginx for static files and proxy
   ```

3. **Set up SSL certificates**
   ```bash
   # Configure SSL with Let's Encrypt or similar
   ```

## Monitoring and Logging

### Logging Configuration
Logs are stored in the `logs/` directory:
- `django.log` - Django application logs
- `celery.log` - Celery task logs

### Health Checks
- **API Health**: `GET /api/health/`
- **Database Health**: `GET /api/health/db/`
- **Redis Health**: `GET /api/health/redis/`

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: API protection against abuse
- **CORS Configuration**: Cross-origin request handling
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Security headers and validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## Roadmap

### Upcoming Features
- **Advanced Trading Algorithms**: Machine learning-based strategies
- **Social Trading**: Copy trading and social features
- **Mobile App**: React Native mobile application
- **Advanced Analytics**: Enhanced portfolio analytics
- **Multi-language Support**: Internationalization
- **Advanced Risk Models**: Sophisticated risk assessment

### Performance Improvements
- **Database Optimization**: Query optimization and indexing
- **Caching Strategy**: Advanced caching implementation
- **Load Balancing**: Horizontal scaling support
- **Microservices**: Service decomposition 