SELECT title, ts_rank(title_vector, plainto_tsquery('фарш'))
FROM products
WHERE title_vector @@ plainto_tsquery('фарш')
ORDER BY ts_rank(title_vector, plainto_tsquery('фарш')) DESC;
