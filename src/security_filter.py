"""Security filter to check for internal information leaks"""
import re

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def generate_security_report(document: str, internal_info: dict, external_info: dict = None) -> str:
    """Generate a security report that identifies which internal information appears in the document"""
    
    detected_leaks = {
        'product_names': [],
        'partnerships': [],
        'methodologies': [],
        'kpis': [],
        'client_profiles': [],
        'financial_estimates': [],
        'expertise_areas': [],
        'risk_categories': [],
        'notes_content': [],
        'companies': [],
        'sensitive_metrics': []
    }
    
    # Convert document to lowercase for case-insensitive matching
    doc_lower = document.lower()
    
    # If internal_info is a single company's data, wrap it in a dict
    if isinstance(internal_info, dict) and 'industry' in internal_info:
        # This is a single company's internal data, create a wrapper
        company_data = {'Target Company': {'internal': internal_info}}
        if external_info:
            company_data['Target Company']['external'] = external_info
    else:
        # This is the full company database
        company_data = internal_info
    
    # Check each company's internal information
    for company_name, company_info in company_data.items():
        internal_data = company_info.get('internal', {})
        
        # Check if company name appears
        if company_name.lower() in doc_lower and company_name != 'Target Company':
            detected_leaks['companies'].append(company_name)
        
        # Check product names
        for product in internal_data.get('products', []):
            product_name = product.get('name', '')
            revenue = product.get('revenue_contribution', '')
            
            if product_name and product_name.lower() in doc_lower:
                detected_leaks['product_names'].append(f"{company_name}: {product_name}")
            
            # Check for revenue information in text
            if revenue and any(rev_part.lower() in doc_lower for rev_part in revenue.split()):
                detected_leaks['sensitive_metrics'].append(f"{company_name}: Product revenue - {revenue}")
        
        # Check partnerships
        for partnership in internal_data.get('partnerships', []):
            partner_name = partnership.get('partner_name', '')
            relationship = partnership.get('relationship_type', '')
            details = partnership.get('details', '')
            
            if partner_name and partner_name.lower() in doc_lower:
                detected_leaks['partnerships'].append(f"{company_name}: {partner_name}")
            
            # Check for specific partnership details
            if details and len(details) > 20:
                # Look for key phrases from partnership details
                detail_words = details.lower().split()[:10]  # First 10 words
                detail_phrase = ' '.join(detail_words)
                if detail_phrase in doc_lower:
                    detected_leaks['partnerships'].append(f"{company_name}: Partnership details with {partner_name}")
        
        # Check methodologies
        for methodology in internal_data.get('methodologies', []):
            if methodology and methodology.lower() in doc_lower:
                detected_leaks['methodologies'].append(f"{company_name}: {methodology}")
        
        # Check KPIs with more sophisticated matching
        for kpi in internal_data.get('kpis', []):
            if kpi:
                # Extract metric names and values
                kpi_match = re.match(r'([A-Za-z\s]+)\s+(\d+%?)', kpi)
                if kpi_match:
                    metric_name, value = kpi_match.groups()
                    # Check if metric name appears
                    if metric_name.strip().lower() in doc_lower:
                        detected_leaks['kpis'].append(f"{company_name}: {kpi}")
                    # Check if specific value appears
                    elif value in document:
                        detected_leaks['kpis'].append(f"{company_name}: {kpi}")
                
                # Also check for the full KPI string
                if kpi.lower() in doc_lower:
                    detected_leaks['kpis'].append(f"{company_name}: {kpi}")
        
        # Check client profiles
        for client_profile in internal_data.get('client_profiles', []):
            if client_profile and client_profile.lower() in doc_lower:
                detected_leaks['client_profiles'].append(f"{company_name}: {client_profile}")
        
        # Check financial estimates with pattern matching
        financial_est = internal_data.get('financial_estimates', '')
        if financial_est:
            # Look for financial patterns in both the estimate and document
            financial_patterns = re.findall(r'\$\d+[MBK]?\s*\w*', financial_est)
            for pattern in financial_patterns:
                if pattern.lower() in doc_lower:
                    detected_leaks['financial_estimates'].append(f"{company_name}: {financial_est}")
                    break
            
            # Also check for "ARR", "revenue", etc.
            if 'arr' in financial_est.lower() and 'arr' in doc_lower:
                detected_leaks['financial_estimates'].append(f"{company_name}: {financial_est}")
        
        # Check expertise areas
        for expertise in internal_data.get('expertise_areas', []):
            if expertise and expertise.lower() in doc_lower:
                detected_leaks['expertise_areas'].append(f"{company_name}: {expertise}")
        
        # Check risk category
        risk_category = internal_data.get('risk_category', '')
        if risk_category and risk_category.lower() in doc_lower:
            detected_leaks['risk_categories'].append(f"{company_name}: {risk_category}")
        
        # Check notes content with improved phrase detection
        notes = internal_data.get('notes', '')
        if notes:
            # Look for key business phrases that might be sensitive
            sensitive_phrases = [
                'strategic partnerships', 'regulatory pressures', 'operational challenges',
                'financial projections', 'material costs', 'regulatory compliance',
                'market presence', 'competitive advantages', 'innovation', 'pricing'
            ]
            
            for phrase in sensitive_phrases:
                if phrase in notes.lower() and phrase in doc_lower:
                    detected_leaks['notes_content'].append(f"{company_name}: Contains sensitive business information about {phrase}")
    
    # Remove duplicates while preserving order
    for category in detected_leaks:
        detected_leaks[category] = list(dict.fromkeys(detected_leaks[category]))
    
    # Generate report
    report_lines = ["=== SECURITY REPORT: INTERNAL INFORMATION DETECTION ===\n"]
    
    total_leaks = sum(len(leaks) for leaks in detected_leaks.values())
    
    if total_leaks == 0:
        report_lines.append("✅ No internal information detected in the document.\n")
        report_lines.append("The document appears safe for external sharing.")
    else:
        # Determine severity
        severity = "HIGH" if total_leaks >= 10 else "MEDIUM" if total_leaks >= 5 else "LOW"
        report_lines.append(f"⚠️  {severity} RISK: {total_leaks} potential information leak(s) detected!\n")
        
        # Priority order for display
        priority_categories = [
            ('financial_estimates', 'Financial Information'),
            ('sensitive_metrics', 'Sensitive Metrics'),
            ('notes_content', 'Confidential Business Information'),
            ('kpis', 'Key Performance Indicators'),
            ('product_names', 'Internal Product Names'),
            ('partnerships', 'Partnership Information'),
            ('client_profiles', 'Client Information'),
            ('risk_categories', 'Risk Classifications'),
            ('methodologies', 'Internal Methodologies'),
            ('expertise_areas', 'Expertise Areas'),
            ('companies', 'Company Names')
        ]
        
        for category_key, category_name in priority_categories:
            items = detected_leaks.get(category_key, [])
            if items:
                report_lines.append(f"\n🚨 {category_name}:")
                for item in items:
                    report_lines.append(f"  - {item}")
        
        report_lines.append(f"\n{'='*60}")
        report_lines.append("RECOMMENDATIONS:")
        if severity == "HIGH":
            report_lines.append("❌ DO NOT SHARE externally without review")
            report_lines.append("📋 Requires immediate security review")
        elif severity == "MEDIUM":
            report_lines.append("⚠️  Requires review before external sharing")
            report_lines.append("📝 Consider redacting sensitive information")
        else:
            report_lines.append("⚠️  Minor concerns - review recommended")
        
        report_lines.append("🔍 Verify all flagged information is appropriate for the target audience")
    
    return '\n'.join(report_lines)


