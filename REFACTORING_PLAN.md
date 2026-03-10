# Refactoring Plan: To Expense Tracker & Budget Optimizer

**Current State**: Financial Suggestions Application (investment/retirement planning)  
**Target State**: AI-Powered Personal Finance & Expense Optimizer  
**Date**: March 10, 2026

---

## 📋 Phase 1: Database Schema Refactoring (30-45 min)

### ❌ Remove (Current - No Longer Needed)
- Investment goal types (car, home, education, retirement goals)
- Retirement product recommendations tables
- Investment options table
- Market data caching tables

### ✅ Add (New - Expense Tracking)
```sql
CREATE TABLE expense_categories (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    category_name TEXT (Groceries, Transport, Entertainment, Bills, etc.),
    color_code TEXT,
    created_at TIMESTAMP
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    category_id INTEGER,
    amount DECIMAL,
    description TEXT,
    date DATE,
    auto_categorized BOOLEAN,
    receipt_image PATH,
    created_at TIMESTAMP,
    FOREIGN KEY(category_id) REFERENCES expense_categories(id)
);

CREATE TABLE budgets (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    category_id INTEGER,
    monthly_limit DECIMAL,
    start_date DATE,
    end_date DATE,
    alert_threshold INTEGER (80%, 90%, 100%),
    created_at TIMESTAMP
);

CREATE TABLE spending_alerts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    budget_id INTEGER,
    alert_type TEXT (THRESHOLD_EXCEEDED, UNUSUAL_SPENDING),
    message TEXT,
    severity TEXT (LOW, MEDIUM, HIGH),
    read_status BOOLEAN,
    created_at TIMESTAMP
);

CREATE TABLE savings_goals (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    goal_name TEXT,
    target_amount DECIMAL,
    current_amount DECIMAL,
    monthly_target DECIMAL,
    deadline DATE,
    category TEXT,
    created_at TIMESTAMP
);
```

### ✏️ Modify (Existing)
- **User table**: Add columns for
  - `monthly_income` 
  - `spending_preferences` (JSON)
  - `preferred_alert_method` (email, push, in-app)
  
- **Income table**: Keep as-is (already exists)

---

## 🎨 Phase 2: Frontend Refactoring (1-2 hours)

### ❌ Remove Templates
- `results.html` (investment results)
- Goal-specific recommendation pages

### ✅ Add/Update Templates
| Template | Purpose |
|----------|---------|
| `dashboard.html` | Expense summary, budget status, alerts |
| `add-expense.html` | Single/bulk expense entry |
| `expenses.html` | Expense history with filters |
| `budgets.html` | Create/manage budgets |
| `reports.html` | Charts, graphs, spending trends |
| `savings.html` | Savings goals tracking |
| `alerts.html` | Spending alerts & notifications |
| `settings.html` | Budget preferences, alert settings |

### 📊 Charts Needed (Chart.js/Plotly)
- Pie chart: Spending by category
- Line chart: Spending trends (monthly)
- Bar chart: Budget vs. actual spending
- Progress bars: Savings goals

---

## ⚙️ Phase 3: Backend Logic Refactoring (2-3 hours)

### Core Modules to Rewrite

#### 1. **Expense Auto-Categorization** (NEW)
```
Module: expense_categorizer.py
- NLP-based description parsing
- ML model to suggest category
- Keywords mapping (groceries → food, uber → transport)
```

#### 2. **Budget Management** (NEW)
```
Module: budget_manager.py
- Create monthly budgets by category
- Track spending vs. budget
- Alert generation logic
```

#### 3. **Spending Pattern Analysis** (NEW)
```
Module: spending_analyzer.py
- Detect unusual spending patterns
- Calculate average spending by category
- Predict next month spending
- Generate saving recommendations
```

#### 4. **Alerts & Notifications** (NEW)
```
Module: alert_system.py
- Budget threshold alerts
- Unusual spending detection
- Gentle nudges for savings goals
```

#### 5. **Reports & Insights** (MODIFY)
```
Rewrite: api_integrations.py / reporting.py
- Monthly spending summaries
- Category insights
- Savings opportunities
- Tips based on spending habits
```

#### 6. **Remove Entirely**
```
- All Gemini-powered investment recommendations
- Real-time market data fetching (yfinance, CoinGecko)
- Investment calculation logic
```

---

## 🤖 Phase 4: AI Integration (1-2 hours)

### Use Gemini API For
1. **Expense categorization** (auto-suggest category from description)
2. **Spending insights** (generate human-readable analysis)
3. **Savings recommendations** (personalized tips based on habits)
4. **Budget suggestions** (recommend budget limits based on history)

### Example Prompt
```
"Based on this user's spending history:
- Groceries: ₹8,000/month
- Entertainment: ₹3,500/month  
- Transport: ₹2,500/month
- Utilities: ₹2,000/month

Provide 3 specific, actionable ways they can save ₹1,500/month without sacrificing quality of life."
```

---

## 📱 Phase 5: New Features to Add (Ongoing)

### Immediate (MVP)
- ✅ Expense entry (manual)
- ✅ Auto-categorization
- ✅ Budget creation & tracking
- ✅ Dashboard with spending overview
- ✅ Monthly reports
- ✅ Basic alerts

### Near-term (v1.1)
- 🔲 Bulk CSV expense import
- 🔲 Spending analytics & trends
- 🔲 Savings recommendations from Gemini
- 🔲 Recurring expense management
- 🔲 Email alerts

### Future Enhancements
- 🔲 Voice expense logging (speech-to-text)
- 🔲 Regional language support
- 🔲 Bill payment integration
- 🔲 Automatic bill categorization (from SMS)
- 🔲 Mobile app
- 🔲 Multi-user family budgets
- 🔲 Bank API integration (auto-sync expenses)

---

## 📊 Effort Estimation

| Phase | Time | Difficulty |
|-------|------|-----------|
| Database refactoring | 30-45 min | Medium |
| Frontend redesign | 1-2 hours | Medium |
| Backend rewrite | 2-3 hours | Hard |
| AI integration | 1-2 hours | Medium |
| Testing & debugging | 1-2 hours | Medium |
| **TOTAL** | **6-10 hours** | - |

---

## ✅ Implementation Checklist

- [ ] Phase 1: Update `database.py` with new schema
- [ ] Phase 2: Create new HTML templates
- [ ] Phase 3: Write expense categorizer module
- [ ] Phase 3: Write budget manager module
- [ ] Phase 3: Write spending analyzer module
- [ ] Phase 3: Write alert system module
- [ ] Phase 3: Rewrite `app.py` routes for new features
- [ ] Phase 4: Integrate Gemini for insights
- [ ] Phase 5: Add auto-categorization logic
- [ ] Testing: Manual testing of all features
- [ ] Documentation: Update README.md

---

## 🚀 Migration Strategy

**Option A: Big Bang Refactoring** (Riskier, faster)
- Backup current project
- Delete old code
- Rewrite from scratch

**Option B: Gradual Migration** (Safer, slower)
- Keep both systems temporarily
- Build new expense tracking in parallel
- Switch routes gradually
- Remove old code after validation

**Recommendation**: Option B (safer for production)

---

## 🤔 Questions Before Starting

1. Should we keep ANY investment planning features, or COMPLETELY pivot?
2. Do you have sample expense data to test categorization?
3. Should we include repeat expenses (subscriptions, rent, etc.)?
4. Want to support multiple currencies or just INR?
5. Should expenses have receipt image upload feature?
