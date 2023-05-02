DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL
);

id, url_id, status_code, h1, title, description, created_at

DROP TABLE IF EXISTS url_checks;

CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint REFERENCES urls (id),
    status_code bigint,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description text,
    created_at TIMESTAMP NOT NULL
);
