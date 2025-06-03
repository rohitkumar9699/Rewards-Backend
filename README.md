
# 🏆 Rewards Management System

This Django project provides a backend system to manage reward wallets and scratchable reward cards for users. It includes wallet balance updates, reward calculation, card lifecycle management, and integration with external APIs.

## 🔧 Features

- User reward wallet with balance tracking
- Scratchable reward cards with time-based access
- Reward amount calculated from product amount and reward rate
- Admin dashboard for wallets and cards
- External API call to fund wallet balance
- Decimal-safe reward calculations

## 🧩 Models

### RewardWallet
- `wallet_username`: Unique identifier for the wallet
- `wallet_fullname`: Full name of the wallet owner
- `wallet_communication_email`: Email
- `wallet_balance`: Decimal balance of rewards

### RewardCards
- Linked to `RewardWallet` via `order_by`
- `product_name`, `product_id`, `final_amount`
- `reward_rate`: Multiplier or percentage rate
- `reward_amount`: Auto-calculated reward = final_amount * reward_rate
- Status flags: `is_active`, `processed`, `scratch_status`
- `scratch_from`, `scratch_to`: Time window for scratching the card
- `valid_from`, `valid_to`: Card validity period

## 📡 APIs

- **CardScratchView**: Validates and scratches a card if within allowed time window.
- **ReedomCoinView**: Reads wallet info and makes POST request to fund wallet via external service.

## 🛡️ Security

- Uses `DecimalField` for all monetary values (accurate + safe)
- Secret key stored securely (ensure `.env` for production)

## 🧪 Admin Panel

Custom admin panel views:
- Inline filters and field grouping for RewardWallet and RewardCards
- Read-only fields for non-editable values
- Search and filter support

## 🏁 Setup Instructions

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Run server: `python manage.py runserver`

## 📁 Folder Structure

- `models.py`: Wallets & Cards models
- `views.py`: Scratch & reward APIs
- `admin.py`: Improved admin interface
- `urls.py`: API endpoints

## 📬 Contact

Maintainer: Rohit Kumar  
Email: rk94523386@gmail.com
