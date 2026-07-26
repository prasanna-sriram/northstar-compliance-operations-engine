/* ============================================================================
   File: management_review_views.sql
   Purpose: Views that feed ISO 27001 management review reporting -
            overdue corrective actions and residual risk exposure.
   Platform: Microsoft SQL Server (T-SQL)
   Tables referenced: corrective_actions, risk_register
   Author: Prasanna Sriram
   Last Updated: 2026-07-24
   ============================================================================ */

/* ----------------------------------------------------------------------------
   View: vw_OverdueCorrectiveActions
   Purpose: Identify corrective actions whose target_date has passed and
            which are not yet Closed, for escalation in management review.
   Logic: target_date < today AND status <> 'Closed'. days_overdue helps
          rank urgency for the review deck.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_OverdueCorrectiveActions AS
WITH ReiewDate
AS
(
    SELECT '2026-06-03' AS review_date
)
SELECT
    ca.ca_id,
    ca.source,
    ca.related_item,
    ca.root_cause,
    ca.owner,
    ca.opened_date,
    ca.target_date,
    DATEDIFF(DAY, ca.target_date, rd.review_date) AS days_overdue,
    ca.status,
    ca.effectiveness_review
FROM corrective_actions AS ca
CROSS JOIN ReiewDate AS rd
WHERE ca.target_date < CAST(rd.review_date AS DATE)
  AND ca.status <> 'Closed';
GO

/* ----------------------------------------------------------------------------
   View: vw_OpenRisksByResidualScore
   Purpose: Rank all open/in-progress risks by residual score descending,
            for the top-risks section of the management review memo.
   Logic: Filter to non-closed statuses; order by residual_score DESC so
          the highest-priority risks surface first for executives.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_OpenRisksByResidualScore AS
SELECT
    r.risk_id,
    r.risk_title,
    r.category,
    r.likelihood,
    r.impact,
    r.inherent_score,
    r.control_strength,
    r.residual_score,
    r.treatment_plan,
    r.owner,
    r.target_date,
    r.status
FROM risk_register AS r
WHERE r.status <> 'Closed';
GO

/* ----------------------------------------------------------------------------
   View: vw_HighResidualRiskPastDue
   Purpose: Flag risks that are both high residual severity (>= 10) AND
            past their treatment target date - the combination that
            demands immediate executive attention.
   Logic: residual_score threshold of 10 is a project-defined cutoff
          (roughly top half of the observed 5-20 scoring range).
          target_date in the past AND status not Closed = missed target.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_HighResidualRiskPastDue AS
SELECT
    r.risk_id,
    r.risk_title,
    r.category,
    r.residual_score,
    r.treatment_plan,
    r.owner,
    r.target_date,
    DATEDIFF(DAY, r.target_date, GETDATE()) AS days_past_target,
    r.status
FROM risk_register AS r
WHERE r.residual_score >= 10
  AND r.target_date < CAST(GETDATE() AS DATE)
  AND r.status <> 'Closed';
GO