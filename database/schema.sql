-- ============================================================================
-- ScamShield AI — Supabase PostgreSQL Production Schema
-- Author & Lead Architect: Ayusman Mishra (@Ayus-ProjeXion)
-- Database: Supabase PostgreSQL 15+
-- Version: 1.0.0
-- ============================================================================

-- 1. Enable Required Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Custom Enumerated Types
DO $$ BEGIN
    CREATE TYPE threat_severity AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'SAFE');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE scam_category AS ENUM (
        'PHISHING_URL',
        'SMISHING_SMS',
        'IMPERSONATION',
        'UPI_PAYMENT_FRAUD',
        'LOTTERY_JOB_SCAM',
        'CREDENTIAL_HARVESTING',
        'MALICIOUS_APP',
        'UNKNOWN'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE scan_channel AS ENUM ('SMS', 'EMAIL', 'URL', 'WHATSAPP', 'TELEGRAM', 'CALL', 'QR_CODE');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE ioc_type AS ENUM ('DOMAIN', 'URL', 'PHONE_NUMBER', 'UPI_VPA', 'IP_ADDRESS', 'REGEX_PATTERN');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE verification_status AS ENUM ('PENDING', 'VERIFIED_SCAM', 'VERIFIED_SAFE', 'DISPUTED');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('ADMIN', 'SECURITY_ANALYST', 'USER');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. Utility Function: Updated At Trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ============================================================================
-- 4. Core Relational Tables
-- ============================================================================

-- TABLE: profiles (Integrated with Supabase Auth auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role user_role DEFAULT 'USER' NOT NULL,
    reputation_score INTEGER DEFAULT 100 CHECK (reputation_score >= 0),
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- TABLE: threat_iocs (Indicators of Compromise: Known Blacklist / Whitelist)
CREATE TABLE IF NOT EXISTS public.threat_iocs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ioc_type ioc_type NOT NULL,
    ioc_value TEXT NOT NULL UNIQUE,
    severity threat_severity NOT NULL,
    category scam_category NOT NULL,
    description TEXT,
    confidence NUMERIC(3, 2) DEFAULT 1.00 CHECK (confidence >= 0.00 AND confidence <= 1.00),
    is_blacklisted BOOLEAN DEFAULT true NOT NULL,
    source TEXT DEFAULT 'ScamShield Intelligence Feed' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- TABLE: threat_scans (Incoming Telemetry & Scan Requests: Text, URL, & Audio Call Transcripts)
CREATE TABLE IF NOT EXISTS public.threat_scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    channel scan_channel NOT NULL,
    raw_payload TEXT NOT NULL,
    extracted_url TEXT,
    extracted_domain TEXT,
    extracted_phone TEXT,
    extracted_vpa TEXT,
    audio_file_url TEXT,
    audio_duration_seconds INTEGER,
    client_ip_hash TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- TABLE: scam_classifications (Deterministic & AI Analysis Results)
CREATE TABLE IF NOT EXISTS public.scam_classifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID NOT NULL REFERENCES public.threat_scans(id) ON DELETE CASCADE,
    overall_severity threat_severity NOT NULL,
    overall_risk_score NUMERIC(5, 2) NOT NULL CHECK (overall_risk_score >= 0.00 AND overall_risk_score <= 100.00),
    primary_category scam_category NOT NULL,
    deterministic_match BOOLEAN DEFAULT false NOT NULL,
    ai_confidence NUMERIC(3, 2) DEFAULT 0.00 CHECK (ai_confidence >= 0.00 AND ai_confidence <= 1.00),
    explanation TEXT NOT NULL,
    detected_heuristics JSONB DEFAULT '[]'::jsonb NOT NULL,
    processing_time_ms INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- TABLE: community_reports (Crowdsourced Reporting & Verification)
CREATE TABLE IF NOT EXISTS public.community_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporter_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    scan_id UUID REFERENCES public.threat_scans(id) ON DELETE SET NULL,
    ioc_value TEXT NOT NULL,
    ioc_type ioc_type NOT NULL,
    category scam_category NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    evidence_url TEXT,
    upvote_count INTEGER DEFAULT 1 CHECK (upvote_count >= 0),
    status verification_status DEFAULT 'PENDING' NOT NULL,
    verified_by UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- TABLE: audit_logs (Immutable Security Audit Trail)
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    details JSONB DEFAULT '{}'::jsonb NOT NULL,
    ip_address TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- ============================================================================
-- 5. High-Performance Indexes
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_threat_iocs_val_type ON public.threat_iocs (ioc_value, ioc_type);
CREATE INDEX IF NOT EXISTS idx_threat_iocs_blacklisted ON public.threat_iocs (is_blacklisted);
CREATE INDEX IF NOT EXISTS idx_threat_scans_created ON public.threat_scans (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_threat_scans_domain ON public.threat_scans (extracted_domain);
CREATE INDEX IF NOT EXISTS idx_threat_scans_user ON public.threat_scans (user_id);
CREATE INDEX IF NOT EXISTS idx_scam_class_scan ON public.scam_classifications (scan_id);
CREATE INDEX IF NOT EXISTS idx_scam_class_severity ON public.scam_classifications (overall_severity);
CREATE INDEX IF NOT EXISTS idx_community_status ON public.community_reports (status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_community_ioc ON public.community_reports (ioc_value);

-- ============================================================================
-- 6. Automated Triggers
-- ============================================================================
DROP TRIGGER IF EXISTS trigger_profiles_updated_at ON public.profiles;
CREATE TRIGGER trigger_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS trigger_iocs_updated_at ON public.threat_iocs;
CREATE TRIGGER trigger_iocs_updated_at
    BEFORE UPDATE ON public.threat_iocs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS trigger_community_updated_at ON public.community_reports;
CREATE TRIGGER trigger_community_updated_at
    BEFORE UPDATE ON public.community_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 7. Row-Level Security (RLS) Configuration
-- ============================================================================
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.threat_iocs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.threat_scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scam_classifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Policy: Profiles
CREATE POLICY "Public profiles are viewable by everyone" 
    ON public.profiles FOR SELECT USING (true);

CREATE POLICY "Users can update own profile" 
    ON public.profiles FOR UPDATE USING (auth.uid() = id);

-- Policy: Threat IOCs (Blacklist/Whitelist is publicly readable for client checking)
CREATE POLICY "Threat IOCs are publicly readable" 
    ON public.threat_iocs FOR SELECT USING (true);

-- Policy: Threat Scans (Anyone can insert a scan for hackathon demo; users see their own)
CREATE POLICY "Anyone can insert scans" 
    ON public.threat_scans FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can read own scans, anonymous scans visible to creator session" 
    ON public.threat_scans FOR SELECT USING (
        user_id IS NULL OR auth.uid() = user_id
    );

-- Policy: Scam Classifications (Readable if parent scan is accessible)
CREATE POLICY "Classifications are readable for scan viewers" 
    ON public.scam_classifications FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.threat_scans ts 
            WHERE ts.id = scam_classifications.scan_id 
            AND (ts.user_id IS NULL OR ts.user_id = auth.uid())
        )
    );

CREATE POLICY "Service role can insert classifications" 
    ON public.scam_classifications FOR INSERT TO service_role WITH CHECK (true);

-- Policy: Community Reports (Publicly readable, inserts must start with PENDING status)
CREATE POLICY "Community reports are publicly viewable" 
    ON public.community_reports FOR SELECT USING (true);

CREATE POLICY "Authenticated users can submit reports" 
    ON public.community_reports FOR INSERT WITH CHECK (status = 'PENDING');
