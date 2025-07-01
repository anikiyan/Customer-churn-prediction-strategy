
SELECT
    c.customer_id,
    c.gender,
    c.age,
    c.segment,
    c.tenure_months,
    c.churn,
    ul.avg_logins,
    ul.avg_active_minutes,
    tk.total_tickets,
    tk.tickets_resolved,
    pm.total_payments,
    pm.failed_payments,
    pm.avg_payment
FROM customers c
LEFT JOIN (
    SELECT customer_id, 
           AVG(logins) AS avg_logins, 
           AVG(active_minutes) AS avg_active_minutes
    FROM usage_logs
    GROUP BY customer_id
) ul ON c.customer_id = ul.customer_id
LEFT JOIN (
    SELECT customer_id, 
           COUNT(ticket_id) AS total_tickets,
           SUM(CASE WHEN resolved = 'Yes' THEN 1 ELSE 0 END) AS tickets_resolved
    FROM tickets
    GROUP BY customer_id
) tk ON c.customer_id = tk.customer_id
LEFT JOIN (
    SELECT customer_id, 
           COUNT(payment_id) AS total_payments,
           SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS failed_payments,
           AVG(amount) AS avg_payment
    FROM payments
    GROUP BY customer_id
) pm ON c.customer_id = pm.customer_id;
