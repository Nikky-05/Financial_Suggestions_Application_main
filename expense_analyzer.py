"""
Expense Categorizer and AI Analysis Module
Automatically categorizes expenses and provides AI-powered financial insights
"""
import google.generativeai as genai
from datetime import datetime, timedelta
import os
import logging

logger = logging.getLogger(__name__)

# Default expense categories with keywords
EXPENSE_CATEGORIES = {
    'Groceries': ['milk', 'bread', 'vegetable', 'fruit', 'grocery', 'supermarket', 'bazar', 'market', 'dal', 'rice', 'wheat'],
    'Transport': ['uber', 'ola', 'cab', 'taxi', 'petrol', 'diesel', 'fuel', 'auto', 'bus', 'train', 'metro', 'ticket'],
    'Entertainment': ['movie', 'cinema', 'game', 'park', 'restaurant', 'cafe', 'pizza', 'burger', 'bar', 'club', 'spotify', 'netflix'],
    'Bills': ['electricity', 'water', 'gas', 'phone', 'internet', 'mobile', 'broadband', 'wifi', 'utility'],
    'Healthcare': ['doctor', 'hospital', 'medicine', 'pharmacy', 'clinic', 'medical', 'health', 'dental', 'ayurveda'],
    'Clothes': ['shirt', 'pant', 'dress', 'shoe', 'clothing', 'apparel', 'fashion', 'mall'],
    'Education': ['book', 'course', 'school', 'college', 'tuition', 'class', 'coaching', 'exam', 'certificate'],
    'Shopping': ['amazon', 'flipkart', 'ebay', 'online', 'store', 'shop', 'retail'],
    'Rent': ['rent', 'landlord', 'deposit', 'apartment', 'house', 'accommodation'],
    'Fitness': ['gym', 'yoga', 'swimming', 'sports', 'fitness', 'trainer', 'exercise']
}