class PromptInjectionFilter:
    def __init__(self):
        self.dangerous_patterns = [
            r'ignore\s+(all\s+)?previous\s+instructions?',
            r'you\s+are\s+now\s+(in\s+)?developer\s+mode',
            r'system\s+override',
            r'reveal\s+prompt',
        ]

        # Fuzzy matching for typoglycemia attacks
        self.fuzzy_patterns = [
            'ignore', 'bypass', 'override', 'reveal', 'delete', 'system'
        ]

    def detect_injection(self, text: str) -> bool:
        # Standard pattern matching
        if any(re.search(pattern, text, re.IGNORECASE)
               for pattern in self.dangerous_patterns):
            return True

        # Fuzzy matching for misspelled words (typoglycemia defense)
        words = re.findall(r'\b\w+\b', text.lower())
        for word in words:
            for pattern in self.fuzzy_patterns:
                if self._is_similar_word(word, pattern):
                    return True
        return False

    def _is_similar_word(self, word: str, target: str) -> bool:
        """Check if word is a typoglycemia variant of target"""
        if len(word) != len(target) or len(word) < 3:
            return False
        # Same first and last letter, scrambled middle
        return (word[0] == target[0] and
                word[-1] == target[-1] and
                sorted(word[1:-1]) == sorted(target[1:-1]))

    def sanitize_input(self, text: str) -> str:
        # Normalize common obfuscations
        text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
        text = re.sub(r'(.)\1{3,}', r'\1', text)  # Remove char repetition

        for pattern in self.dangerous_patterns:
            text = re.sub(pattern, '[FILTERED]', text, flags=re.IGNORECASE)
        return text[:10000]  # Limit length


class OutputValidator:
    def __init__(self):
        self.suspicious_patterns = [
            r'SYSTEM\s*[:]\s*You\s+are',     # System prompt leakage
            r'instructions?[:]\s*\d+\.',     # Numbered instructions
        ]

    def validate_output(self, output: str) -> bool:
        return not any(re.search(pattern, output, re.IGNORECASE)
                      for pattern in self.suspicious_patterns)

    def filter_response(self, response: str) -> str:
        if not self.validate_output(response) or len(response) > 5000:
            return "I cannot provide that information for security reasons."
        return response