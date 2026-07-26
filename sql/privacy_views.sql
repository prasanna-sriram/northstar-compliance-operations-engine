/* ============================================================================
   File: privacy_views.sql
   Purpose: Privacy operations reporting - DSAR SLA tracking for
            PIPEDA-aligned response timelines.
   Platform: Microsoft SQL Server (T-SQL)
   Tables referenced: privacy_requests
   Author: Prasanna Sriram
   Last Updated: 2026-07-24
   ============================================================================ */

/* ----------------------------------------------------------------------------
   View: vw_DSARStatus
   Purpose: Classify every open or in-progress privacy request into an SLA
            status bucket (On Track / Due Soon / Past Due) based on the
            due_date relative to today. Closed requests are excluded since
            SLA risk no longer applies once resolved.
   Logic: "Past Due" = due_date < today; "Due Soon" = due_date within next
          7 days; everything else is "On Track".
   Consumers: Legal/Privacy weekly SLA review, DSAR SLA monitor script.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_DSARStatus AS
SELECT
    pr.request_id,
    pr.request_type,
    pr.received_date,
    pr.due_date,
    pr.status,
    pr.days_open,
    pr.owner,
    DATEDIFF(DAY, GETDATE(), pr.due_date) AS days_until_due,
    CASE
        WHEN pr.due_date < CAST(GETDATE() AS DATE) THEN 'Past Due'
        WHEN pr.due_date <= DATEADD(DAY, 7, CAST(GETDATE() AS DATE)) THEN 'Due Soon'
        ELSE 'On Track'
    END AS sla_status
FROM privacy_requests AS pr
WHERE pr.status <> 'Closed';
GO

/* ----------------------------------------------------------------------------
   View: vw_DSARPastDue
   Purpose: Narrow view of only the requests that have breached their SLA,
            for escalation to Legal/Privacy leadership.
   Logic: Reuses the same past-due logic as vw_DSARStatus, filtered down.
---------------------------------------------------------------------------- */
CREATE OR ALTER VIEW vw_DSARPastDue AS
SELECT
    pr.request_id,
    pr.request_type,
    pr.received_date,
    pr.due_date,
    DATEDIFF(DAY, pr.due_date, GETDATE()) AS days_past_due,
    pr.owner
FROM privacy_requests AS pr
WHERE pr.status <> 'Closed'
  AND pr.due_date < CAST(GETDATE() AS DATE);
GO