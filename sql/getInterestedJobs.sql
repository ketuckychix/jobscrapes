SELECT j.CompanyName, j.JobTitle, j.JobLink
FROM jobs j
INNER JOIN (
    SELECT CompanyName, JobTitle, MAX(id) AS max_id
    FROM jobs
    WHERE SalaryLower >= 60000
    GROUP BY CompanyName, JobTitle
) sub ON j.id = sub.max_id
