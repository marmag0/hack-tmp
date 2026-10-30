-- migrate:up

INSERT INTO example_items (name) VALUES
    ('First example item'),
    ('Second example item'),
    ('Third example item');


-- migrate:down

DELETE FROM example_items WHERE name IN (
    'First example item',
    'Second example item',
    'Third example item'
);
