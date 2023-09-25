CREATE EXTENSION IF NOT EXISTS vector;

/* 
For simplicity, we are directly adding the content into this table
Could easily be a foreign key of another table that has content you
want to vectorize for semantic search
*/

CREATE TABLE items (id bigserial PRIMARY KEY, content TEXT, embedding vector(768));