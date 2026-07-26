/* ============================================================================
   File: tprm_views.sql
   Purpose: Third-party risk management reporting - high-risk vendors,
            open findings, and reassessment cadence tracking.
   Platform: Microsoft SQL Server (T-SQL)
   Tables referenced: vendors, vendor_assessments
   Author: Prasanna Sriram
   Last Updated: 2026-07-24
   ============================================================================ */

/* ----------------------------------------------------------------------------
   View: vw_HighRiskVendorsOpenFindings
   Purpose: Surface vendors tiered "High" that currently carry one or more
            open findings from their most recent assessment - these are
            the vendors with the greatest unresolved exposure.
   Logic: Join vendors to vendor_assessments on vendor_id. Use ROW_NUMBER
          to pick each vendor's most recent assessment by assessment_date,
          then filter to risk_tier = 'High' and open_findings > 0.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_HighRiskVendorsOpenFindings AS

WITH LatestAssessment 
AS 
(
    SELECT
        va.*,
        ROW_NUMBER() OVER (
            PARTITION BY va.vendor_id
            ORDER BY va.assessment_date DESC
        ) AS rn
    FROM vendor_assessment AS va
)

SELECT
    v.vendor_id,
    v.vendor_name,
    v.service_type,
    v.data_sensitivity,
    v.criticality,
    v.privileged_access,
    v.risk_tier,
    la.assessment_date AS latest_assessment_date,
    la.review_type,
    la.security_score,
    la.open_findings,
    la.next_review_due
FROM vendors AS v
INNER JOIN LatestAssessment AS la
    ON v.vendor_id = la.vendor_id
    AND la.rn = 1
WHERE v.risk_tier = 'High'
  AND la.open_findings > 0;
GO

/* ----------------------------------------------------------------------------
   View: vw_HighRiskVendorsReassessmentOverdue
   Purpose: Identify High-tier vendors that have NOT been reassessed within
            the last 12 months - a common SOC 2 / ISO audit sampling point.
   Logic: Take each vendor's latest assessment_date; flag High-tier vendors
          where that date is more than 365 days in the past.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_HighRiskVendorsReassessmentOverdue AS

WITH LatestAssessment 
AS 
(
    SELECT
        va.vendor_id,
        MAX(va.assessment_date) AS latest_assessment_date
    FROM vendor_assessment AS va
    GROUP BY va.vendor_id
)

SELECT
    v.vendor_id,
    v.vendor_name,
    v.risk_tier,
    v.criticality,
    la.latest_assessment_date,
    DATEDIFF(DAY, la.latest_assessment_date, GETDATE()) AS days_since_last_assessment
FROM vendors AS v
INNER JOIN LatestAssessment AS la
    ON v.vendor_id = la.vendor_id
WHERE v.risk_tier = 'High'
  AND DATEDIFF(DAY, la.latest_assessment_date, GETDATE()) > 365;
GO