-- ============================================================================
-- ScamShield AI — Seed Data Fixtures for Supabase PostgreSQL
-- Author & Lead Architect: Ayusman Mishra (@Ayus-ProjeXion)
-- Version: 1.0.0
-- ============================================================================

-- 1. Seed Known IOCs (Blacklist & Whitelist)
INSERT INTO public.threat_iocs (ioc_type, ioc_value, severity, category, description, confidence, is_blacklisted, source)
VALUES
    -- Known Phishing Domains
    ('DOMAIN', 'sbi-kyc-verification-login.com', 'CRITICAL', 'PHISHING_URL', 'Spoofed State Bank of India KYC phishing portal harvesting netbanking credentials', 0.99, true, 'ScamShield Threat Intel'),
    ('DOMAIN', 'hdfc-rewards-points-claim.xyz', 'CRITICAL', 'PHISHING_URL', 'Malicious reward claim phishing landing page targeting HDFC cardholders', 0.98, true, 'ScamShield Threat Intel'),
    ('DOMAIN', 'netflix-billing-update-account.online', 'HIGH', 'CREDENTIAL_HARVESTING', 'Fake Netflix renewal form harvesting credit card numbers', 0.95, true, 'ScamShield Threat Intel'),
    ('DOMAIN', 'amazon-prime-deals-luckywinner.vip', 'HIGH', 'LOTTERY_JOB_SCAM', 'Fraudulent lottery winner claim asking for advance processing fees', 0.92, true, 'ScamShield Threat Intel'),
    
    -- Known Fraudulent Phone Numbers
    ('PHONE_NUMBER', '+919876543210', 'CRITICAL', 'SMISHING_SMS', 'High-volume smishing number dispatching fake electricity bill cutoff alerts', 0.96, true, 'National Cybercrime Feed'),
    ('PHONE_NUMBER', '+918765432109', 'HIGH', 'IMPERSONATION', 'Caller impersonating Mumbai Police / FedEx custom department extortion scam', 0.94, true, 'Community Telemetry'),

    -- Known Fraudulent UPI VPA Addresses
    ('UPI_VPA', 'custom.duty.clearance@ybl', 'CRITICAL', 'UPI_PAYMENT_FRAUD', 'Extortion payment handle associated with fake customs parcel threats', 0.99, true, 'ScamShield Blacklist'),
    ('UPI_VPA', 'instant.loan.sanction@okhdfcbank', 'HIGH', 'UPI_PAYMENT_FRAUD', 'Fake instant personal loan processing fee fraud', 0.93, true, 'ScamShield Blacklist'),

    -- Verified Whitelisted Safe Domains
    ('DOMAIN', 'onlinesbi.sbi', 'SAFE', 'PHISHING_URL', 'Official State Bank of India netbanking domain', 1.00, false, 'Verified Whitelist'),
    ('DOMAIN', 'hdfcbank.com', 'SAFE', 'PHISHING_URL', 'Official HDFC Bank main portal', 1.00, false, 'Verified Whitelist'),
    ('DOMAIN', 'amazon.in', 'SAFE', 'LOTTERY_JOB_SCAM', 'Official Amazon India e-commerce domain', 1.00, false, 'Verified Whitelist')
ON CONFLICT (ioc_value) DO NOTHING;

-- 2. Seed Mock Telemetry Scans
INSERT INTO public.threat_scans (id, channel, raw_payload, extracted_url, extracted_domain, extracted_phone, extracted_vpa)
VALUES
    ('c1111111-1111-1111-1111-111111111111', 'SMS', 'Dear Customer, your electricity power will be disconnected tonight at 9:30 PM due to unpaid bill. Immediately contact our officer at +919876543210 or update KYC at http://sbi-kyc-verification-login.com', 'http://sbi-kyc-verification-login.com', 'sbi-kyc-verification-login.com', '+919876543210', NULL),
    ('c2222222-2222-2222-2222-222222222222', 'URL', 'https://onlinesbi.sbi/portal/login', 'https://onlinesbi.sbi/portal/login', 'onlinesbi.sbi', NULL, NULL),
    ('c3333333-3333-3333-3333-333333333333', 'QR_CODE', 'upi://pay?pa=custom.duty.clearance@ybl&pn=CustomsClearance&am=4999', NULL, NULL, NULL, 'custom.duty.clearance@ybl')
ON CONFLICT (id) DO NOTHING;

-- 3. Seed Classifications for Mock Scans
INSERT INTO public.scam_classifications (scan_id, overall_severity, overall_risk_score, primary_category, deterministic_match, ai_confidence, explanation, detected_heuristics, processing_time_ms)
VALUES
    ('c1111111-1111-1111-1111-111111111111', 'CRITICAL', 98.50, 'PHISHING_URL', true, 0.99, 'Urgent electricity disconnection scam combined with blacklisted fake SBI banking domain. Multiple fraud markers triggered.', '["Known Phishing Domain", "Blacklisted Smishing Caller", "Extreme Urgency Framing", "Utility Disconnection Threat"]'::jsonb, 42),
    ('c2222222-2222-2222-2222-222222222222', 'SAFE', 2.00, 'PHISHING_URL', true, 0.01, 'Domain verified against official government and banking whitelist registry. Secure SSL and valid DNS records confirmed.', '["Official Whitelisted Domain", "Valid EV SSL Certificate", "No Deceptive Heuristics"]'::jsonb, 18),
    ('c3333333-3333-3333-3333-333333333333', 'CRITICAL', 95.00, 'UPI_PAYMENT_FRAUD', true, 0.97, 'Flagged UPI handle linked to ongoing fake customs duty extortion campaign. Direct funds transfer request with fraud history.', '["Blacklisted VPA Handle", "Extortion Keyword Match", "Impersonation of Customs Authority"]'::jsonb, 35)
ON CONFLICT (id) DO NOTHING;

-- 4. Seed Initial Community Reports
INSERT INTO public.community_reports (ioc_value, ioc_type, category, title, description, evidence_url, upvote_count, status)
VALUES
    ('sbi-kyc-verification-login.com', 'DOMAIN', 'PHISHING_URL', 'Fake SBI Netbanking link sent via SMS', 'Received SMS claiming PAN card is expired and asking to log in here. The page steals OTP.', 'https://imgbb.com/sample-evidence-sbi', 47, 'VERIFIED_SCAM'),
    ('+919876543210', 'PHONE_NUMBER', 'SMISHING_SMS', 'Electricity Power Cutoff Threat Spammer', 'Sent mass messages to 5 of my family members claiming power will be cut at 9:30 PM.', NULL, 31, 'VERIFIED_SCAM'),
    ('custom.duty.clearance@ybl', 'UPI_VPA', 'UPI_PAYMENT_FRAUD', 'Fake FedEx / Customs Clearance UPI Payment', 'Caller claiming they intercepted illegal drugs in my courier package and demanded Rs 5,000 clearance fee.', NULL, 64, 'VERIFIED_SCAM')
ON CONFLICT (id) DO NOTHING;
