#!/usr/bin/env python3
"""
Financial Statement Generator for Z K FITNESS CLUB
Based on Trial Balance data for the year ended December 31, 2024
Currency: QAR (Qatari Riyal)
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style for plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

class FinancialStatementGenerator:
    def __init__(self, tb_file_path):
        """Initialize with the path to the structured Trial Balance file"""
        self.tb_file_path = tb_file_path
        self.df = pd.read_csv(tb_file_path)
        self.company_name = "Z K FITNESS CLUB"
        self.period_end = "December 31, 2024"
        self.currency = "QAR"
        self.output_dir = os.path.dirname(tb_file_path)
        
    def generate_all_statements(self):
        """Generate all financial statements"""
        self.generate_balance_sheet()
        self.generate_income_statement()
        self.generate_cash_flow_statement()
        self.generate_visualizations()
        print(f"All financial statements have been generated in {self.output_dir}")
        
    def generate_balance_sheet(self):
        """Generate Balance Sheet"""
        # Filter accounts by classification
        assets = self.df[self.df['classification'] == 'Asset'].copy()
        liabilities = self.df[self.df['classification'] == 'Liability'].copy()
        equity = self.df[self.df['classification'] == 'Equity'].copy()
        
        # Calculate net income/loss
        revenue = self.df[self.df['classification'] == 'Revenue']['closing_balance'].sum()
        expenses = self.df[self.df['classification'] == 'Expense']['closing_balance'].sum()
        net_income = abs(revenue) - expenses
        
        # Create balance sheet dataframe
        balance_sheet = []
        
        # Assets section
        balance_sheet.append({"Category": "ASSETS", "Account": "", "Amount": ""})
        balance_sheet.append({"Category": "Current Assets", "Account": "", "Amount": ""})
        
        # Current Assets
        current_assets = assets[assets['account_name'].str.contains('CASH|BANK|RECEIVABLE|INVENTORY|PREPAID|LOAN GIVEN', case=False, na=False)]
        for _, row in current_assets.iterrows():
            balance_sheet.append({
                "Category": "", 
                "Account": row['account_name'], 
                "Amount": f"{row['closing_balance']:,.2f}"
            })
        current_assets_total = current_assets['closing_balance'].sum()
        balance_sheet.append({"Category": "", "Account": "Total Current Assets", "Amount": f"{current_assets_total:,.2f}"})
        
        # Non-Current Assets
        balance_sheet.append({"Category": "Non-Current Assets", "Account": "", "Amount": ""})
        non_current_assets = assets[~assets['account_name'].str.contains('CASH|BANK|RECEIVABLE|INVENTORY|PREPAID|LOAN GIVEN', case=False, na=False)]
        for _, row in non_current_assets.iterrows():
            balance_sheet.append({
                "Category": "", 
                "Account": row['account_name'], 
                "Amount": f"{row['closing_balance']:,.2f}"
            })
        non_current_assets_total = non_current_assets['closing_balance'].sum()
        balance_sheet.append({"Category": "", "Account": "Total Non-Current Assets", "Amount": f"{non_current_assets_total:,.2f}"})
        
        # Total Assets
        total_assets = current_assets_total + non_current_assets_total
        balance_sheet.append({"Category": "", "Account": "TOTAL ASSETS", "Amount": f"{total_assets:,.2f}"})
        
        # Liabilities section
        balance_sheet.append({"Category": "LIABILITIES", "Account": "", "Amount": ""})
        balance_sheet.append({"Category": "Current Liabilities", "Account": "", "Amount": ""})
        
        # Current Liabilities
        current_liabilities = liabilities[liabilities['account_name'].str.contains('PAYABLE|ACCRUED|ADVANCE', case=False, na=False)]
        for _, row in current_liabilities.iterrows():
            balance_sheet.append({
                "Category": "", 
                "Account": row['account_name'], 
                "Amount": f"{abs(row['closing_balance']):,.2f}"
            })
        current_liabilities_total = abs(current_liabilities['closing_balance'].sum())
        balance_sheet.append({"Category": "", "Account": "Total Current Liabilities", "Amount": f"{current_liabilities_total:,.2f}"})
        
        # Non-Current Liabilities
        balance_sheet.append({"Category": "Non-Current Liabilities", "Account": "", "Amount": ""})
        non_current_liabilities = liabilities[~liabilities['account_name'].str.contains('PAYABLE|ACCRUED|ADVANCE', case=False, na=False)]
        for _, row in non_current_liabilities.iterrows():
            balance_sheet.append({
                "Category": "", 
                "Account": row['account_name'], 
                "Amount": f"{abs(row['closing_balance']):,.2f}"
            })
        non_current_liabilities_total = abs(non_current_liabilities['closing_balance'].sum())
        balance_sheet.append({"Category": "", "Account": "Total Non-Current Liabilities", "Amount": f"{non_current_liabilities_total:,.2f}"})
        
        # Total Liabilities
        total_liabilities = current_liabilities_total + non_current_liabilities_total
        balance_sheet.append({"Category": "", "Account": "TOTAL LIABILITIES", "Amount": f"{total_liabilities:,.2f}"})
        
        # Equity section
        balance_sheet.append({"Category": "EQUITY", "Account": "", "Amount": ""})
        
        # Equity accounts
        for _, row in equity.iterrows():
            balance_sheet.append({
                "Category": "", 
                "Account": row['account_name'], 
                "Amount": f"{abs(row['closing_balance']):,.2f}" if row['closing_balance'] < 0 else f"{row['closing_balance']:,.2f}"
            })
        
        # Current year profit/loss
        balance_sheet.append({
            "Category": "", 
            "Account": "Current Year Profit/(Loss)", 
            "Amount": f"{net_income:,.2f}" if net_income >= 0 else f"({abs(net_income):,.2f})"
        })
        
        # Total Equity
        total_equity = equity['closing_balance'].sum() + net_income
        balance_sheet.append({"Category": "", "Account": "TOTAL EQUITY", "Amount": f"{abs(total_equity):,.2f}"})
        
        # Total Liabilities and Equity
        balance_sheet.append({"Category": "", "Account": "TOTAL LIABILITIES AND EQUITY", "Amount": f"{total_liabilities + abs(total_equity):,.2f}"})
        
        # Convert to DataFrame
        bs_df = pd.DataFrame(balance_sheet)
        
        # Save to CSV
        bs_file_path = os.path.join(self.output_dir, "Balance_Sheet.csv")
        bs_df.to_csv(bs_file_path, index=False)
        
        # Generate HTML version
        html_content = self._generate_html_statement(
            bs_df, 
            "Balance Sheet", 
            f"As at {self.period_end}"
        )
        
        html_file_path = os.path.join(self.output_dir, "Balance_Sheet.html")
        with open(html_file_path, 'w') as f:
            f.write(html_content)
            
        print(f"Balance Sheet generated: {bs_file_path} and {html_file_path}")
        return bs_df
    
    def generate_income_statement(self):
        """Generate Income Statement"""
        # Filter accounts by classification
        revenue = self.df[self.df['classification'] == 'Revenue'].copy()
        expenses = self.df[self.df['classification'] == 'Expense'].copy()
        
        # Create income statement dataframe
        income_statement = []
        
        # Revenue section
        income_statement.append({"Category": "REVENUE", "Account": "", "Amount": ""})
        
        # Revenue accounts
        for _, row in revenue.iterrows():
            income_statement.append({
                "Category": "", 
                "Account": row['account_name'], 
                "Amount": f"{abs(row['closing_balance']):,.2f}"
            })
        
        # Total Revenue
        total_revenue = abs(revenue['closing_balance'].sum())
        income_statement.append({"Category": "", "Account": "TOTAL REVENUE", "Amount": f"{total_revenue:,.2f}"})
        
        # Expenses section
        income_statement.append({"Category": "EXPENSES", "Account": "", "Amount": ""})
        
        # Group expenses by type
        expense_groups = {
            "Employee Related": expenses[expenses['account_name'].str.contains('SALARIES|EMPLOYEE|LABOR|VISA|IMMIGRATION', case=False, na=False)],
            "Premises Related": expenses[expenses['account_name'].str.contains('RENT|UTILITIES|WATER|ELECTRICITY|CLEANING', case=False, na=False)],
            "Administrative": expenses[expenses['account_name'].str.contains('AUDIT|REGISTRATION|STATIONARY|OFFICE|BANK|COMMISSION', case=False, na=False)],
            "Marketing": expenses[expenses['account_name'].str.contains('PROMOTION|ADVERTISING|SPONSOR', case=False, na=False)],
            "Operational": expenses[expenses['account_name'].str.contains('MAINTENANCE|REPAIRS|FUEL|TRAVELLING|REFRESHMENT', case=False, na=False)],
            "Other": expenses[~expenses['account_name'].str.contains('SALARIES|EMPLOYEE|LABOR|VISA|IMMIGRATION|RENT|UTILITIES|WATER|ELECTRICITY|CLEANING|AUDIT|REGISTRATION|STATIONARY|OFFICE|BANK|COMMISSION|PROMOTION|ADVERTISING|SPONSOR|MAINTENANCE|REPAIRS|FUEL|TRAVELLING|REFRESHMENT', case=False, na=False)]
        }
        
        # Add expenses by group
        total_expenses = 0
        for group, group_expenses in expense_groups.items():
            if not group_expenses.empty:
                income_statement.append({"Category": group, "Account": "", "Amount": ""})
                for _, row in group_expenses.iterrows():
                    income_statement.append({
                        "Category": "", 
                        "Account": row['account_name'], 
                        "Amount": f"{row['closing_balance']:,.2f}"
                    })
                group_total = group_expenses['closing_balance'].sum()
                total_expenses += group_total
                income_statement.append({"Category": "", "Account": f"Total {group} Expenses", "Amount": f"{group_total:,.2f}"})
        
        # Total Expenses
        income_statement.append({"Category": "", "Account": "TOTAL EXPENSES", "Amount": f"{total_expenses:,.2f}"})
        
        # Net Income/Loss
        net_income = total_revenue - total_expenses
        income_statement.append({
            "Category": "", 
            "Account": "NET INCOME/(LOSS)", 
            "Amount": f"{net_income:,.2f}" if net_income >= 0 else f"({abs(net_income):,.2f})"
        })
        
        # Convert to DataFrame
        is_df = pd.DataFrame(income_statement)
        
        # Save to CSV
        is_file_path = os.path.join(self.output_dir, "Income_Statement.csv")
        is_df.to_csv(is_file_path, index=False)
        
        # Generate HTML version
        html_content = self._generate_html_statement(
            is_df, 
            "Income Statement", 
            f"For the year ended {self.period_end}"
        )
        
        html_file_path = os.path.join(self.output_dir, "Income_Statement.html")
        with open(html_file_path, 'w') as f:
            f.write(html_content)
            
        print(f"Income Statement generated: {is_file_path} and {html_file_path}")
        return is_df
    
    def generate_cash_flow_statement(self):
        """Generate a simplified Cash Flow Statement based on available data"""
        # This is a simplified version as we don't have opening balances for all accounts
        
        # Get cash and bank accounts
        cash_accounts = self.df[self.df['account_name'].str.contains('CASH|BANK', case=False, na=False)].copy()
        
        # Calculate net change in cash
        net_cash_change = cash_accounts['closing_balance'].sum() - cash_accounts['opening_balance'].sum()
        
        # Create cash flow statement dataframe
        cash_flow = []
        
        # Header
        cash_flow.append({"Category": "CASH FLOWS", "Description": "", "Amount": ""})
        
        # Operating Activities
        cash_flow.append({"Category": "Operating Activities", "Description": "", "Amount": ""})
        
        # Calculate net income
        revenue = abs(self.df[self.df['classification'] == 'Revenue']['closing_balance'].sum())
        expenses = self.df[self.df['classification'] == 'Expense']['closing_balance'].sum()
        net_income = revenue - expenses
        
        cash_flow.append({
            "Category": "", 
            "Description": "Net Income/(Loss)", 
            "Amount": f"{net_income:,.2f}" if net_income >= 0 else f"({abs(net_income):,.2f})"
        })
        
        # Adjustments for non-cash items
        depreciation_accounts = self.df[self.df['account_name'].str.contains('DEP|AMORTIZATION', case=False, na=False)]
        depreciation = depreciation_accounts['closing_balance'].sum() - depreciation_accounts['opening_balance'].sum()
        
        if depreciation != 0:
            cash_flow.append({
                "Category": "", 
                "Description": "Depreciation and Amortization", 
                "Amount": f"{abs(depreciation):,.2f}"
            })
        
        # Changes in working capital
        current_assets = self.df[
            (self.df['classification'] == 'Asset') & 
            (~self.df['account_name'].str.contains('CASH|BANK|EQUIPMENT|FURNITURE|INTANGIBLE|ACCU', case=False, na=False))
        ]
        current_assets_change = current_assets['closing_balance'].sum() - current_assets['opening_balance'].sum()
        
        current_liabilities = self.df[self.df['classification'] == 'Liability']
        current_liabilities_change = current_liabilities['closing_balance'].sum() - current_liabilities['opening_balance'].sum()
        
        if current_assets_change != 0:
            cash_flow.append({
                "Category": "", 
                "Description": "Change in Current Assets", 
                "Amount": f"{-current_assets_change:,.2f}" if current_assets_change > 0 else f"{abs(current_assets_change):,.2f}"
            })
            
        if current_liabilities_change != 0:
            cash_flow.append({
                "Category": "", 
                "Description": "Change in Current Liabilities", 
                "Amount": f"{abs(current_liabilities_change):,.2f}" if current_liabilities_change < 0 else f"{current_liabilities_change:,.2f}"
            })
        
        # Net cash from operating activities (simplified)
        net_operating_cash = net_income - current_assets_change + current_liabilities_change
        cash_flow.append({
            "Category": "", 
            "Description": "Net Cash from Operating Activities", 
            "Amount": f"{net_operating_cash:,.2f}" if net_operating_cash >= 0 else f"({abs(net_operating_cash):,.2f})"
        })
        
        # Investing Activities
        cash_flow.append({"Category": "Investing Activities", "Description": "", "Amount": ""})
        
        # Capital expenditures
        fixed_assets = self.df[self.df['account_name'].str.contains('EQUIPMENT|FURNITURE|INTANGIBLE|ASSETS - COST', case=False, na=False)]
        fixed_assets_change = fixed_assets['debit'].sum() - fixed_assets['credit'].sum()
        
        if fixed_assets_change != 0:
            cash_flow.append({
                "Category": "", 
                "Description": "Capital Expenditures", 
                "Amount": f"({fixed_assets_change:,.2f})"
            })
        
        # Net cash used in investing activities
        net_investing_cash = -fixed_assets_change
        cash_flow.append({
            "Category": "", 
            "Description": "Net Cash used in Investing Activities", 
            "Amount": f"{net_investing_cash:,.2f}" if net_investing_cash >= 0 else f"({abs(net_investing_cash):,.2f})"
        })
        
        # Financing Activities
        cash_flow.append({"Category": "Financing Activities", "Description": "", "Amount": ""})
        
        # Partner transactions
        partner_accounts = self.df[self.df['account_name'].str.contains('PARTNER|CAPITAL|LOAN FROM', case=False, na=False)]
        partner_transactions = partner_accounts['credit'].sum() - partner_accounts['debit'].sum()
        
        if partner_transactions != 0:
            cash_flow.append({
                "Category": "", 
                "Description": "Partner Contributions/(Withdrawals)", 
                "Amount": f"{partner_transactions:,.2f}" if partner_transactions >= 0 else f"({abs(partner_transactions):,.2f})"
            })
        
        # Net cash from financing activities
        net_financing_cash = partner_transactions
        cash_flow.append({
            "Category": "", 
            "Description": "Net Cash from Financing Activities", 
            "Amount": f"{net_financing_cash:,.2f}" if net_financing_cash >= 0 else f"({abs(net_financing_cash):,.2f})"
        })
        
        # Net increase/decrease in cash
        cash_flow.append({
            "Category": "Net Increase/(Decrease) in Cash", 
            "Description": "", 
            "Amount": f"{net_cash_change:,.2f}" if net_cash_change >= 0 else f"({abs(net_cash_change):,.2f})"
        })
        
        # Cash at beginning of period
        beginning_cash = cash_accounts['opening_balance'].sum()
        cash_flow.append({
            "Category": "Cash at Beginning of Period", 
            "Description": "", 
            "Amount": f"{beginning_cash:,.2f}" if beginning_cash >= 0 else f"({abs(beginning_cash):,.2f})"
        })
        
        # Cash at end of period
        ending_cash = cash_accounts['closing_balance'].sum()
        cash_flow.append({
            "Category": "Cash at End of Period", 
            "Description": "", 
            "Amount": f"{ending_cash:,.2f}" if ending_cash >= 0 else f"({abs(ending_cash):,.2f})"
        })
        
        # Convert to DataFrame
        cf_df = pd.DataFrame(cash_flow)
        
        # Save to CSV
        cf_file_path = os.path.join(self.output_dir, "Cash_Flow_Statement.csv")
        cf_df.to_csv(cf_file_path, index=False)
        
        # Generate HTML version
        html_content = self._generate_html_statement(
            cf_df, 
            "Cash Flow Statement", 
            f"For the year ended {self.period_end}",
            columns=["Category", "Description", "Amount"]
        )
        
        html_file_path = os.path.join(self.output_dir, "Cash_Flow_Statement.html")
        with open(html_file_path, 'w') as f:
            f.write(html_content)
            
        print(f"Cash Flow Statement generated: {cf_file_path} and {html_file_path}")
        return cf_df
    
    def generate_visualizations(self):
        """Generate visualizations for financial analysis"""
        # Create visualizations directory
        viz_dir = os.path.join(self.output_dir, "Visualizations")
        os.makedirs(viz_dir, exist_ok=True)
        
        # 1. Expense Breakdown Pie Chart
        plt.figure(figsize=(12, 8))
        expenses = self.df[self.df['classification'] == 'Expense'].copy()
        
        # Group small expenses as "Other"
        threshold = expenses['closing_balance'].sum() * 0.03  # 3% threshold
        major_expenses = expenses[expenses['closing_balance'] >= threshold].copy()
        other_expenses = expenses[expenses['closing_balance'] < threshold].copy()
        
        if not other_expenses.empty:
            other_sum = other_expenses['closing_balance'].sum()
            major_expenses = pd.concat([
                major_expenses, 
                pd.DataFrame([{"account_name": "Other Expenses", "closing_balance": other_sum}])
            ])
        
        plt.pie(
            major_expenses['closing_balance'], 
            labels=major_expenses['account_name'], 
            autopct='%1.1f%%',
            startangle=90,
            shadow=True
        )
        plt.axis('equal')
        plt.title('Expense Breakdown', fontsize=16)
        plt.tight_layout()
        
        expense_pie_path = os.path.join(viz_dir, "expense_breakdown.png")
        plt.savefig(expense_pie_path)
        plt.close()
        
        # 2. Assets Composition Bar Chart
        plt.figure(figsize=(12, 8))
        assets = self.df[self.df['classification'] == 'Asset'].copy()
        assets = assets[assets['closing_balance'] > 0]  # Exclude contra assets
        
        sns.barplot(x='closing_balance', y='account_name', data=assets.sort_values('closing_balance'))
        plt.title('Asset Composition', fontsize=16)
        plt.xlabel('Amount (QAR)', fontsize=12)
        plt.ylabel('Asset Account', fontsize=12)
        plt.tight_layout()
        
        assets_bar_path = os.path.join(viz_dir, "asset_composition.png")
        plt.savefig(assets_bar_path)
        plt.close()
        
        # 3. Financial Position Summary
        plt.figure(figsize=(10, 6))
        
        # Calculate totals
        assets_total = self.df[self.df['classification'] == 'Asset']['closing_balance'].sum()
        liabilities_total = abs(self.df[self.df['classification'] == 'Liability']['closing_balance'].sum())
        equity_total = abs(self.df[self.df['classification'] == 'Equity']['closing_balance'].sum())
        revenue_total = abs(self.df[self.df['classification'] == 'Revenue']['closing_balance'].sum())
        expenses_total = self.df[self.df['classification'] == 'Expense']['closing_balance'].sum()
        
        # Create summary data
        categories = ['Assets', 'Liabilities', 'Equity', 'Revenue', 'Expenses']
        values = [assets_total, liabilities_total, equity_total, revenue_total, expenses_total]
        
        sns.barplot(x=categories, y=values)
        plt.title('Financial Position Summary', fontsize=16)
        plt.ylabel('Amount (QAR)', fontsize=12)
        plt.xticks(rotation=0)
        
        # Add value labels on top of bars
        for i, v in enumerate(values):
            plt.text(i, v + 5000, f"{v:,.0f}", ha='center')
            
        plt.tight_layout()
        
        summary_bar_path = os.path.join(viz_dir, "financial_summary.png")
        plt.savefig(summary_bar_path)
        plt.close()
        
        # 4. Profitability Analysis
        plt.figure(figsize=(8, 6))
        
        # Calculate net income/loss
        net_income = revenue_total - expenses_total
        
        # Create data for the waterfall chart
        labels = ['Revenue', 'Expenses', 'Net Income/(Loss)']
        values = [revenue_total, -expenses_total, net_income]
        colors = ['green', 'red', 'blue' if net_income >= 0 else 'red']
        
        # Create waterfall chart
        plt.bar(labels, values, color=colors)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.title('Profitability Analysis', fontsize=16)
        plt.ylabel('Amount (QAR)', fontsize=12)
        
        # Add value labels
        for i, v in enumerate(values):
            if i == 1:  # Expenses (negative value)
                plt.text(i, v/2, f"{abs(v):,.0f}", ha='center', color='white')
            else:
                plt.text(i, v/2 if v >= 0 else v*1.1, f"{abs(v):,.0f}", ha='center', 
                         color='white' if v >= 0 else 'black')
        
        plt.tight_layout()
        
        profitability_path = os.path.join(viz_dir, "profitability_analysis.png")
        plt.savefig(profitability_path)
        plt.close()
        
        print(f"Financial visualizations generated in: {viz_dir}")
        
        # Create an HTML dashboard with all visualizations
        self._generate_dashboard(viz_dir)
    
    def _generate_html_statement(self, df, title, subtitle, columns=None):
        """Generate HTML for financial statements"""
        if columns is None:
            columns = df.columns.tolist()
            
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} - {self.company_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    color: #333;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                h1 {{
                    color: #2c3e50;
                    margin-bottom: 5px;
                }}
                h2 {{
                    color: #7f8c8d;
                    font-weight: normal;
                    margin-top: 0;
                }}
                .company {{
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                .category {{
                    font-weight: bold;
                    background-color: #f9f9f9;
                }}
                .subcategory {{
                    padding-left: 20px;
                    font-weight: bold;
                }}
                .account {{
                    padding-left: 40px;
                }}
                .total {{
                    font-weight: bold;
                }}
                .grand-total {{
                    font-weight: bold;
                    border-top: 2px solid #333;
                    border-bottom: 2px solid #333;
                }}
                .amount {{
                    text-align: right;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    font-size: 12px;
                    color: #7f8c8d;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="company">{self.company_name}</div>
                <h1>{title}</h1>
                <h2>{subtitle}</h2>
                <p>Currency: {self.currency}</p>
            </div>
            
            <table>
                <thead>
                    <tr>
        """
        
        # Add table headers
        for col in columns:
            html += f"<th>{col}</th>"
        
        html += """
                    </tr>
                </thead>
                <tbody>
        """
        
        # Add table rows
        for _, row in df.iterrows():
            html += "<tr"
            
            # Apply styling based on content
            if row[columns[0]] and not row[columns[1]] and not row[columns[-1]]:
                html += ' class="category"'
            elif not row[columns[0]] and row[columns[1]] and row[columns[1]].startswith("Total "):
                html += ' class="total"'
            elif not row[columns[0]] and row[columns[1]] and row[columns[1]].startswith("TOTAL "):
                html += ' class="grand-total"'
            elif row[columns[0]] and not row[columns[1]]:
                html += ' class="subcategory"'
            elif not row[columns[0]] and row[columns[1]]:
                html += ' class="account"'
                
            html += ">"
            
            for col in columns:
                if col == columns[-1]:  # Amount column
                    html += f'<td class="amount">{row[col]}</td>'
                else:
                    html += f'<td>{row[col]}</td>'
            
            html += "</tr>"
        
        html += """
                </tbody>
            </table>
            
            <div class="footer">
                <p>Generated on {date} | Prepared in accordance with IFRS</p>
            </div>
        </body>
        </html>
        """.format(date=datetime.now().strftime("%B %d, %Y"))
        
        return html
    
    def _generate_dashboard(self, viz_dir):
        """Generate an HTML dashboard with all visualizations"""
        dashboard_path = os.path.join(self.output_dir, "Financial_Dashboard.html")
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Financial Dashboard - {self.company_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    background-color: #2c3e50;
                    color: white;
                    padding: 20px;
                    border-radius: 5px;
                }}
                h1 {{
                    margin-bottom: 5px;
                }}
                h2 {{
                    font-weight: normal;
                    margin-top: 0;
                    color: #ecf0f1;
                }}
                .dashboard {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }}
                .card {{
                    background-color: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    padding: 20px;
                    transition: transform 0.3s ease;
                }}
                .card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                .card h3 {{
                    color: #2c3e50;
                    margin-top: 0;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                }}
                .card img {{
                    width: 100%;
                    height: auto;
                    border-radius: 5px;
                }}
                .summary {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .metric {{
                    background-color: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    padding: 20px;
                    text-align: center;
                }}
                .metric h3 {{
                    margin-top: 0;
                    color: #7f8c8d;
                    font-size: 16px;
                }}
                .metric .value {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .metric .change {{
                    margin-top: 5px;
                    font-size: 14px;
                }}
                .positive {{
                    color: #27ae60;
                }}
                .negative {{
                    color: #e74c3c;
                }}
                .links {{
                    margin-top: 30px;
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                }}
                .links a {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background-color 0.3s ease;
                }}
                .links a:hover {{
                    background-color: #2980b9;
                }}
                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{self.company_name}</h1>
                <h2>Financial Dashboard - {self.period_end}</h2>
            </div>
            
            <div class="summary">
        """
        
        # Calculate key metrics
        assets_total = self.df[self.df['classification'] == 'Asset']['closing_balance'].sum()
        liabilities_total = self.df[self.df['classification'] == 'Liability']['closing_balance'].sum()
        equity_total = self.df[self.df['classification'] == 'Equity']['closing_balance'].sum()
        revenue_total = abs(self.df[self.df['classification'] == 'Revenue']['closing_balance'].sum())
        expenses_total = self.df[self.df['classification'] == 'Expense']['closing_balance'].sum()
        net_income = revenue_total - expenses_total
        
        # Add key metrics
        metrics = [
            {"name": "Total Revenue", "value": f"{revenue_total:,.2f}", "change": ""},
            {"name": "Net Income/(Loss)", "value": f"{net_income:,.2f}", "change": "negative" if net_income < 0 else "positive"},
            {"name": "Total Assets", "value": f"{assets_total:,.2f}", "change": ""},
            {"name": "Total Liabilities", "value": f"{abs(liabilities_total):,.2f}", "change": ""}
        ]
        
        for metric in metrics:
            html += f"""
                <div class="metric">
                    <h3>{metric['name']}</h3>
                    <div class="value {metric['change']}">{self.currency} {metric['value']}</div>
                </div>
            """
        
        html += """
            </div>
            
            <div class="dashboard">
        """
        
        # Add visualization cards
        visualizations = [
            {"file": "expense_breakdown.png", "title": "Expense Breakdown"},
            {"file": "asset_composition.png", "title": "Asset Composition"},
            {"file": "financial_summary.png", "title": "Financial Position Summary"},
            {"file": "profitability_analysis.png", "title": "Profitability Analysis"}
        ]
        
        for viz in visualizations:
            html += f"""
                <div class="card">
                    <h3>{viz['title']}</h3>
                    <img src="Visualizations/{viz['file']}" alt="{viz['title']}">
                </div>
            """
        
        html += """
            </div>
            
            <div class="links">
                <a href="Balance_Sheet.html" target="_blank">View Balance Sheet</a>
                <a href="Income_Statement.html" target="_blank">View Income Statement</a>
                <a href="Cash_Flow_Statement.html" target="_blank">View Cash Flow Statement</a>
            </div>
            
            <div class="footer">
                <p>Generated on {date} | Prepared in accordance with IFRS</p>
            </div>
        </body>
        </html>
        """.format(date=datetime.now().strftime("%B %d, %Y"))
        
        with open(dashboard_path, 'w') as f:
            f.write(html)
            
        print(f"Financial Dashboard generated: {dashboard_path}")


if __name__ == "__main__":
    # Path to the structured Trial Balance file
    tb_file_path = os.path.expanduser("~/Uploads/TB2024_structured_corrected.csv")
    
    # Create the financial statement generator
    generator = FinancialStatementGenerator(tb_file_path)
    
    # Generate all financial statements
    generator.generate_all_statements()
