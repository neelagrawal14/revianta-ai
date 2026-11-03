
-- ============================================================
-- REVIANTA AI
-- Migration 002: Projects and External Research Relationships
-- ============================================================

-- ============================================================
-- PROJECTS
-- ============================================================

CREATE TABLE IF NOT EXISTS projects (
    id BIGSERIAL PRIMARY KEY,

    name TEXT NOT NULL,

    title TEXT NOT NULL,

    description TEXT,

    status VARCHAR(30) DEFAULT 'active',

    created_by TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- PROJECT ↔ PAPERS
-- ============================================================

CREATE TABLE IF NOT EXISTS project_papers (
    project_id BIGINT NOT NULL,

    paper_id BIGINT NOT NULL,

    relevance_score NUMERIC(6,5),

    relationship_type VARCHAR(50) DEFAULT 'related',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (project_id, paper_id),

    CONSTRAINT fk_project_papers_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_project_papers_paper
        FOREIGN KEY (paper_id)
        REFERENCES papers(id)
        ON DELETE CASCADE
);


-- ============================================================
-- PROJECT ↔ GITHUB
-- ============================================================

CREATE TABLE IF NOT EXISTS project_github (
    project_id BIGINT NOT NULL,

    github_id BIGINT NOT NULL,

    relevance_score NUMERIC(6,5),

    relationship_type VARCHAR(50) DEFAULT 'related',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (project_id, github_id),

    CONSTRAINT fk_project_github_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_project_github_repository
        FOREIGN KEY (github_id)
        REFERENCES github_repositories(id)
        ON DELETE CASCADE
);


-- ============================================================
-- PROJECT ↔ DATASETS
-- ============================================================

CREATE TABLE IF NOT EXISTS project_datasets (
    project_id BIGINT NOT NULL,

    dataset_id BIGINT NOT NULL,

    relevance_score NUMERIC(6,5),

    relationship_type VARCHAR(50) DEFAULT 'related',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (project_id, dataset_id),

    CONSTRAINT fk_project_datasets_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_project_datasets_dataset
        FOREIGN KEY (dataset_id)
        REFERENCES datasets(id)
        ON DELETE CASCADE
);


-- ============================================================
-- PROJECT ↔ PATENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS project_patents (
    project_id BIGINT NOT NULL,

    patent_id BIGINT NOT NULL,

    relevance_score NUMERIC(6,5),

    relationship_type VARCHAR(50) DEFAULT 'related',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (project_id, patent_id),

    CONSTRAINT fk_project_patents_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_project_patents_patent
        FOREIGN KEY (patent_id)
        REFERENCES patents(id)
        ON DELETE CASCADE
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_projects_status
ON projects(status);

CREATE INDEX IF NOT EXISTS idx_projects_created_at
ON projects(created_at);

CREATE INDEX IF NOT EXISTS idx_project_papers_paper
ON project_papers(paper_id);

CREATE INDEX IF NOT EXISTS idx_project_github_repository
ON project_github(github_id);

CREATE INDEX IF NOT EXISTS idx_project_datasets_dataset
ON project_datasets(dataset_id);

CREATE INDEX IF NOT EXISTS idx_project_patents_patent
ON project_patents(patent_id);


-- ============================================================
-- COMPLETE
-- ============================================================