class ExpenseCategorizer:
    """AI-powered expense categorizer"""
    
    @staticmethod
    def categorize(description, amount=None):
        """
        Categorize expense based on description
        Returns: (category, confidence)
        """
        description_lower = description.lower()
        
        # Keyword-based categorization
        for category, keywords in EXPENSE_CATEGORIES.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category, "high"
        
        # Default to Shopping if not categorized
        return "Shopping", "low"
    
    @staticmethod
    def suggest_with_gemini(description):
        """Use Gemini API for smart categorization"""
        try:
            genai_key = os.getenv('GEMINI_API_KEY')
            if not genai_key:
                logger.warning("Gemini API key not found, using keyword categorization")
                return ExpenseCategorizer.categorize(description)
            
            genai.configure(api_key=genai_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            categories_list = ', '.join(EXPENSE_CATEGORIES.keys())
            prompt = f"""
Categorize this expense description into ONE of these categories:
{categories_list}

Description: "{description}"

Return ONLY the category name, nothing else. If unsure, pick the most likely category.
"""
            response = model.generate_content(prompt)
            category = response.text.strip()
            
            # Validate that returned category exists
            if category in EXPENSE_CATEGORIES:
                return category, "high"
            else:
                return ExpenseCategorizer.categorize(description)
                
        except Exception as e:
            logger.error(f"Gemini categorization error: {e}")
            return ExpenseCategorizer.categorize(description)


class FinancialAnalyzer:
    """AI-powered financial analysis and insights"""
    
    def __init__(self, user_data, expenses, income):
        self.user_data = user_data
        self.expenses = expenses
        self.income = income
    
    def calculate_stats(self):
        """Calculate spending statistics"""
        total_expenses = sum([e['amount'] for e in self.expenses])
        total_income = sum([i['amount'] for i in self.income])
        balance = total_income - total_expenses
        savings_rate = (balance / total_income * 100) if total_income > 0 else 0
        
        # Category breakdown
        category_breakdown = {}
        for expense in self.expenses:
            cat = expense.get('category', 'Other')
            category_breakdown[cat] = category_breakdown.get(cat, 0) + expense['amount']
        
        # Top spending categories
        top_categories = sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'total_income': round(total_income, 2),
            'total_expenses': round(total_expenses, 2),
            'balance': round(balance, 2),
            'savings_rate': round(savings_rate, 2),
            'category_breakdown': category_breakdown,
            'top_categories': top_categories,
            'expense_count': len(self.expenses),
            'average_expense': round(total_expenses / len(self.expenses), 2) if self.expenses else 0
        }
    
    def get_ai_recommendations(self):
        """Get AI-powered savings recommendations"""
        try:
            stats = self.calculate_stats()
            genai_key = os.getenv('GEMINI_API_KEY')
            
            if not genai_key:
                return self._default_recommendations(stats)
            
            genai.configure(api_key=genai_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            category_str = ', '.join([f"{cat}: ₹{amt}" for cat, amt in stats['category_breakdown'].items()])
            
            prompt = f"""
You are a personal finance advisor. Analyze this user's spending and provide SPECIFIC, ACTIONABLE savings tips.

User: {self.user_data.get('name', 'User')}
Monthly Income: ₹{stats['total_income']}
Monthly Expenses: ₹{stats['total_expenses']}
Savings Rate: {stats['savings_rate']}%

Spending Breakdown:
{category_str}

Top 3 Spending Categories: {', '.join([f"{cat}: ₹{amt}" for cat, amt in stats['top_categories']])}

Provide 3-4 SPECIFIC money-saving tips the user can implement immediately. Be concise and actionable.
Format: Start each tip with "💡 " followed by the tip.
"""
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Parse response into tips
            tips = [line.strip() for line in text.split('\n') if line.strip() and ('💡' in line or '•' in line or '-' in line)]
            
            return tips if tips else self._default_recommendations(stats)
            
        except Exception as e:
            logger.error(f"AI recommendations error: {e}")
            stats = self.calculate_stats()
            return self._default_recommendations(stats)
    
    def _default_recommendations(self, stats):
        """Default recommendations when AI is unavailable"""
        recommendations = []
        
        # Tip 1: Check top spending category
        if stats['top_categories']:
            top_cat, top_amount = stats['top_categories'][0]
            recommendations.append(f"💡 Your highest spending is in {top_cat} (₹{top_amount}). Look for ways to reduce this by 10-15%.")
        
        # Tip 2: Savings rate
        if stats['savings_rate'] < 20:
            recommendations.append(f"💡 Your savings rate is {stats['savings_rate']}%. Try to increase it to at least 20% by cutting non-essential expenses.")
        else:
            recommendations.append(f"💡 Great! You're saving {stats['savings_rate']}% of your income. Keep it up!")
        
        # Tip 3: General advice
        recommendations.append("💡 Track your daily expenses in the app to identify spending patterns and opportunities to save.")
        
        # Tip 4: Budget planning
        if stats['total_expenses'] > 0:
            avg_per_category = stats['total_expenses'] / len(stats['category_breakdown'])
            recommendations.append(f"💡 Set monthly budgets for each category (avg: ₹{avg_per_category:.0f}) to maintain control.")
        
        return recommendations[:4]
    
    def get_monthly_insight(self):
        """Get monthly spending insight"""
        stats = self.calculate_stats()
        
        if stats['savings_rate'] >= 30:
            insight = f"🎯 Excellent! You're saving {stats['savings_rate']}% of your income."
        elif stats['savings_rate'] >= 20:
            insight = f"✅ Good job! You're saving {stats['savings_rate']}% of your income."
        elif stats['savings_rate'] >= 10:
            insight = f"⚠️ You're saving {stats['savings_rate']}%. Try to increase your savings rate."
        else:
            insight = f"❌ You're spending more than you earn! Urgent action needed."
        
        return insight


def get_expense_insights(user_id, conn):
    """Get complete expense insights for user"""
    cursor = conn.cursor()
    
    # Get current month expenses and income
    today = datetime.now()
    month_start = today.replace(day=1)
    
    cursor.execute('''
        SELECT * FROM expenses 
        WHERE user_id = ? AND date >= ?
        ORDER BY date DESC
    ''', (user_id, month_start))
    expenses = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('''
        SELECT * FROM income 
        WHERE user_id = ? AND date >= ?
        ORDER BY date DESC
    ''', (user_id, month_start))
    income = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = dict(cursor.fetchone())
    
    analyzer = FinancialAnalyzer(user, expenses, income)
    
    return {
        'stats': analyzer.calculate_stats(),
        'recommendations': analyzer.get_ai_recommendations(),
        'insight': analyzer.get_monthly_insight(),
        'expenses': expenses,
        'income': income
    }
