/* ============================================================================
   File: compliance_views.sql
   Purpose: Core control monitoring views for evidence freshness, policy
            review status, and control test failures.
   Platform: Microsoft SQL Server (T-SQL)
   Tables referenced: controls, evidence_inventory, policy_register,
                       control_tests
   Author: Prasanna Sriram
   Last Updated: 2026-07-24
   ============================================================================ */

/* ----------------------------------------------------------------------------
   View: vw_StaleEvidenceByOwner
   Purpose: Identify all evidence records that are past their next_due_date,
            grouped so audit/compliance can chase owners for refresh.
   Logic: An evidence item is "stale" if next_due_date is in the past
          relative to GETDATE(). We also surface days_overdue to help
          prioritize follow-up.
   Consumers: Weekly compliance ops standup, audit readiness tracking.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_StaleEvidenceByOwner AS
SELECT
    e.evidence_id,
    e.control_id,
    e.evidence_name,
    e.source_system,
    e.owner,
    e.last_collected_date,
    e.next_due_date,
    e.status,
    DATEDIFF(DAY, e.next_due_date, GETDATE()) AS days_overdue
FROM evidence_inventory AS e
WHERE e.next_due_date < CAST(GETDATE() AS DATE);
GO

/* ----------------------------------------------------------------------------
   View: vw_EvidenceDueSoon
   Purpose: Surface evidence due within the next 14 days so owners can
            proactively refresh before it goes stale.
   Logic: next_due_date falls between today and today + 14 days.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_EvidenceDueSoon AS
SELECT
    e.evidence_id,
    e.control_id,
    e.evidence_name,
    e.owner,
    e.next_due_date,
    DATEDIFF(DAY, CAST(GETDATE() AS DATE), e.next_due_date) AS days_until_due
FROM evidence_inventory AS e
WHERE e.next_due_date BETWEEN CAST(GETDATE() AS DATE)
                           AND DATEADD(DAY, 14, CAST(GETDATE() AS DATE));
GO

/* ----------------------------------------------------------------------------
   View: vw_MissingEvidenceByControl
   Purpose: Identify controls that currently have zero evidence records
            attached at all (as opposed to stale evidence). This catches
            controls that were defined but never had evidence operationalized.
   Logic: LEFT JOIN controls to evidence_inventory; any control with a NULL
          evidence_id after the join has no evidence on file.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_MissingEvidenceByControl AS
SELECT
    c.control_id,
    c.control_name,
    c.domain,
    c.owner,
    c.evidence_required
FROM controls AS c
LEFT JOIN evidence_inventory AS e
    ON c.control_id = e.control_id
WHERE e.evidence_id IS NULL;
GO

/* ----------------------------------------------------------------------------
   View: vw_OverduePolicyReviews
   Purpose: List all policies whose next_review_due date is more than 30
            days in the past, indicating a governance lapse.
   Logic: Use DATEDIFF to compute how many days past due, filter > 30.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_OverduePolicyReviews AS
SELECT
    p.policy_id,
    p.policy_name,
    p.owner,
    p.version,
    p.last_review_date,
    p.next_review_date,
    DATEDIFF(DAY, p.next_review_date, GETDATE()) AS days_overdue,
    p.attestation_required,
    p.status
FROM policy_register AS p
WHERE DATEDIFF(DAY, p.next_review_date, GETDATE()) > 30;
GO

/* ----------------------------------------------------------------------------
   View: vw_FailedControlTestsByDomain
   Purpose: Roll up failed and "pass with observation" control test results
            by control domain, to spot systemic weak spots rather than
            one-off failures.
   Logic: Join control_tests to controls to get domain; classify result
          into a simplified outcome bucket; aggregate counts by domain
          and outcome.
---------------------------------------------------------------------------- */

CREATE OR ALTER VIEW vw_FailedControlTestsByDomain AS

WITH DomainOutcomes
AS
(
	SELECT c.domain,
	CASE
		WHEN ct.result = 'Fail' THEN 'Fail'
		WHEN ct.result = 'Pass with Observation' THEN 'Pass With Observation'
		ELSE 'Pass'
	END AS outcome_bracket
	FROM control_tests ct
	INNER JOIN controls c
	on ct.control_id = c.control_id
)

SELECT 
    doc.domain, 
    doc.outcome_bracket, 
    COUNT(*) AS test_count
FROM DomainOutcomes doc
WHERE doc.outcome_bracket IN ('Fail', 'Pass With Observation')
GROUP BY 
    doc.domain, 
    doc.outcome_bracket
GO