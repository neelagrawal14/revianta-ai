-- ============================================================
-- REVIANTA AI
-- Migration 001: External Research Sources
-- ============================================================

-- ============================================================
-- PAPERS
-- ============================================================

CREATE TABLE IF NOT EXISTS papers (
    id BIGSERIAL PRIMARY KEY,

    record_id VARCHAR(64) UNIQUE NOT NULL,

    source VARCHAR(50) NOT NULL,
    external_id TEXT NOT NULL,

    title TEXT NOT NULL,
    abstract TEXT,

    authors JSONB DEFAULT '[]'::jsonb,

    publication_year INTEGER,
    publication_date DATE,

    doi TEXT,
    url TEXT,

    source_name TEXT,

    citation_count INTEGER DEFAULT 0,

    paper_type TEXT,

    open_access BOOLEAN,

    keywords JSONB DEFAULT '[]'::jsonb,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(source, external_id)
);


-- ============================================================
-- GITHUB REPOSITORIES
-- ============================================================

CREATE TABLE IF NOT EXISTS github_repositories (
    id BIGSERIAL PRIMARY KEY,

    record_id VARCHAR(64) UNIQUE NOT NULL,

    source VARCHAR(50) NOT NULL DEFAULT 'github',
    external_id TEXT NOT NULL,

    name TEXT NOT NULL,
    full_name TEXT,

    description TEXT,

    owner TEXT,
    url TEXT,

    stars INTEGER DEFAULT 0,
    forks INTEGER DEFAULT 0,
    watchers INTEGER DEFAULT 0,
    open_issues INTEGER DEFAULT 0,

    language TEXT,

    topics JSONB DEFAULT '[]'::jsonb,

    license TEXT,

    created_at_external TIMESTAMP,
    updated_at_external TIMESTAMP,
    pushed_at TIMESTAMP,

    default_branch TEXT,

    is_fork BOOLEAN DEFAULT FALSE,
    archived BOOLEAN DEFAULT FALSE,
    has_issues BOOLEAN DEFAULT TRUE,
    has_wiki BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(source, external_id)
);


-- ============================================================
-- DATASETS
-- ============================================================

CREATE TABLE IF NOT EXISTS datasets (
    id BIGSERIAL PRIMARY KEY,

    record_id VARCHAR(64) UNIQUE NOT NULL,

    source VARCHAR(50) NOT NULL,
    external_id TEXT NOT NULL,

    name TEXT NOT NULL,

    description TEXT,

    url TEXT,

    owner TEXT,

    license TEXT,

    tags JSONB DEFAULT '[]'::jsonb,

    downloads BIGINT DEFAULT 0,

    votes INTEGER DEFAULT 0,

    usability NUMERIC,

    created_at_external TIMESTAMP,
    updated_at_external TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(source, external_id)
);


-- ============================================================
-- PATENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS patents (
    id BIGSERIAL PRIMARY KEY,

    record_id VARCHAR(64) UNIQUE NOT NULL,

    source VARCHAR(50) NOT NULL,
    external_id TEXT NOT NULL,

    publication_number TEXT,

    title TEXT NOT NULL,

    abstract TEXT,
    summary TEXT,

    inventors JSONB DEFAULT '[]'::jsonb,

    assignee TEXT,

    filing_date DATE,
    publication_date DATE,

    grant_year INTEGER,

    priority_date DATE,

    country TEXT,
    kind TEXT,

    url TEXT,

    patent_type TEXT,

    citation_count INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(source, external_id)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_papers_source
ON papers(source);

CREATE INDEX IF NOT EXISTS idx_papers_external_id
ON papers(external_id);

CREATE INDEX IF NOT EXISTS idx_papers_publication_year
ON papers(publication_year);

CREATE INDEX IF NOT EXISTS idx_papers_doi
ON papers(doi);


CREATE INDEX IF NOT EXISTS idx_github_source
ON github_repositories(source);

CREATE INDEX IF NOT EXISTS idx_github_external_id
ON github_repositories(external_id);

CREATE INDEX IF NOT EXISTS idx_github_language
ON github_repositories(language);

CREATE INDEX IF NOT EXISTS idx_github_stars
ON github_repositories(stars);


CREATE INDEX IF NOT EXISTS idx_datasets_source
ON datasets(source);

CREATE INDEX IF NOT EXISTS idx_datasets_external_id
ON datasets(external_id);


CREATE INDEX IF NOT EXISTS idx_patents_source
ON patents(source);

CREATE INDEX IF NOT EXISTS idx_patents_external_id
ON patents(external_id);

CREATE INDEX IF NOT EXISTS idx_patents_publication_number
ON patents(publication_number);


-- ============================================================
-- COMPLETE
-- ============================================================

-- Migration 001 complete.